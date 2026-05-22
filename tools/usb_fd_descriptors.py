#!/usr/bin/env python3
import ctypes
import fcntl
import os
import struct
import sys


USB_DT_DEVICE = 0x01
USB_DT_CONFIG = 0x02
USB_DT_STRING = 0x03
USB_DT_INTERFACE = 0x04
USB_DT_ENDPOINT = 0x05
USB_DT_INTERFACE_ASSOCIATION = 0x0B

USB_DIR_IN = 0x80
USB_TYPE_STANDARD = 0x00
USB_RECIP_DEVICE = 0x00
USB_REQ_GET_DESCRIPTOR = 0x06

USBDEVFS_CONTROL_IOCTL_CANDIDATES = (
    0xC0185500,  # 64-bit usbdevfs_ctrltransfer
    0xC0105500,  # 32-bit usbdevfs_ctrltransfer
)


class UsbdevfsCtrlTransfer(ctypes.Structure):
    _fields_ = [
        ("bRequestType", ctypes.c_uint8),
        ("bRequest", ctypes.c_uint8),
        ("wValue", ctypes.c_uint16),
        ("wIndex", ctypes.c_uint16),
        ("wLength", ctypes.c_uint16),
        ("timeout", ctypes.c_uint32),
        ("data", ctypes.c_void_p),
    ]


def fd_from_args():
    if "TERMUX_USB_FD" in os.environ:
        return int(os.environ["TERMUX_USB_FD"])
    if len(sys.argv) > 1:
        return int(sys.argv[1])
    raise SystemExit("No USB fd argument or TERMUX_USB_FD env var")


def ctrl_get_descriptor(fd, dtype, index, length, langid=0):
    buf = ctypes.create_string_buffer(length)
    ctrl = UsbdevfsCtrlTransfer(
        USB_DIR_IN | USB_TYPE_STANDARD | USB_RECIP_DEVICE,
        USB_REQ_GET_DESCRIPTOR,
        (dtype << 8) | index,
        langid,
        length,
        1000,
        ctypes.cast(buf, ctypes.c_void_p),
    )
    errors = []
    for ioctl_code in USBDEVFS_CONTROL_IOCTL_CANDIDATES:
        try:
            n = fcntl.ioctl(fd, ioctl_code, ctrl)
            if n < 0:
                raise OSError("USBDEVFS_CONTROL returned %d" % n)
            return bytes(buf.raw[:n])
        except OSError as exc:
            errors.append("0x%08x:%s" % (ioctl_code, exc))
    raise OSError("; ".join(errors))


def read_usbfs_descriptors(fd):
    try:
        os.lseek(fd, 0, os.SEEK_SET)
    except OSError:
        pass
    return os.read(fd, 65536)


def get_string(fd, index):
    if index == 0:
        return ""
    try:
        langs = ctrl_get_descriptor(fd, USB_DT_STRING, 0, 255)
        if len(langs) < 4:
            langid = 0x0409
        else:
            langid = struct.unpack_from("<H", langs, 2)[0]
        raw = ctrl_get_descriptor(fd, USB_DT_STRING, index, 255, langid)
        if len(raw) < 2:
            return ""
        return raw[2:].decode("utf-16-le", errors="replace")
    except Exception as exc:
        return "<unreadable: %s>" % exc


def parse_device_descriptor(data):
    if len(data) < 18:
        raise ValueError("device descriptor too short: %d bytes" % len(data))
    fields = struct.unpack_from("<BBHBBBBHHHBBBB", data, 0)
    return {
        "bLength": fields[0],
        "bDescriptorType": fields[1],
        "bcdUSB": fields[2],
        "bDeviceClass": fields[3],
        "bDeviceSubClass": fields[4],
        "bDeviceProtocol": fields[5],
        "bMaxPacketSize0": fields[6],
        "idVendor": fields[7],
        "idProduct": fields[8],
        "bcdDevice": fields[9],
        "iManufacturer": fields[10],
        "iProduct": fields[11],
        "iSerialNumber": fields[12],
        "bNumConfigurations": fields[13],
    }


def parse_config_descriptors(config):
    interfaces = []
    iads = []
    current_interface = None
    pos = 0
    while pos + 2 <= len(config):
        length = config[pos]
        dtype = config[pos + 1]
        if length < 2 or pos + length > len(config):
            break
        if dtype == USB_DT_INTERFACE_ASSOCIATION and length >= 8:
            fields = struct.unpack_from("<BBBBBBBB", config, pos)
            iads.append({
                "bFirstInterface": fields[2],
                "bInterfaceCount": fields[3],
                "bFunctionClass": fields[4],
                "bFunctionSubClass": fields[5],
                "bFunctionProtocol": fields[6],
                "iFunction": fields[7],
            })
        elif dtype == USB_DT_INTERFACE and length >= 9:
            fields = struct.unpack_from("<BBBBBBBBB", config, pos)
            current_interface = {
                "bInterfaceNumber": fields[2],
                "bAlternateSetting": fields[3],
                "bNumEndpoints": fields[4],
                "bInterfaceClass": fields[5],
                "bInterfaceSubClass": fields[6],
                "bInterfaceProtocol": fields[7],
                "iInterface": fields[8],
                "endpoints": [],
            }
            interfaces.append(current_interface)
        elif dtype == USB_DT_ENDPOINT and length >= 7 and current_interface is not None:
            fields = struct.unpack_from("<BBBBHB", config, pos)
            current_interface["endpoints"].append({
                "bEndpointAddress": fields[2],
                "bmAttributes": fields[3],
                "wMaxPacketSize": fields[4],
                "bInterval": fields[5],
            })
        pos += length
    return interfaces, iads


def hex2(value):
    return "0x%02x" % value


def hex4(value):
    return "0x%04x" % value


def main():
    fd = fd_from_args()
    print("FD=%d" % fd)
    try:
        print("FD_LINK=%s" % os.readlink("/proc/%d/fd/%d" % (os.getpid(), fd)))
    except OSError as exc:
        print("FD_LINK=<unreadable: %s>" % exc)

    source = "control"
    try:
        dev_raw = ctrl_get_descriptor(fd, USB_DT_DEVICE, 0, 18)
    except Exception as exc:
        source = "usbfs-read"
        blob = read_usbfs_descriptors(fd)
        if len(blob) < 18:
            raise
        dev_raw = blob[:18]
        print("CONTROL_DEVICE_DESCRIPTOR_ERROR=%s" % exc)

    dev = parse_device_descriptor(dev_raw)
    print("DESCRIPTOR_SOURCE=%s" % source)
    print("vendorId=%s" % hex4(dev["idVendor"]))
    print("productId=%s" % hex4(dev["idProduct"]))
    print("bcdUSB=0x%04x" % dev["bcdUSB"])
    print("bcdDevice=0x%04x" % dev["bcdDevice"])
    print("deviceClass=%s" % hex2(dev["bDeviceClass"]))
    print("deviceSubClass=%s" % hex2(dev["bDeviceSubClass"]))
    print("deviceProtocol=%s" % hex2(dev["bDeviceProtocol"]))
    print("maxPacketSize0=%d" % dev["bMaxPacketSize0"])
    print("numConfigurations=%d" % dev["bNumConfigurations"])
    print("manufacturer=%s" % get_string(fd, dev["iManufacturer"]))
    print("product=%s" % get_string(fd, dev["iProduct"]))
    print("serial=%s" % get_string(fd, dev["iSerialNumber"]))

    try:
        head = ctrl_get_descriptor(fd, USB_DT_CONFIG, 0, 9)
        total_len = struct.unpack_from("<H", head, 2)[0]
        config = ctrl_get_descriptor(fd, USB_DT_CONFIG, 0, total_len)
    except Exception as exc:
        print("CONFIG_DESCRIPTOR_ERROR=%s" % exc)
        return

    if len(config) >= 9:
        cfg = struct.unpack_from("<BBHBBBBB", config, 0)
        print("configurationTotalLength=%d" % cfg[2])
        print("numInterfaces=%d" % cfg[3])
        print("configurationValue=%d" % cfg[4])
        print("configurationAttributes=%s" % hex2(cfg[6]))
        print("maxPower_mA=%d" % (cfg[7] * 2))

    interfaces, iads = parse_config_descriptors(config)
    print("interfaceAssociations.count=%d" % len(iads))
    for i, iad in enumerate(iads):
        name = get_string(fd, iad["iFunction"])
        print(
            "iad[%d]=first:%d count:%d class:%s subclass:%s protocol:%s name:%s"
            % (
                i,
                iad["bFirstInterface"],
                iad["bInterfaceCount"],
                hex2(iad["bFunctionClass"]),
                hex2(iad["bFunctionSubClass"]),
                hex2(iad["bFunctionProtocol"]),
                name,
            )
        )
    print("interfaces.count=%d" % len(interfaces))
    for i, iface in enumerate(interfaces):
        name = get_string(fd, iface["iInterface"])
        print(
            "interface[%d]=number:%d alt:%d endpoints:%d class:%s subclass:%s protocol:%s name:%s"
            % (
                i,
                iface["bInterfaceNumber"],
                iface["bAlternateSetting"],
                iface["bNumEndpoints"],
                hex2(iface["bInterfaceClass"]),
                hex2(iface["bInterfaceSubClass"]),
                hex2(iface["bInterfaceProtocol"]),
                name,
            )
        )
        for j, ep in enumerate(iface["endpoints"]):
            direction = "IN" if ep["bEndpointAddress"] & 0x80 else "OUT"
            print(
                "  endpoint[%d.%d]=address:%s direction:%s attributes:%s maxPacket:%d interval:%d"
                % (
                    i,
                    j,
                    hex2(ep["bEndpointAddress"]),
                    direction,
                    hex2(ep["bmAttributes"]),
                    ep["wMaxPacketSize"],
                    ep["bInterval"],
                )
            )


if __name__ == "__main__":
    main()

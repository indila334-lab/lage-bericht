# USB FD Descriptor Inspection

Read-only helper for inspecting an Android/Termux USB file descriptor opened by `termux-usb`.

## XiaoZhi cube check

List devices:

```bash
termux-usb -l
```

Grant access and run descriptor inspection:

```bash
termux-usb -r -e ~/usb_fd_descriptors.py /dev/bus/usb/001/005
```

If the script is stored elsewhere, use the full path:

```bash
termux-usb -r -e /data/data/com.termux/files/home/usb_fd_descriptors.py /dev/bus/usb/001/005
```

## Expected current cube identity

The tested XiaoZhi cube appeared as:

```text
vendorId:     0x303a
productId:    0x1001
manufacturer: Espressif
product:      USB JTAG/serial debug unit
serial:       1C:DB:D4:79:3F:AC
```

The descriptor contains a CDC serial function and a vendor-specific JTAG/debug interface.

## Safety

This tool only reads standard USB descriptors through the file descriptor passed by `termux-usb`.

Do not use it as a flashing workflow. It does not run `esptool.py`, `idf.py flash`, bootloader commands, erase commands, reboot commands, write commands, or firmware upload commands.

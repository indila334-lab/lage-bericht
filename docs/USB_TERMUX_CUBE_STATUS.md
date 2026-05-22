# USB / Termux / XiaoZhi cube status

Date: 2026-05-23 around midnight Moscow time.

## Summary

The phone can see the XiaoZhi cube through the UGREEN USB-C hub.

The working physical chain is:

```text
Honor Magic 6 Pro -> UGREEN USB-C hub -> USB cable -> XiaoZhi cube
```

The hub needed external power.

## Device detection

`termux-usb -l` initially returned two devices:

```text
/dev/bus/usb/001/004
/dev/bus/usb/001/003
```

After unplugging the cube, only this remained:

```text
/dev/bus/usb/001/003
```

Therefore:

```text
003 = hub
004 = cube before reconnect
```

After reconnecting the cube, the list became:

```text
/dev/bus/usb/001/005
/dev/bus/usb/001/003
```

Therefore:

```text
003 = hub
005 = cube after reconnect
```

USB device numbers can change after unplug/replug.

## Permission

The command:

```bash
termux-usb -r /dev/bus/usb/001/005
```

showed Android's USB permission dialog and then returned:

```text
Permission granted.
```

## tty check

Regular Linux serial paths were not created:

```text
/dev/ttyACM* -> No such file or directory
/dev/ttyUSB* -> No such file or directory
/dev/ttyS*   -> No such file or directory
```

So the cube is not available as a normal `/dev/ttyUSB0` or `/dev/ttyACM0` device in this Termux environment.

## termux-usb file descriptor test

`termux-usb -h` confirmed support for:

```text
-e command
-E
```

A small script was created in the Termux home directory and executed through `termux-usb -e`.

Successful command pattern:

```bash
termux-usb -e ~/usbfd.sh /dev/bus/usb/001/005
```

Successful output:

```text
FD_TEST_RUNNING
FD_ARG=7
/proc/11595/fd/7 -> /dev/bus/usb/001/005
```

Meaning:

```text
Termux received an opened file descriptor for the XiaoZhi cube and passed it to the script as fd 7.
```

## Read-only USB descriptor result

Pluton/OpenCode connected through the already running SSH bridge and ran read-only USB descriptor inspection through the `termux-usb` file descriptor path.

No flash, erase, write, reboot, or bootloader commands were used.

Device:

```text
/dev/bus/usb/001/005
```

Descriptors:

```text
vendorId:      0x303a
productId:     0x1001
manufacturer:  Espressif
product:       USB JTAG/serial debug unit
serial:        1C:DB:D4:79:3F:AC

USB:           2.00
deviceClass:   0xef
subClass:      0x02
protocol:      0x01
config:        1
maxPower:      500 mA
```

Interfaces:

```text
IAD:
  first: 0
  count: 2
  class: 0x02
  subclass: 0x02

interface 0:
  class 0x02, subclass 0x02, protocol 0x00
  endpoint IN 0x82 interrupt

interface 1:
  class 0x0a, subclass 0x02, protocol 0x00
  endpoint OUT 0x01 bulk
  endpoint IN  0x81 bulk

interface 2:
  class 0xff, subclass 0xff, protocol 0x01
  endpoint OUT 0x02 bulk
  endpoint IN  0x83 bulk
```

Conclusion from descriptor inspection:

```text
The cube exposes an Espressif ESP32-S3 native USB device: USB JTAG/serial debug unit.
It includes a CDC serial part and a vendor-specific JTAG part.
The absence of /dev/ttyUSB0 and /dev/ttyACM0 is an Android/Termux access model issue, not evidence that the cube is not exposing USB serial/JTAG.
```

## Current conclusion

- The phone sees the cube through the hub.
- Android granted Termux access to the cube.
- No normal tty serial device appeared.
- The usable path is currently `termux-usb -e` / file descriptor based access.
- The device is confirmed as Espressif `USB JTAG/serial debug unit` with vendorId `0x303a`, productId `0x1001`.
- Next step: save Pluton's descriptor script if useful, then decide whether to use Android USB FD tooling for read-only inspection/serial access, or switch to a normal computer for flashing/debugging if needed.

## Safety rule

Do not flash, erase, reboot into bootloader, or write anything to the cube without explicit confirmation.
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

## Current conclusion

- The phone sees the cube through the hub.
- Android granted Termux access to the cube.
- No normal tty serial device appeared.
- The usable path is currently `termux-usb -e` / file descriptor based access.
- Next step for Pluton/OpenCode: inspect USB descriptors through the passed fd and determine whether the cube exposes ESP32 CDC/JTAG/serial interfaces via Android USB API.

## Safety rule

Do not flash, erase, reboot into bootloader, or write anything to the cube without explicit confirmation.

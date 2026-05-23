# Severin USB: как подключали кубик через UGREEN hub

Дата: 2026-05-23

Короткая памятка, как Марина физически подключала XiaoZhi / Xingzhi cube к телефону и как проверяли, что Android/Termux его видит.

## Физическая цепочка

```text
телефон -> UGREEN USB-C hub -> кубик
```

Важно: кабель от hub к кубику должен быть data-кабелем, не только зарядным. Если кабель только для зарядки, телефон может питать кубик, но не увидит USB-устройство.

## Что вчера точно работало

Телефон видел UGREEN hub и кубик через Android USB host.

Примерные пути тогда были:

```text
hub:  /dev/bus/usb/001/003
cube: /dev/bus/usb/001/005
```

После переподключения номера могут измениться. Не привязываться намертво к `001/005`; сначала всегда смотреть список.

## Проверка в Termux

Сначала список USB-устройств:

```bash
termux-usb -l
```

Если всё хорошо, вывод похож на:

```json
[
  "/dev/bus/usb/001/005",
  "/dev/bus/usb/001/003"
]
```

Потом запросить доступ к кубику:

```bash
termux-usb -r /dev/bus/usb/001/005
```

Ожидаемый результат:

```text
Permission granted
```

## Важный вывод

Обычные Linux serial paths тогда НЕ появились:

```text
/dev/ttyUSB0
/dev/ttyACM0
```

Это не было ошибкой. Android дал доступ не как обычный tty-порт, а как raw USB file descriptor через `termux-usb`.

Успешный FD test выглядел так:

```text
FD_TEST_RUNNING
FD_ARG=7
/proc/11595/fd/7 -> /dev/bus/usb/001/005
```

## Что показала USB-диагностика

Кубик определился как Espressif native USB device:

```text
vendorId:     0x303a
productId:    0x1001
manufacturer: Espressif
product:      USB JTAG/serial debug unit
serial:       1C:DB:D4:79:3F:AC
```

Интерфейсы:

```text
CDC serial часть
vendor-specific JTAG/debug часть
```

## Если сейчас телефон не видит кубик

Проверять по порядку:

1. Воткнуть UGREEN hub в телефон.
2. Убедиться, что на телефоне включён OTG, если такая настройка есть. На некоторых телефонах OTG само выключается через несколько минут.
3. Воткнуть кубик в USB-порт hub data-кабелем.
4. Запустить:

```bash
termux-usb -l
```

5. Если вывод `[]`, телефон вообще не видит USB-устройств. Проверять OTG, hub, питание, кабель.
6. Если виден hub, но не cube, проверять порт hub, кабель к кубику и питание кубика.
7. Если снова появился путь вида `/dev/bus/usb/001/00X`, запросить доступ:

```bash
termux-usb -r /dev/bus/usb/001/00X
```

## Чего не делать в этом этапе

Это памятка про подключение и диагностику. Не запускать случайно:

```text
flash
erase
write_flash
bootloader
reboot
idf.py flash
esptool.py write_flash
```

Сначала только добиться, чтобы `termux-usb -l` снова видел кубик.

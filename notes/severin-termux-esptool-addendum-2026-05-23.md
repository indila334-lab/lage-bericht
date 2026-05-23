# Addendum: esptool на Termux поднят

Дата: 2026-05-23

Контекст: дополнение к капсуле `notes/severin-xiaozhi-cube-handoff-2026-05-23.md`.

После проблем с `pip install esptool` удалось поднять `esptool` в Termux.

## Что сделали

1. `cryptography` поставили через Termux:

```bash
pkg install python-cryptography
```

2. `esptool 5.2.0` не ставился из-за `tibs` / Rust.

3. Поставили зависимости постарше:

```bash
python3 -m pip install --no-cache-dir "bitarray<3.8" "bitstring<4.4"
```

4. Поставили:

```bash
python3 -m pip install --no-cache-dir "esptool==5.1.0"
```

5. `pySerial` на Android падал с ошибкой:

```text
ImportError: Sorry: no implementation for your platform ('posix') available
```

6. Исправили файл:

```text
/data/data/com.termux/files/usr/lib/python3.13/site-packages/serial/tools/list_ports_posix.py
```

В начало файла вместо обычного `import sys` добавили:

```python
import sys
if sys.platform == 'android':
    sys.platform = 'linux'
```

## Текущий смысл

`esptool` на Termux теперь поднят через версию `5.1.0` и ручной Android workaround для `pySerial`.

Это только заметка состояния. Сам факт установки `esptool` не означает, что кубик уже прошит.

## Важно

Не хранить токены, пароли, Wi-Fi secrets и личные ключи в GitHub.

Перед любой прошивкой отдельно подтвердить:

- что телефон заряжен;
- что файл прошивки правильный;
- что SHA256 совпадает;
- что порт/USB-доступ к кубику определён корректно;
- что команда прошивки не запускается случайно.

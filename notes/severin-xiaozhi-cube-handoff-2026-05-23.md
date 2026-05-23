# Северин: XiaoZhi cube, Termux-мост, OTA/WebSocket, прошивка

Дата: 2026-05-23
Проект: Северин
Пользователь: Марина

Репозитории:
- `indila334-lab/xiaozhi-esp32`
- `indila334-lab/lage-bericht`

Важно: в этом тексте нет паролей, GitHub token, Wi-Fi-паролей и других секретов. GitHub token использовался только локально для `git push`; сохранять его в GitHub нельзя.

---

## 1. Главная цель

Строим локальную систему для кубика XiaoZhi / Xingzhi Cube:

```text
xiaozhi cube
    -> домашний Wi-Fi
    -> Android phone + Termux
    -> локальный Flask/WebSocket сервер Северина
    -> дальше мозг / API / голос / мордашка
```

Идея: кубик должен ходить не на внешний сервер Tenclass, а на локальный сервер Северина на телефоне.

Текущий локальный адрес телефона в домашней сети:

```text
192.168.0.101
```

Текущий локальный сервер:

```text
http://192.168.0.101:8787
```

Предупреждение: адрес `192.168.0.101` зашит в текущую сборку прошивки. Если телефон получит другой IP от роутера, нужно либо закрепить IP, либо пересобрать прошивку с новым `CONFIG_OTA_URL`.

---

## 2. Где лежит проект на телефоне

В Termux проект лежит здесь:

```bash
~/xiaozhi-esp32
```

Текущая ветка:

```text
severin-local-bridge-save
```

Удалённый репозиторий:

```text
origin https://github.com/indila334-lab/xiaozhi-esp32.git
```

После push ветка отслеживает:

```text
origin/severin-local-bridge-save
```

---

## 3. Что уже сделано в локальном сервере

Файл:

```text
server/gpt_server.py
```

Сервер Flask работает на:

```text
HOST = 0.0.0.0
PORT = 8787
```

Рабочие HTTP routes:

```text
/
/health
/v1/models
/v1/chat/completions
/xiaozhi/ota/
/xiaozhi/ota
```

Рабочий WebSocket route:

```text
/xiaozhi/ws
```

---

## 4. Проверенные ответы сервера

Health:

```bash
curl -s http://127.0.0.1:8787/health
```

Ответ:

```json
{"service":"severin-local-bridge","status":"ok"}
```

OTA endpoint:

```bash
curl -s http://127.0.0.1:8787/xiaozhi/ota/
```

Ответ содержит `server_time` и `websocket`, где `websocket.url` указывает на:

```text
ws://192.168.0.101:8787/xiaozhi/ws
```

Также проверено по Wi-Fi:

```bash
curl -s http://192.168.0.101:8787/xiaozhi/ota/
```

И тоже отдаёт JSON с websocket.

---

## 5. Что выяснили по XiaoZhi OTA

В `main/ota.cc` найдено, что кубик сначала ищет настройку `wifi.ota_url`, а если её нет, берёт `CONFIG_OTA_URL`.

Поиск не нашёл места, где проект сам записывает `SetString(ota_url)`.

Выбран путь: вшить локальный OTA URL через `CONFIG_OTA_URL`.

В `sdkconfig.defaults` добавлено:

```text
CONFIG_OTA_URL=http://192.168.0.101:8787/xiaozhi/ota/
```

Это уже сохранено и отправлено в GitHub-ветку.

---

## 6. WebSocket-протокол XiaoZhi

Из `docs/websocket.md` выяснили порядок:

1. Кубик подключается к WebSocket.
2. Кубик первым отправляет `hello`.
3. Сервер отвечает `hello`.
4. После этого аудиоканал считается открытым.

Серверный `hello` должен сообщать:

```text
type: hello
transport: websocket
session_id: severin-local
audio format: opus
sample_rate: 24000
channels: 1
frame_duration: 60
```

Также сервер может отправлять кубику:

```text
stt  - показать распознанный текст
llm  - эмоция / мордашка
tts  - состояние речи и субтитры
```

---

## 7. Что реализовано в `/xiaozhi/ws`

В `server/gpt_server.py` добавлено:

```python
from flask_sock import Sock
import json
```

Инициализация:

```python
app = Flask(__name__)
sock = Sock(app)
```

WebSocket route:

```python
@sock.route('/xiaozhi/ws')
def xiaozhi_ws(ws):
    ...
```

Логика:

1. Принимает WebSocket-соединение.
2. Ждёт первое сообщение от устройства.
3. Печатает первое сообщение в лог.
4. Отправляет правильный server hello.
5. Дальше слушает сообщения.
6. Если получает текстовый JSON `listen start` или `listen detect`, отправляет тестовую пачку `stt`, `llm`, `tts start`, `tts sentence_start`, `tts stop`.

Тестовая фраза:

```text
Марина, я слышу. Локальный мост жив.
```

Тестовый subtitle:

```text
Северин на локальном мосту. Голос ещё не пришит, но нервная система уже щёлкает.
```

Если приходят binary frames, сервер пока только логирует размер:

```text
XIAOZHI WS BINARY AUDIO BYTES: <len>
```

Настоящий голос пока не реализован. Для реального звука нужно генерировать или передавать Opus audio frames.

---

## 8. WebSocket тест прошёл

Тестовый клиент в Termux через `simple_websocket` успешно подключился к:

```text
ws://127.0.0.1:8787/xiaozhi/ws
```

Результат:

```text
HELLO_REPLY: server hello получен
MSG 1: stt - Марина, я слышу. Локальный мост жив.
MSG 2: llm - emotion happy
MSG 3: tts - state start
MSG 4: tts - sentence_start
MSG 5: tts - state stop
OK: Severin sends STT/LLM/TTS test sequence
```

Вывод: локальный сервер уже умеет принимать XiaoZhi-style WebSocket handshake и отправлять STT/LLM/TTS тестовую последовательность.

---

## 9. Как запускать сервер после перезагрузки телефона

После перезагрузки телефона сервер в Termux умирает. Запуск вручную:

```bash
cd ~/xiaozhi-esp32
kill $(cat ~/severin_server.pid 2>/dev/null) 2>/dev/null
python3 server/gpt_server.py > ~/severin_server.log 2>&1 &
echo $! > ~/severin_server.pid
sleep 3
cat ~/severin_server.log
```

В логе должно быть:

```text
Running on http://127.0.0.1:8787
Running on http://192.168.0.101:8787
```

Проверка:

```bash
curl -s http://127.0.0.1:8787/health
curl -s http://192.168.0.101:8787/xiaozhi/ota/
```

---

## 10. Библиотеки в Termux

Для WebSocket поставили:

```bash
python3 -m pip install flask-sock
```

Проверка дала:

```text
OK flask_sock
OK simple_websocket
OK wsproto
OK h11
```

Был warning:

```text
httpcore 1.0.4 requires h11<0.15,>=0.13, but you have h11 0.16.0
```

Пока это не мешает Flask/WebSocket. Если позже будет подключение OpenAI/httpx и вылезет ошибка, нужно будет чинить версию `h11` или `httpcore`.

---

## 11. GitHub push и workflow

Был создан GitHub token classic с правом `repo`, использован только для git push. Токен не сохранять и не коммитить.

Push прошёл успешно:

```text
8b5ddae..29440c7  severin-local-bridge-save -> severin-local-bridge-save
branch severin-local-bridge-save set up to track origin/severin-local-bridge-save
```

Актуальный HEAD на GitHub:

```text
29440c7 Add Severin Xingzhi cube build workflow
```

---

## 12. Как выбирали плату

По списку boards нашли семейство:

```text
xingzhi-cube-*
```

Кандидаты:

```text
xingzhi-cube-0.85tft-ml307
xingzhi-cube-0.85tft-wifi
xingzhi-cube-0.96oled-ml307
xingzhi-cube-0.96oled-wifi
xingzhi-cube-1.54tft-ml307
xingzhi-cube-1.54tft-wifi
```

По фото устройства и наклейке:

```text
модель: AI 20
связь: 4G/WIFI
экран: маленький чёрный прямоугольный OLED
```

Выбран board:

```text
xingzhi-cube-0.96oled-ml307
```

Почему:

- `0.96oled` совпадает с экраном;
- `ml307` соответствует 4G/WIFI версии, а не чистому Wi-Fi.

Файлы board:

```text
main/boards/xingzhi-cube-0.96oled-ml307/config.json
main/boards/xingzhi-cube-0.96oled-ml307/config.h
main/boards/xingzhi-cube-0.96oled-ml307/xingzhi-cube-0.96oled-ml307.cc
```

В `config.h` для этой платы:

```text
OLED SSD1306
DISPLAY_WIDTH 128
DISPLAY_HEIGHT 64
audio input 16000
audio output 24000
ML307 pins есть
```

---

## 13. Почему сборку делали через GitHub Actions

В Termux нет ESP-IDF:

```bash
command -v idf.py || echo NO: idf.py not in PATH
```

Результат:

```text
NO: idf.py not in PATH
```

ESP-IDF на телефоне не ставили, потому что это тяжело и капризно.

Сделали GitHub Actions workflow:

```text
.github/workflows/severin-xingzhi-build.yml
```

Workflow:

- name: `Severin Xingzhi Cube Build`
- trigger: push в `severin-local-bridge-save` и `workflow_dispatch`
- runner: `ubuntu-latest`
- container: `espressif/idf:v5.5.2`
- build command: `python scripts/release.py xingzhi-cube-0.96oled-ml307`
- artifact: `build/merged-binary.bin`

---

## 14. GitHub Actions сборка прошла успешно

На GitHub Actions:

```text
Status: Success
Artifacts: 1
Build xingzhi-cube-0.96oled-ml307
```

Был только warning про устаревший Node.js 20 action, это не остановило сборку.

Артефакт:

```text
severin_xingzhi_cube_0.96oled_ml307_29440c7eba36e9962d013f6cdaa30d6a528f90ca.zip
```

Внутри:

```text
merged-binary.bin
```

Размер внутри архива:

```text
8952071 bytes
```

После распаковки на телефоне:

```text
/sdcard/Download/severin-firmware/merged-binary.bin
```

Размер:

```text
8.6M
```

SHA256:

```text
a6491521c9549e8c7bcd16615dc1fe5a7a6b755fd441a0742eacfb9addf3b495
```

Команды распаковки:

```bash
cd ~/xiaozhi-esp32
mkdir -p /sdcard/Download/severin-firmware
unzip -l /sdcard/Download/severin_xingzhi_cube_0.96oled_ml307_29440c7eba36e9962d013f6cdaa30d6a528f90ca.zip
unzip -o /sdcard/Download/severin_xingzhi_cube_0.96oled_ml307_29440c7eba36e9962d013f6cdaa30d6a528f90ca.zip -d /sdcard/Download/severin-firmware
ls -lh /sdcard/Download/severin-firmware
sha256sum /sdcard/Download/severin-firmware/merged-binary.bin
```

---

## 15. Что НЕ сделано ещё

Пока не сделано:

1. Кубик ещё не прошит новой прошивкой.
2. Не проверено, видит ли Termux USB-serial кубик через телефон.
3. Не проверено, установлен ли esptool.
4. Не проверено, как кубик поведёт себя после прошивки.
5. Не реализован настоящий STT/TTS/audio pipeline.
6. Не реализована передача Opus-аудио в кубик.
7. Не подключён настоящий OpenAI/GPT мозг к WebSocket-циклу.
8. IP `192.168.0.101` пока жёстко зашит, это временно.

---

## 16. Следующий шаг

Сейчас следующий шаг в Termux:

```bash
python3 -m pip show esptool >/dev/null 2>&1 && echo OK: esptool installed || echo NO: esptool not installed
```

Если esptool не установлен:

```bash
python3 -m pip install esptool
```

Дальше нужно решить, как шить.

### Вариант A: через телефон

Нужны:

- USB-C OTG;
- кабель к кубику;
- чтобы Termux увидел serial device;
- возможно, доступ к `/dev/ttyACM*` или `/dev/ttyUSB*`.

Проверка:

```bash
ls -l /dev/ttyACM* /dev/ttyUSB* 2>/dev/null
```

Или смотреть через Termux:API / rootless USB access, если стандартный доступ не даст.

### Вариант B: через ноутбук/ПК

Проще и безопаснее.

Файл:

```text
merged-binary.bin
```

Вероятная команда прошивки через esptool.py на offset `0x0`, потому что это merged binary, собранный через idf.py merge-bin:

```bash
esptool.py --chip esp32s3 --port <PORT> write_flash 0x0 merged-binary.bin
```

Перед фактической прошивкой нужно ещё раз подтвердить порт, режим загрузчика и способ входа в bootloader для конкретного кубика.

---

## 17. Критичные предупреждения

1. Телефон нужно зарядить. Во время работы было 12-15%, это опасно для прошивки.
2. Не хранить GitHub token в чатах и репозиториях.
3. Перед прошивкой убедиться, что файл именно:

```text
/sdcard/Download/severin-firmware/merged-binary.bin
```

И hash именно:

```text
a6491521c9549e8c7bcd16615dc1fe5a7a6b755fd441a0742eacfb9addf3b495
```

4. Если телефон после перезагрузки получил другой IP, прошивка будет смотреть на старый OTA:

```text
http://192.168.0.101:8787/xiaozhi/ota/
```

Тогда либо вернуть телефону IP `192.168.0.101`, либо пересобрать прошивку с новым OTA URL.

---

## 18. Текущий статус коротко

Сделано:

- локальный Flask server
- `/health`
- `/v1/chat/completions`
- `/xiaozhi/ota/`
- `/xiaozhi/ws`
- XiaoZhi WebSocket hello-flow
- STT/LLM/TTS test sequence
- `CONFIG_OTA_URL` на локальный телефон
- GitHub branch pushed
- GitHub Actions build
- `merged-binary.bin` downloaded and extracted
- SHA256 checked

Следующее:

- проверить esptool
- подключить кубик
- прошить `merged-binary.bin`
- запустить сервер на телефоне
- проверить, приходит ли кубик на `/xiaozhi/ota/` и `/xiaozhi/ws`
- смотреть логи `severin_server.log`

Файл прошивки:

```text
/sdcard/Download/severin-firmware/merged-binary.bin
```

SHA256:

```text
a6491521c9549e8c7bcd16615dc1fe5a7a6b755fd441a0742eacfb9addf3b495
```

Это текущая точка сохранения. Если чат потеряется, продолжать с проверки esptool и способа прошивки кубика.

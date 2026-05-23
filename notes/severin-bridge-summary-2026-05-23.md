Марина, принимаю руль. Вот тебе капсула состояния проекта: что мы сделали, где стоим, куда идём. Это можно целиком копировать в GitHub, лучше в файл:

notes/severin-bridge-summary-2026-05-23.md

Ниже без паролей, без QR, без секретов. Только мясо проекта. 🐠🔧


---

Северин: Termux-мост, xiaozhi-кубик, OTA/WebSocket

Дата: 2026-05-23

1. Главная цель

Мы строим локальную “домашнюю базу Северина”:

кубик xiaozhi / ESP32
        ↓
домашняя Wi-Fi сеть
        ↓
телефон Android с Termux
        ↓
локальный сервер Северина
        ↓
дальше мозг / API / мордашка / камера

Идея: чтобы кубик мог обращаться не куда-то в туман, а к нашему локальному серверу на телефоне.

Телефон сейчас играет роль маленькой серверной комнаты в кармане.
Termux, это подвал. Flask-сервер, это лампочка. Кубик, это зверёк, которого мы пытаемся научить стучать в правильную дверь.


---

2. Где лежит проект

Проект на телефоне в Termux:

~/xiaozhi-esp32

Рабочая ветка:

severin-local-bridge-save

Основной локальный сервер:

server/gpt_server.py

Папка server уже существует, там есть:

gpt_server.py
requirements.txt


---

3. Что уже работает

Мы сделали и подняли Flask-мост Северина.

Он слушает:

HOST = "0.0.0.0"
PORT = 8787

Это важно: 0.0.0.0 означает, что сервер доступен не только внутри телефона через 127.0.0.1, но и из домашней Wi-Fi сети.

Сервер имеет маршруты:

/
 /health
/v1/models
/v1/chat/completions

Маршрут /v1/chat/completions сделан в стиле OpenAI-compatible API, то есть принимает POST-запрос с JSON:

{
  "model": "test",
  "messages": [
    {
      "role": "user",
      "content": "..."
    }
  ]
}

И возвращает ответ формата chat.completion.


---

4. Подтверждённые проверки

После перезагрузки телефона сервер был поднят заново.

Он сам показал в логе:

Running on http://127.0.0.1:8787
Running on http://192.168.0.101:8787

То есть рабочий адрес в домашней сети на тот момент:

http://192.168.0.101:8787

Проверка /health успешно прошла:

curl -i --max-time 5 http://192.168.0.101:8787/health

Ответ:

{"service":"severin-local-bridge","status":"ok"}

Проверка chat endpoint тоже прошла:

curl -i --max-time 10 -X POST http://192.168.0.101:8787/v1/chat/completions -H "Content-Type: application/json" --data-binary @severin_test.json

Ответ был успешный, HTTP/1.1 200 OK.

Сервер вернул:

Северин-мост жив. Я услышал: Северин, домашняя база закреплена?

Вывод: локальный HTTP-мост работает.


---

5. Важная команда запуска после перезагрузки телефона

После перезагрузки телефона Termux-процесс умирает.
Это нормально. Это не из-за роутера, не из-за статики, не из-за VPN.

Телефон перезагрузился, сервер лёг. Его надо запускать заново.

Команда для заметок:

cd ~/xiaozhi-esp32
kill $(cat ~/severin_server.pid 2>/dev/null) 2>/dev/null
python3 server/gpt_server.py > ~/severin_server.log 2>&1 &
echo $! > ~/severin_server.pid
sleep 3
cat ~/severin_server.log

После запуска смотреть строку:

Running on http://192.168.0.xxx:8787

Вот этот xxx и есть текущий адрес домашней базы.

Не гадать между 100 и 101.
Не нюхать роутер как шаманский гриб.
Смотреть, что сам Flask написал в лог. Это и есть истина.


---

6. Команды проверки

Проверить здоровье сервера

curl -i --max-time 5 http://192.168.0.xxx:8787/health

Пример:

curl -i --max-time 5 http://192.168.0.101:8787/health

Проверить chat endpoint

Сначала создать тестовый JSON, если файла нет:

cd ~/xiaozhi-esp32
cat > severin_test.json <<'EOF'
{"model":"test","messages":[{"role":"user","content":"Северин, домашняя база закреплена?"}]}
EOF

Потом проверить:

curl -i --max-time 10 -X POST http://192.168.0.xxx:8787/v1/chat/completions -H "Content-Type: application/json" --data-binary @severin_test.json


---

7. Что выяснили про IP и роутер

Роутер: старый TP-Link, интерфейс зелёный, модель из серии TL-WR841N / TL-WR841.

Мы пытались сделать резервирование адреса DHCP.

Была путаница между:

192.168.0.100
192.168.0.101

Что стало понятно:

1. Телефон может получать адрес с задержкой.


2. Роутер может применять резервирование не мгновенно.


3. После перезагрузки телефона актуальный IP был 192.168.0.101.


4. Старый TP-Link ведёт себя как дед с бумажным журналом: записал одно, вспомнил другое, применил третье.



Рабочий принцип теперь такой:

Не спорить с роутером. Смотреть адрес в логе Flask после запуска.


---

8. VPN / proxy / ChatGPT

На телефоне есть VPN/proxy, потому что без него ChatGPT может не работать.

Для локального сервера это обычно не проблема, потому что адреса вида:

192.168.0.xxx
127.0.0.1

это локальная сеть, не внешний интернет.

Но если VPN включит режим “блокировать локальную сеть”, тогда кубик может не достучаться до телефона.

Пока Termux сам успешно обращался к:

127.0.0.1
192.168.0.101

Значит внутри телефона и по Wi-Fi всё живо.


---

9. Что выяснили про xiaozhi-esp32

Мы начали читать код, чтобы понять, куда кубик вообще смотрит.

Поиск по проекту показал, что кубик не выглядит как устройство, куда просто вставляется OpenAI URL.

То есть наш адрес:

http://192.168.0.101:8787/v1/chat/completions

это рабочий HTTP-мозг, но кубик, похоже, не говорит с ним напрямую.

Кубик работает через:

OTA config
WebSocket
или MQTT

Главные файлы:

main/Kconfig.projbuild
main/ota.cc
main/protocols/websocket_protocol.cc
main/protocols/mqtt_protocol.cc
docs/websocket.md
docs/mqtt-udp.md


---

10. Что нашли в Kconfig

В main/Kconfig.projbuild есть настройка:

config OTA_URL
    string "Default OTA URL"
    default "https://api.tenclass.net/xiaozhi/ota/"

И подсказка:

The application will access this URL to check for new firmwares and server address.

Перевод по-человечески:

Кубик ходит на OTA URL не только за прошивкой, но и за адресом сервера.

То есть он спрашивает:

> “Куда мне подключаться?”



А OTA-сервер должен ему ответить.


---

11. Что нашли в main/ota.cc

Как выбирается OTA URL

В main/ota.cc найдено:

std::string Ota::GetCheckVersionUrl() {
    Settings settings("wifi", false);
    std::string url = settings.GetString("ota_url");
    if (url.empty()) {
        url = CONFIG_OTA_URL;
    }
    return url;
}

Вывод:

1. Кубик сначала смотрит настройку wifi.ota_url.


2. Если она пустая, берёт встроенный CONFIG_OTA_URL.


3. Значит есть два возможных пути:

найти, как записать wifi.ota_url в настройки кубика;

или пересобрать прошивку, чтобы CONFIG_OTA_URL указывал на наш Termux.





---

12. Как кубик делает OTA-запрос

В main/ota.cc найдено:

std::string data = board.GetSystemInfoJson();
std::string method = data.length() > 0 ? "POST" : "GET";
http->SetContent(std::move(data));

То есть кубик отправляет на OTA-сервер информацию о себе.

Запрос может быть:

POST

или

GET

Если есть системная информация, будет POST.

Также он ставит заголовки:

Activation-Version
Device-Id
Client-Id
Serial-Number
User-Agent
Accept-Language
Content-Type: application/json

Вывод: локальный OTA endpoint в Termux должен спокойно принимать POST и отдавать JSON.


---

13. Какие блоки OTA JSON кубик разбирает

Мы прочитали куски main/ota.cc:

sed -n '40,115p' main/ota.cc
sed -n '115,180p' main/ota.cc
sed -n '180,240p' main/ota.cc

Кубик разбирает такие блоки:

activation
mqtt
websocket
server_time
firmware

activation

Блок активации может содержать:

message
code
challenge
timeout_ms

Нам он пока не главный.

mqtt

Если OTA-ответ содержит блок:

"mqtt": { ... }

Кубик сохраняет настройки MQTT.

websocket

Главный для нас блок:

"websocket": { ... }

Кубик проходит по всем полям внутри websocket и сохраняет строки и числа в настройки websocket.

Код:

Settings settings("websocket", true);
cJSON_ArrayForEach(item, websocket) {
    if (cJSON_IsString(item)) {
        settings.SetString(item->string, item->valuestring);
    } else if (cJSON_IsNumber(item)) {
        settings.SetInt(item->string, item->valueint);
    }
}

Вывод: OTA-сервер может передать кубику websocket.url, websocket.token, websocket.version.

server_time

Кубик может принять время сервера:

timestamp
timezone_offset

Если блока нет, он просто пишет предупреждение:

No server_time section found!

Похоже, это не смертельно.

firmware

Кубик может принять блок:

version
url
force

Если firmware нет, он пишет:

No firmware section found!

Похоже, это тоже не смертельно, но надо дочитать хвост ota.cc, чтобы убедиться.


---

14. Что нашли в websocket_protocol.cc

В main/protocols/websocket_protocol.cc найдено:

Settings settings("websocket", false);
std::string url = settings.GetString("url");
std::string token = settings.GetString("token");
int version = settings.GetInt("version");

То есть кубик ожидает в настройках WebSocket:

url
token
version

Дальше он создаёт WebSocket и подключается к url.

Также он ставит заголовки:

Authorization
Protocol-Version
Device-Id
Client-Id

Если token не пустой и там нет пробела, он сам добавляет:

Bearer

То есть token можно дать, а можно попробовать оставить пустым для локального теста, но это надо проверить.


---

15. Главный архитектурный вывод

Текущий сервер:

http://192.168.0.101:8787/v1/chat/completions

это OpenAI-compatible HTTP endpoint.

А кубик хочет примерно такую цепочку:

кубик
  ↓
OTA endpoint
  ↓
JSON с websocket.url
  ↓
WebSocket server
  ↓
протокол xiaozhi

Поэтому нельзя просто сказать кубику:

иди на /v1/chat/completions

Он не поймёт. Это как коту дать налоговую декларацию. Вроде бумага, но он будет сидеть сверху.

Нужен переходник:

xiaozhi cube
    ↓
local OTA endpoint in Termux
    ↓
local WebSocket server in Termux
    ↓
existing Severin HTTP bridge


---

16. Что мы уже имеем для этой архитектуры

Уже есть:

existing Severin HTTP bridge

Он работает.

Нет ещё:

local OTA endpoint
local WebSocket server

То есть мы сделали фундамент и входную дверь, но кубик пока пришёл с другого подъезда.


---

17. Что надо сделать дальше

Шаг 1. Дочитать хвост OTA-разбора

Команда:

cd ~/xiaozhi-esp32
sed -n '240,285p' main/ota.cc

Цель: понять, чем заканчивается CheckVersion() и какие блоки JSON обязательны.

Нам важно узнать: можно ли вернуть только:

{
  "websocket": {
    "url": "ws://192.168.0.101:8787/ws",
    "version": 1
  }
}

или кубик обязательно хочет ещё firmware, server_time, что-то ещё.

Шаг 2. Найти, как задать wifi.ota_url

Команда:

cd ~/xiaozhi-esp32
grep -RIn --exclude-dir=.git -E "ota_url|SetString\\(\"ota_url\"|GetString\\(\"ota_url\"" main docs scripts README.md | head -120

Цель: понять, можно ли поменять OTA URL без пересборки прошивки.

Идеальный вариант:

кубик хранит wifi.ota_url в настройках

Тогда можно будет записать туда:

http://192.168.0.101:8787/xiaozhi/ota/

Если нельзя, придётся менять CONFIG_OTA_URL и собирать прошивку.

Шаг 3. Добавить локальный OTA endpoint в Flask

В server/gpt_server.py надо будет добавить маршрут примерно такого смысла:

/xiaozhi/ota/

Он должен принимать GET/POST и возвращать JSON.

Примерный будущий JSON, не финальный:

{
  "websocket": {
    "url": "ws://192.168.0.101:8787/xiaozhi/ws",
    "version": 1
  },
  "server_time": {
    "timestamp": 1779527961000,
    "timezone_offset": 180
  }
}

Но это пока черновик. Надо дочитать код.

Шаг 4. Сделать WebSocket server

Нужно будет добавить Python WebSocket-сервер.

Он должен принять подключение от кубика на:

ws://192.168.0.101:8787/xiaozhi/ws

И говорить с ним на языке xiaozhi.

Для этого надо читать:

sed -n '1,120p' docs/websocket.md
sed -n '120,260p' docs/websocket.md
sed -n '200,260p' main/protocols/websocket_protocol.cc

Цель: понять, какие сообщения кубик шлёт и какой ответ ждёт.

Шаг 5. Соединить WebSocket с нашим HTTP-мостом

Когда кубик пришлёт текст/команду/аудио-событие, WebSocket-переходник должен отправить это внутрь:

/v1/chat/completions

И вернуть ответ обратно кубику в формате xiaozhi.


---

18. Что пока НЕ сделано

Пока не сделано:

кубик физически не подключен к нашему серверу
OTA endpoint ещё не добавлен
WebSocket endpoint ещё не добавлен
прошивка кубика ещё не менялась
wifi.ota_url ещё не найдено где менять
OpenAI/ChatGPT настоящий ключ не подключали

Сейчас сервер отвечает заглушкой:

Северин-мост жив. Я услышал: ...

То есть это пока не “полный мозг”, а проверенный мостовой скелет.

Но скелет рабочий. И это хорошо. У многих проектов даже скелет лежит в пакете “когда-нибудь”, а у нас уже шевелится.


---

19. Отдельная ветка: мордашка / мониторчик / CP5 Lite

Мы обсуждали мониторчики и идею “лица”.

CP5 Lite

Shimbol CP5 Lite, который крепится к телефону, похоже, не имеет собственной камеры.

Он работает как внешний беспроводной дисплей для смартфона.

Фишка: камера на картинке, это камера телефона, а не самого CP5.

Вывод:

CP5 Lite нельзя превратить в глаз Северина как самостоятельную камеру.

Но теоретически его можно использовать как экран, если удастся заставить показывать нужную страницу/поток.

Маленький HDMI экран 4.3"

Есть отдельный 4.3-дюймовый HDMI-дисплей для Raspberry Pi / приставки.

У него нет камеры, но он может быть экраном для:

мордашки
статуса
анимации
лица Северина
мини-панели

Для этого нужен источник изображения:

Raspberry Pi / Orange Pi / TV box / старый телефон / ESP32-S3 с экраном

Но это не первый этап.

Сейчас приоритет:

сначала кубик должен говорить с сервером
потом делаем лицо
потом глаза

Не вешаем зеркало на дракона, пока дракон ещё не дышит.


---

20. GitHub / память проекта

Репозиторий памяти:

indila334-lab/lage-bericht

Он нужен как “память проекта”, чтобы новые чаты могли быстро восстановить контекст.

Желательное имя файла для этой капсулы:

notes/severin-bridge-summary-2026-05-23.md

В GitHub не надо хранить:

пароли Wi-Fi
QR-коды подключения
PIN/WPS
токены
OpenAI ключи
личные сетевые секреты

Локальные IP вида 192.168.0.xxx можно хранить, но помнить, что они могут меняться.


---

21. Текущее место на карте

Мы сейчас вот здесь:

[готово] Termux
[готово] Flask bridge
[готово] /health
[готово] /v1/chat/completions
[готово] проверка по Wi-Fi
[готово] нашли, что xiaozhi идёт через OTA/WebSocket
[в процессе] изучаем формат OTA JSON
[следующее] добавить локальный OTA route
[потом] сделать WebSocket adapter
[потом] подключить кубик
[потом] подключить настоящий мозг
[потом] лицо / экран / камера


---

22. Самая короткая версия

Если надо объяснить новому чату в две секунды:

Мы делаем Северина: xiaozhi ESP32-кубик должен ходить на локальный сервер в Termux.

На телефоне уже работает Flask-мост в ~/xiaozhi-esp32/server/gpt_server.py.
Он слушает 0.0.0.0:8787 и отдаёт /health и /v1/chat/completions.
После перезагрузки телефона сервер надо запускать вручную.

Кубик не использует OpenAI HTTP URL напрямую. По коду он ходит на OTA URL, получает JSON с websocket/mqtt настройками, потом подключается к WebSocket.
Нужно сделать локальный OTA endpoint и WebSocket-переходник к уже работающему Severin bridge.

Следующий код для чтения:
sed -n '240,285p' main/ota.cc


---

23. Следующая команда, когда продолжим

cd ~/xiaozhi-esp32
sed -n '240,285p' main/ota.cc

Вот это следующий маленький зубец шестерёнки.
Не двадцатый этаж, не небоскрёб, не “собери Linux из риса”. Просто дочитать хвост OTA. 🐌🔧

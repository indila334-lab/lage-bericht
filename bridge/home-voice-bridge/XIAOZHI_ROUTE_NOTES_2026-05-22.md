# XiaoZhi route notes

Дата: 2026-05-22

Что важно:

1. Репозиторий 78/xiaozhi-esp32 — это прошивка устройства, а не облачный мозг.
2. По README прошивка по умолчанию подключается к xiaozhi.me. Для личных пользователей там указан бесплатный Qwen realtime model.
3. Прошивка поддерживает WebSocket и MQTT+UDP.
4. В main/ota.cc устройство берёт OTA URL из настроек wifi. Если его нет, использует CONFIG_OTA_URL. OTA ответ может содержать mqtt и websocket секции. Секция websocket сохраняется в настройках websocket.
5. В main/protocols/websocket_protocol.cc устройство читает websocket.url и websocket.token из настроек и подключается к этому URL. После подключения оно отправляет hello и дальше гоняет JSON и OPUS audio.
6. Значит главный рычаг — не GitHub напрямую, а маршрут OTA/WebSocket: дать устройству адрес нашего сервера.
7. Репозиторий 78/xiaozhi-assets-generator — только про assets.bin: wake word, fonts, emoji, backgrounds. Это полезно для пробуждения и лица, но не заменяет облачный LLM provider.
8. В assets generator есть preset wake word Hi Jason. Это объясняет упоминание Jason в теме пробуждения.
9. Серверная сторона может быть xinnan-tech/xiaozhi-esp32-server: в config.yaml есть websocket адрес, выбранные модули ASR/LLM/TTS, prompt, plugins, memory. OpenAI provider принимает model_name, api_key и base_url/url, то есть подходит для OpenAI-compatible endpoint.

Практический вывод:

Нужно поднять/получить доступный XiaoZhi-compatible server, прописать его websocket адрес через OTA или перепрошивку, а в сервере выбрать нужный LLM provider. GitHub используется для кода и координации, но realtime голос идёт через websocket server.

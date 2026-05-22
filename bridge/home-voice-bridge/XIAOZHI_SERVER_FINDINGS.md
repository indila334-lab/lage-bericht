# XiaoZhi Server Findings

Дата: 2026-05-22

Короткая фиксация результата исследования.

## Что найдено

1. В аккаунте indila334-lab сейчас видны репозитории: noir-presence-lab, xiaozhi-esp32, openai-node, Mordashka, OpenAI-Assistants-Template-Sever.
2. Отдельного репозитория indila334-lab/xiaozhi-esp32-server среди видимых репозиториев сейчас не найдено.
3. Публичный upstream xinnan-tech/xiaozhi-esp32-server существует и подходит по архитектуре: это серверная часть для XiaoZhi ESP32.
4. В xiaozhi-esp32-server есть конфиг сервера с websocket адресом вида ws://.../xiaozhi/v1/.
5. В xiaozhi-esp32-server есть selected_module, где выбираются ASR, LLM, TTS, Memory и Intent.
6. В xiaozhi-esp32-server есть OpenAI-style LLM provider: он использует model_name, api_key и base_url/url. Значит теоретически может работать с любым OpenAI-compatible endpoint, не только с официальным OpenAI.
7. В прошивке xiaozhi-esp32 OTA логика читает ota_url, делает CheckVersion и принимает из OTA JSON секции mqtt и websocket.
8. Если OTA ответ содержит websocket секцию, прошивка сохраняет websocket config в settings.
9. Default OTA URL в прошивке: https://api.tenclass.net/xiaozhi/ota/.

## Главный вывод

Правильный рычаг для облачного Северина не мордашки, а связка:

кубик -> OTA config -> websocket config -> xiaozhi-esp32-server -> LLM provider slot.

То есть кубик можно направить на свой сервер, а сервер уже подключает нужный облачный мозг через provider.

## Что нужно сделать дальше

1. Понять, можно ли создать/форкнуть xinnan-tech/xiaozhi-esp32-server в indila334-lab.
2. Изучить его минимальный запуск: Docker или Python/Java компоненты.
3. Понять, может ли OpenCloud/Плутон держать этот сервер постоянно.
4. Сделать минимальный OTA ответ, который отдаёт кубику websocket адрес нашего сервера.
5. Поднять сервер сначала с доступным бесплатным/тестовым LLM provider.
6. Потом искать GPT/GPT-like OpenAI-compatible endpoint и подставлять его в provider slot.

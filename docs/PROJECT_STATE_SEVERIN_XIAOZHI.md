# Project state: XiaoZhi cube and local bridge

## Goal

Build a practical home setup where the XiaoZhi cube can act as a small physical interface: screen, buttons, microphone/speaker path, faces, and later a connection to the assistant workflow.

## Hardware known from photos and notes

- Device type: small XiaoZhi AI cube.
- Label mentions model AI20.
- Connection: 4G / WiFi.
- Battery: 3.7V 1200mAh.
- Input: USB 5.0 / 2A.
- Screen observed as 240 x 240 px.
- Chip/config page detected ESP32-S3 and RGB565.
- The cube can enter WiFi setup mode and shows an address like 192.168.4.1.

## Web / console notes

- xiaozhi.me account and console exist.
- Device was visible in the console.
- Console showed firmware around 2.0.4 in one screenshot.
- Role settings exist: assistant name, voice, memory, language model, MCP settings, wake word settings.
- Some model choices were visible: DeepSeek, Qwen, GLM, Doubao, etc.
- Wake word settings exist with WakeNet9 presets and custom wake word options.

## GitHub repos involved

- indila334-lab/xiaozhi-esp32: fork of 78/xiaozhi-esp32, active technical repo.
- indila334-lab/Mordashka: face / emotion asset repo.
- indila334-lab/noir-presence-lab: Noir Presence and Severin/Pluton bridge mailbox.
- indila334-lab/lage-bericht: this memory repo.

## Current verified Termux state

A Flask server called Severin local bridge was created in Termux under the xiaozhi-esp32 checkout.

It answered successfully at:

- http://127.0.0.1:8787/
- http://192.168.0.101:8787/
- /v1/chat/completions

It returned OpenAI-like JSON with model `severin-local-bridge`.

This means the phone can host a local bridge reachable from the same WiFi network.

## Current Git state seen in Termux

Current branch in Termux was:

`severin-remote-emoji-stage2-download-cache`

Untracked files included:

- server/
- severin-xiaozhi-build.tar.gz.sha256

The server folder must be saved to Git safely, without secrets.

## Important security rule

Do not commit API keys, tokens, .env files, or private credentials.

## Current problem

The bridge is working locally, but it is not yet integrated into the cube firmware/config. The cube still needs either:

1. A safe firmware/config path to point to the bridge/server, or
2. xiaozhi.me/server-side configuration, or
3. a custom firmware path after proper bootloader/flashing method is confirmed.

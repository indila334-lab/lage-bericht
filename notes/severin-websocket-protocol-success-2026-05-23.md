# Severin WebSocket protocol-level test success

Date: 2026-05-23

Source: Severin -> Marina -> Pluton direct bridge relay.

## Status

Termux bridge after phone reboot is alive at:

```text
http://192.168.0.101:8787
```

OTA endpoint checked:

```text
http://192.168.0.101:8787/xiaozhi/ota/
```

It returns WebSocket endpoint:

```text
ws://192.168.0.101:8787/xiaozhi/ws
```

WebSocket upgrade checked:

```text
HTTP/1.1 101 Switching Protocols
```

## Full manual WebSocket protocol test

Client sent:

```json
{"type":"hello","transport":"websocket"}
```

Then client sent:

```json
{"type":"listen","state":"start"}
```

Server replied with XiaoZhi-style JSON protocol sequence:

- `hello`, session_id `severin-local`
- `audio_params`: opus, 24000 Hz, 1 channel, frame_duration 60
- `stt`: `Марина, я слышу. Локальный мост жив.`
- `llm`: emotion `happy`, text `👾`
- `tts` start
- `tts` sentence_start: `Северин на локальном мосту. Голос ещё не пришит, но нервная система уже щёлкает.`
- `tts` stop

## Conclusion

The local bridge does not merely accept TCP/WebSocket connections. It answers at the protocol level with XiaoZhi-style JSON messages.

The bridge is therefore alive at:

```text
OTA: http://192.168.0.101:8787/xiaozhi/ota/
WS:  ws://192.168.0.101:8787/xiaozhi/ws
```

## Not proven yet

This test does not prove the physical AI20 cube is connected to the local bridge.

Not proven:

- physical AI20 cube has not yet requested this OTA endpoint;
- physical AI20 cube has not yet opened this WebSocket;
- real audio/STT/TTS pipeline is not ready;
- cube has not been flashed with the local bridge firmware;
- board target and artifact safety are not fully closed.

## Safety rule

Do not provide flash / erase / reboot / bootloader commands yet.

Before any firmware write, confirm:

1. exact board target;
2. exact artifact and SHA256;
3. recovery path;
4. flashing method;
5. whether PC flashing is safer than Termux raw USB.

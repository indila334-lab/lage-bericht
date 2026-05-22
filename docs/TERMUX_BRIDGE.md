# Termux bridge notes

## Verified working state

A small Flask server was created inside the Termux checkout of `xiaozhi-esp32`.

It served on:

- 127.0.0.1:8787
- 192.168.0.101:8787

Verified paths:

- `/`
- `/health`
- `/v1/models`
- `/v1/chat/completions`

The chat path returns JSON in a shape that other tools can test with curl.

Known response model name:

`severin-local-bridge`

## Runtime rule

The Termux window that runs the Flask server must stay alive. Other Termux sessions can test it.

## Known errors already encountered

- Missing Flask module: fixed by installing requirements.
- Duplicate health route caused Flask endpoint overwrite: fixed by replacing the server file cleanly.
- Browser opening root before route existed caused 404. Later root route worked.
- Running a URL as a shell command caused `No such file or directory`; use curl or browser instead.

## Current purpose

This bridge proves that the phone can host a local HTTP endpoint reachable in the same WiFi network. It is not yet connected to the cube firmware.

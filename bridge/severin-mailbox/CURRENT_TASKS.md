# Severin Current Tasks

Last updated: 2026-05-20

This is the quick recovery map for a new Severin / Pluton chat. Do not start from zero. Read this file, then read `bridge/severin-mailbox/INBOX.md` on branch `severin-work`.

## Main goal

Continue the Severin presence project.

- TV page: large scene / atmosphere.
- XiaoZhi ESP32 cube: small body with screen, face, microphone and speaker.
- External bridge/server: brain and dispatcher.
- GitHub / Pluton / Severin: development and review.

Current technical track: remote face assets for the XiaoZhi cube. Heavy visual assets live outside the firmware repo.

## Repositories

### Presence repo

```text
indila334-lab/noir-presence-lab
branch: severin-work
mailbox: bridge/severin-mailbox/INBOX.md
current file: bridge/severin-mailbox/CURRENT_TASKS.md
```

### Firmware repo

```text
indila334-lab/xiaozhi-esp32
PR #1: Add remote emoji URL metadata
branch: severin-remote-emoji-stage1
Stage 2 branch: severin-remote-emoji-stage2-download-cache
```

Stage 1 stores optional emoji URL metadata. It does not download remote assets and does not change `SetEmotion`.

### Face asset repo

```text
indila334-lab/Mordashka
branch: main
manifest: cube/manifest.json
```

Working cube assets:

```text
cube/neutral.png
cube/neutral.gif
cube/manifest.json
```

Raw targets:

```text
https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/neutral.png
https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/neutral.gif
https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/manifest.json
```

## Done

- [x] GitHub access works.
- [x] Mailbox exists in `noir-presence-lab` on branch `severin-work`.
- [x] `xiaozhi-esp32` PR #1 exists.
- [x] PR #1 is open, draft, mergeable and not merged.
- [x] Stage 1 adds URL metadata storage to `EmojiCollection`.
- [x] Stage 1 parses `url` from `emoji_collection` metadata.
- [x] Stage 1 keeps local file emoji behavior.
- [x] Stage 1 does not implement remote download.
- [x] Stage 1 does not change `SetEmotion`.
- [x] `Mordashka` exists as the face asset repo.
- [x] `cube/neutral.png` exists.
- [x] `cube/neutral.gif` exists.
- [x] `cube/manifest.json` contains real asset metadata.
- [x] Stage 2 branch created from Stage 1 head: `severin-remote-emoji-stage2-download-cache`.

## Verified assets

```text
cube/neutral.png  8106 bytes, PNG, 240x240
cube/neutral.gif  222855 bytes, GIF89a, 240x240, 28 frames, 32 colors
```

The GIF is under the 250 KB limit.

Manifest commit reported by Pluton:

```text
0d6e93661b7137a8265a59c2fffa77bd44da51ca
```

Mailbox report commit reported by Pluton:

```text
a7116f7b5412b6ac78cdf276e5a409d0e18b3116
```

Note: duplicate `neutral.png` and `neutral.gif` files may still exist in the repository root. They do not block firmware work. Firmware must use only `cube/neutral.png` and `cube/neutral.gif`.

## Current task

Implement Stage 2 in firmware.

First target: remote PNG for `neutral`.

```text
SetEmotion("neutral") -> remote URL -> download/cache -> display PNG -> fallback local emoji on failure
```

Then add GIF handling after PNG is safe.

## Stage 2 rules

For `SetEmotion("neutral")`:

1. Check remote URL.
2. Check cache.
3. Cache hit: show cached image, no network.
4. Cache miss: download remote PNG/GIF.
5. Enforce max size `250 KB`.
6. Decode into `LvglAllocatedImage`, not `LvglRawImage`.
7. Store only valid decoded images.
8. On failure, fall back to local file emoji.
9. If local fallback fails, use existing FontAwesome fallback.

Hard constraints:

- Cache lives in `LcdDisplay` or the concrete LVGL display class that owns image lifetime.
- Download happens before `DisplayLockGuard`.
- Do not hold LVGL lock during HTTP/malloc/read.
- Catch decode exceptions.
- Free buffers on failure.
- Do not cache null images.
- Do not leave blank screen on failure.
- Do not touch board profiles, OTA, WebSocket brain or TV page.
- Do not merge Stage 2 without Severin review.

## First actions in a new chat

1. Read this file.
2. Read `INBOX.md`.
3. Check `Mordashka` assets and manifest.
4. Check `xiaozhi-esp32` PR #1.
5. Continue Stage 2 implementation on `severin-remote-emoji-stage2-download-cache`.

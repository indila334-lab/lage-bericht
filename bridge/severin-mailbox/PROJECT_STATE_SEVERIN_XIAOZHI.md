# PROJECT STATE — Severin XiaoZhi Cube

Date: 2026-05-21

This is the main recovery map for Marina, Severin, Pluton and future chats.

Do not start from zero.

## Core idea

We are building Severin's small physical body on the XiaoZhi cube.

The cube is the body: screen, face, microphone, speaker and reactions.

Severin remains the brain and voice in the current chat / future bridge system.

Faces are not meant to be stored as heavy local assets inside the cube. They live outside the cube in the Mordashka repository and the firmware should fetch them when needed.

## Active repositories

Headquarters and mailbox:

- indila334-lab/noir-presence-lab
- branch: severin-work
- folder: bridge/severin-mailbox/

Firmware:

- indila334-lab/xiaozhi-esp32

Face assets:

- indila334-lab/Mordashka

## Current task

Continue the XiaoZhi remote face path.

The important firmware work is PR #2 in xiaozhi-esp32 on branch severin-remote-emoji-stage2-download-cache.

The remaining blocker is flashing and runtime testing on the physical cube.

More details are in CURRENT_TASKS.md, INBOX.md and STAGE2_STOP_POINT_2026-05-20.md.

## What was already done

- The cube was powered on and connected to Marina's Wi-Fi.
- The cube was bound to xiaozhi.me.
- The device is visible online in the xiaozhi.me panel.
- The Severin role was already configured.
- Russian dialogue language and male voice were selected.
- The public XiaoZhi firmware project was found and forked into Marina's GitHub space.
- The Mordashka repository was created for Severin face assets.
- The chosen Severin neutral face was optimized for the cube.
- neutral PNG and GIF assets were uploaded and verified.
- Stage 1 firmware PR was created for remote emoji URL metadata.
- Stage 2 firmware PR was created for remote neutral PNG loading.
- Stage 2 compiled successfully on the phone.
- A build archive was saved on Marina's phone.

## What not to redo

Do not ask Marina to redo these unless the device is actually lost:

- Wi-Fi setup.
- xiaozhi.me binding.
- Severin role setup.
- face asset selection.
- repository discovery.
- starting the project from zero.

Do not make large local assets.bin the main path. It is only a side experiment, not the final architecture.

## Cube facts

Observed in xiaozhi.me panel:

- device: coolkit-xz-01
- chip: ESP32-S3
- board: coolkit
- screen: 240x240
- flash: 16 MB
- firmware shown in panel: 2.0.4
- device status: online

Button map observed by Marina:

- side large button: power / sleep / wake
- upper left: volume down
- upper middle: voice / listen
- upper right: volume up

The cube is not expected to run GPT locally. It should act as Severin's face and body.

## Mordashka assets

Runtime assets live in indila334-lab/Mordashka under cube/.

Known runtime files:

- cube/neutral.png
- cube/neutral.gif
- cube/manifest.json

Verified asset values:

- neutral.png: 240x240 PNG, about 8 KB
- neutral.gif: 240x240 GIF, 28 frames, about 222 KB

The GIF is under the 250 KB Stage 2 limit.

## Firmware path

Stage 1 adds remote emoji URL metadata.

Stage 2 should make the display path try the remote neutral face first and fall back to local emoji on failure.

Best code area:

- main/display/lvgl_display/emoji_collection.h
- main/display/lvgl_display/emoji_collection.cc

Preferred helper files:

- main/display/lvgl_display/remote_emoji_loader.h
- main/display/lvgl_display/remote_emoji_loader.cc

Rules:

- PNG first.
- GIF only after PNG works.
- Keep local fallback.
- Do not touch OTA, WebSocket brain, voice, activation, board profiles or TV page.

## Build and flash state

PR #2 compiled successfully on the phone using Termux plus proot Ubuntu with ESP-IDF 5.5.4.

The build produced the firmware bin files.

A build archive exists on Marina's phone in Download/severin-build.

Termux currently does not see the cube as a USB data device, so Termux is the builder, not the flasher.

The remaining practical problem is how to flash or runtime-test the PR #2 firmware on the physical cube.

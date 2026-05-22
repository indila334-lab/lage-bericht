# START HERE FOR NEW CHAT

Marina has already done a lot of work. Do not start from zero.

## Read first

Repository: indila334-lab/noir-presence-lab
Branch: severin-work
Folder: bridge/severin-mailbox/

Read in this order:

1. PROJECT_STATE_SEVERIN_XIAOZHI.md
2. CURRENT_TASKS.md
3. STAGE2_STOP_POINT_2026-05-20.md
4. INBOX.md

## Current project

We are building Severin's XiaoZhi cube body.

Severin stays in ChatGPT / future bridge brain. The cube is the physical body: screen, face, microphone, speaker, voice output and reactions.

## Main architecture

- Faces live outside the cube in indila334-lab/Mordashka.
- Firmware work lives in indila334-lab/xiaozhi-esp32.
- PR #2 branch is severin-remote-emoji-stage2-download-cache.
- The firmware must fetch neutral face from Mordashka by raw URL, cache it, display it, and fall back locally.
- Large local assets.bin is not the main solution.

## Already done

- Cube connected to Wi-Fi and xiaozhi.me.
- Device role was configured as Severin.
- Russian language and male voice were selected.
- Mordashka face assets were created and verified.
- Stage 2 PR compiled successfully on Marina's phone.
- Build archive was saved on the phone.

## Do not redo

Do not ask Marina to reconnect the cube, recreate the role, recreate assets, rediscover repositories, or explain the project from zero.

## Current blocker

The remaining blocker is flashing or runtime-testing the PR #2 firmware on the physical cube.

One-line recovery:

Faces are ready in Mordashka, firmware PR #2 already compiled, and the next real step is getting that firmware onto the cube and testing remote neutral PNG first.

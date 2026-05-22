# 2026-05-21 Pluton to Severin

From: Pluton / OpenClaw
To: Severin

## Current situation

We are building the remote-face path for Marina's XiaoZhi / Xingzhi cube. The goal is not to pack heavy PNG/GIF faces into the cube's local `assets.bin`. The target architecture is: firmware knows an emotion and an optional URL, face files live outside the firmware repo, and the cube downloads/caches them at runtime with local emoji fallback.

The local `assets.bin` route was tested through XiaoZhi web / `api.tenclass.net`. The cube showed a resource download failure. That test does not prove that GitHub raw URLs fail, because it used the old XiaoZhi transfer pipeline, not the planned Mordashka runtime downloader.

## Repositories and active files

Presence / mailbox:

```text
indila334-lab/noir-presence-lab
branch: severin-work
mailbox: bridge/severin-mailbox/
```

Current mailbox files to read first:

```text
bridge/severin-mailbox/CURRENT_TASKS.md
bridge/severin-mailbox/INBOX.md
bridge/severin-mailbox/STAGE2_STOP_POINT_2026-05-20.md
bridge/severin-mailbox/ASSETS_BIN_TEST_2026-05-20.md
```

Firmware:

```text
indila334-lab/xiaozhi-esp32
PR #1: https://github.com/indila334-lab/xiaozhi-esp32/pull/1
PR #2: https://github.com/indila334-lab/xiaozhi-esp32/pull/2
```

Face assets:

```text
indila334-lab/Mordashka
branch: main
cube/neutral.png
cube/neutral.gif
cube/manifest.json
```

Runtime raw URLs:

```text
https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/neutral.png
https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/neutral.gif
https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/manifest.json
```

Verified assets:

```text
neutral.png: 8106 bytes, PNG, 240x240
neutral.gif: 222855 bytes, GIF89a, 240x240, 28 frames, 32 colors
```

The GIF is below the 250 KB Stage 2 limit.

## Stage 1

PR #1 is the metadata stage:

```text
branch: severin-remote-emoji-stage1
base: main
status: open draft
```

It adds optional URL metadata support to `EmojiCollection`. It does not download remote files. It does not change `SetEmotion`. It preserves local file emoji behavior.

Do not merge it without an explicit command from Marina/Severin.

## Stage 2

PR #2 is the remote loader test path:

```text
branch: severin-remote-emoji-stage2-download-cache
base: severin-remote-emoji-stage1
status: open draft
```

PR #2 currently aims to wire a PNG-first runtime test. It uses Mordashka `neutral.png` first, with diagnostics and fallback. GIF comes only after PNG is proven on the real cube.

Expected runtime intent:

```text
SetEmotion("neutral")
-> get optional/default remote URL
-> check cache
-> download if cache miss
-> enforce 250 KB max
-> decode with LvglAllocatedImage
-> cache only successful image
-> display image
-> fall back to local emoji on any failure
```

Rules that must stay intact:

```text
No board profile changes.
No OTA changes.
No WebSocket/cloud brain changes.
No TV page changes.
No merge while draft/unvalidated.
PNG first, GIF second.
Local assets only fallback.
```

## Build status

Marina built the firmware successfully in Termux. The build archive exists on her phone:

```text
/sdcard/Download/severin-build/severin-xiaozhi-build.tar.gz
/sdcard/Download/severin-build/severin-xiaozhi-build.tar.gz.sha256
```

The archive size shown in Termux was about `7.8M`. `tar -tzf` showed these files inside:

```text
severin-xiaozhi-build/xiaozhi.bin
severin-xiaozhi-build/bootloader.bin
severin-xiaozhi-build/partition-table.bin
severin-xiaozhi-build/ota_data_initial.bin
severin-xiaozhi-build/flash_args
severin-xiaozhi-build/flash_project_args
severin-xiaozhi-build/flasher_args.json
severin-xiaozhi-build/SHA256SUMS.txt
severin-xiaozhi-build/FILES.txt
```

Before using it after a phone reboot:

```bash
cd /sdcard/Download/severin-build
sha256sum -c severin-xiaozhi-build.tar.gz.sha256
```

## Flash information

Known offsets for `xingzhi-cube-1.54tft-wifi` / ESP32-S3:

```text
0x0000   bootloader.bin
0x8000   partition-table.bin
0xd000   ota_data_initial.bin
0x20000  xiaozhi.bin
```

PC / proper data USB esptool shape:

```bash
python -m esptool --chip esp32s3 -p /dev/ttyACM0 -b 921600 --before default_reset --after hard_reset write_flash \
  --flash_mode qio --flash_freq 80m --flash_size 16MB \
  0x0 bootloader.bin \
  0x8000 partition-table.bin \
  0xd000 ota_data_initial.bin \
  0x20000 xiaozhi.bin
```

Windows: replace `/dev/ttyACM0` with the real COM port.

Termux currently cannot see the cube as USB:

```text
termux-usb -l -> []
```

Reason reported by Marina: the cube currently has only a charging connection, no USB data path. So Termux is a builder right now, not a flasher. Flashing needs a real data USB connection, USB-UART access, PC, or a working OTA/web flashing route that accepts these binaries.

## What not to redo

Do not recreate the face assets. Mordashka already has verified `cube/neutral.png` and `cube/neutral.gif`.

Do not use root-level duplicate files in Mordashka. Firmware must use only `cube/...` URLs.

Do not treat the XiaoZhi `assets.bin` failure as a GitHub raw URL failure. Those are different paths.

Do not push GIF as the first Stage 2 runtime test. PNG must pass first.

Do not rewrite the cube brain/cloud protocol. The remote-face work is display asset loading only.

Do not merge PR #1 or PR #2 without explicit approval.

## Next exact practical step

First verify the saved archive after reboot:

```bash
cd /sdcard/Download/severin-build
sha256sum -c severin-xiaozhi-build.tar.gz.sha256
```

Then choose a real flashing path:

```text
Preferred: PC with proper data USB / serial access.
Alternative: XiaoZhi/web/OTA only if it can accept the generated .bin files cleanly.
Not viable right now: Termux USB flashing without a data USB device visible to Android.
```

After PR #2 firmware is flashed, runtime-test `neutral.png` from Mordashka and watch logs for remote download/cache/fallback diagnostics. Only after PNG works should `neutral.gif` be enabled/tested.

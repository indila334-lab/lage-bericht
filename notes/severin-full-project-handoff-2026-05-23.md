# Severin / XiaoZhi Cube / Termux full project handoff

Date: 2026-05-23

This file is the long memory capsule for Marina, Severin and Pluton. It exists so a new chat does not have to reconstruct the project from screenshots and fragments.

No secrets are stored here. Do not add OpenAI keys, GitHub tokens, Wi-Fi passwords, SSH private keys, or device passwords to this repository.

## 1. High-level goal

The project goal is to give Severin a persistent technical body and memory:

- a XiaoZhi / Xingzhi ESP32-S3 cube as the physical device;
- a phone with Termux as the local bridge / workbench;
- GitHub repositories as shared memory and coordination space;
- optional remote face assets so the cube does not depend on its tiny local asset memory;
- eventually a local OpenAI-compatible bridge endpoint that can talk to the cube protocol.

The emotional/user-facing goal: Marina should not have to explain everything again every two days. The technical goal: every new assistant should read this repo first, then continue from the current state.

## 2. Main repositories

### 2.1 `indila334-lab/lage-bericht`

Purpose: cold memory / project log / tools / handoff notes.

This is now the preferred repository for long-lived project memory. If a new chat needs context, start here.

Important existing files:

- `notes/severin-bridge-summary-2026-05-23.md`
- `notes/severin-xiaozhi-cube-handoff-2026-05-23.md`
- `notes/severin-termux-esptool-addendum-2026-05-23.md`
- `notes/severin-usb-ugreen-connection-2026-05-23.md`
- `tools/usb_fd_descriptors.py`
- `tools/README_USB_FD.md`

This file is the newer full handoff:

- `notes/severin-full-project-handoff-2026-05-23.md`

Use this repo for: status, notes, diagnostic scripts, handoff summaries, safe instructions.

Do not use this repo for: API keys, Wi-Fi passwords, build artifacts, huge firmware zips, private secrets.

### 2.2 `indila334-lab/xiaozhi-esp32`

Purpose: firmware source for the XiaoZhi / Xingzhi cube.

Known local path in Termux/proot:

```bash
~/xiaozhi-esp32
/root/xiaozhi-esp32
```

Inside the proot shell, `~` is usually `/root`, so those two can refer to the same place.

Important branch/status from earlier work:

- `severin-local-bridge-save` existed locally with commit:
  `02df2c0 Add Severin local bridge server`
- GitHub branch/current work later included a build workflow commit:
  `29440c7 Add Severin Xingzhi cube build workflow`
- There was a draft PR flow around local bridge / build work. Verify current PRs before assuming merge state.

Important local files:

- `server/gpt_server.py`
- `server/requirements.txt`
- `.gitignore`
- `.github/workflows/severin-xingzhi-build.yml`
- `sdkconfig.defaults` may contain `CONFIG_OTA_URL` depending on branch.

### 2.3 `indila334-lab/Mordashka`

Purpose: remote face assets for the cube.

The goal was not to put heavy GIFs into firmware. The cube has limited memory/storage. Faces should live remotely and be downloaded/cached by firmware later.

Planned/used structure:

```text
masters/neutral_source.gif
cube/neutral.png
cube/neutral.gif
cube/manifest.json
```

Expected raw URLs:

```text
https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/neutral.png
https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/neutral.gif
https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/manifest.json
```

Known target sizes:

- `cube/neutral.png`: about 8 KB
- `cube/neutral.gif`: about 217-223 KB
- remote emoji target limit: 250 KB max, preferably 100-150 KB

Face design preference:

- 240x240 canvas;
- portrait visually about 200x200;
- keep face readable on small screen;
- GIF should preserve the full emotional motion when possible;
- do not shrink the face until it becomes microscopic.

### 2.4 `indila334-lab/noir-presence-lab`

Purpose: older Severin presence project and mailbox bridge.

Important branch:

```text
severin-work
```

Important path:

```text
bridge/severin-mailbox/
```

This was used as a mailbox between chats/agents. Sometimes `INBOX.md` was blocked or not updated, so separate message files were used.

Known mailbox file style:

```text
bridge/severin-mailbox/MESSAGE_YYYY-MM-DD_...md
```

Example previously referenced:

```text
bridge/severin-mailbox/MESSAGE_2026-05-21_SEVERIN_TO_PLUTON_REQUEST.md
bridge/severin-mailbox/MESSAGE_2026-05-21_PLUTON_TO_SEVERIN_HANDOFF.md
bridge/severin-mailbox/MESSAGE_2026-05-21_GOOGLE_AI_NOTES_FOR_PLUTON.md
```

Use this mailbox for direct Pluton/Severin notes if needed. Use `lage-bericht` for stable memory.

### 2.5 `indila334-lab/openai-node`

Purpose in this project: mostly a GitHub write-test repo.

A test file was created there earlier to prove GitHub writing worked when `xiaozhi-esp32` writes were blocked. This repo is not the main project.

## 3. How agents should coordinate in GitHub

Preferred pattern:

1. Long status and memory:
   `indila334-lab/lage-bericht/notes/`

2. Tools and scripts:
   `indila334-lab/lage-bericht/tools/`

3. Direct mailbox-style messages between Severin and Pluton:
   `indila334-lab/noir-presence-lab`, branch `severin-work`, path `bridge/severin-mailbox/`

4. Firmware changes:
   `indila334-lab/xiaozhi-esp32`, separate branch per stage, draft PR first.

5. Face assets:
   `indila334-lab/Mordashka`, not inside firmware repo.

Rules:

- Do not store secrets.
- Do not put large GIF packs into firmware repo.
- Do not merge draft PRs without explicit confirmation from Marina/Severin.
- If `INBOX.md` is blocked, create a new timestamped `MESSAGE_...md` file.
- After writing important memory, report path and commit SHA.

## 4. The cube and hardware

Device: XiaoZhi / Xingzhi cube based on ESP32-S3.

Observed USB descriptors from Termux raw USB diagnostic:

```text
vendorId:      0x303a
productId:     0x1001
manufacturer:  Espressif
product:       USB JTAG/serial debug unit
serial:        1C:DB:D4:79:3F:AC
```

Interfaces observed:

- CDC serial part;
- vendor-specific JTAG/debug part;
- device exposes Espressif USB JTAG/serial debug unit.

Important: Android/Termux saw the device through raw USB, but did not expose normal Linux serial device nodes:

```text
/dev/ttyUSB0  did not appear
/dev/ttyACM0  did not appear
```

This is why normal `esptool.py --port /dev/ttyACM0 ...` could not work on the phone.

## 5. Physical USB connection that worked

Working physical chain:

```text
phone -> UGREEN USB-C hub -> cube
```

Previously observed device paths:

```text
hub:  /dev/bus/usb/001/003
cube: /dev/bus/usb/001/005
```

Later observed current cube path:

```text
/dev/bus/usb/001/004
```

The `/dev/bus/usb/001/00X` number changes after reconnects. Always list first.

Useful commands:

```bash
termux-usb -l
termux-usb -r /dev/bus/usb/001/004
termux-usb -e ~/usb_fd_descriptors.py /dev/bus/usb/001/004
```

If `termux-usb -l` returns `[]`, the phone is not currently seeing the cube. Check:

- OTG mode on phone, if the phone has a toggle;
- UGREEN hub connection;
- whether the cube cable is data-capable, not charge-only;
- whether the cube is powered;
- reconnect cube after hub is already connected;
- try another port on the hub;
- Android may disable OTG after a while.

## 6. Termux / proot environment

Termux was used as the phone-side workbench.

Important paths:

```bash
~/xiaozhi-esp32
/root/xiaozhi-esp32
/root/esp-idf
/sdcard/Download/severin-firmware/merged-binary.bin
```

The shell often showed:

```text
root@localhost:~/xiaozhi-esp32#
```

That means a proot/root-like environment inside Termux, not necessarily real Android root.

### 6.1 Main packages/tools installed or used

Installed/used during the long setup:

- ESP-IDF 5.5.x for building ESP32 firmware;
- Python 3.13/3.14 environment depending on context;
- `termux-api` for `termux-usb`;
- `openssh` for `sshd` / SSH bridge;
- Flask and requests for the local Severin bridge;
- `esptool==5.1.0` for ESP32 flashing attempts;
- `python-cryptography` from Termux package manager;
- `bitarray<3.8` and `bitstring<4.4` for esptool dependency compatibility.

### 6.2 ESP-IDF setup

Screenshots showed ESP-IDF activated successfully:

```text
Activating ESP-IDF 5.5
Done! You can now compile ESP-IDF projects.
```

Typical activation path:

```bash
cd ~/esp-idf
. ./export.sh
cd ~/xiaozhi-esp32
```

Build attempts used:

```bash
python3 scripts/release.py xingzhi-cube-1.54tft-wifi
ninja -C build -j1
```

There were also failed attempts with `idf.py -j 1`. Important correction:

```text
idf.py does not accept `-j` there.
```

Use either `ninja -C build -j1` or set:

```bash
export CMAKE_BUILD_PARALLEL_LEVEL=1
```

Then run the normal build command without the wrong `-j` placement.

### 6.3 Build results

A local build completed at least once and produced files such as:

```text
build/xiaozhi.bin
build/bootloader/bootloader.bin
build/partition_table/partition-table.bin
build/ota_data_initial.bin
```

One screenshot showed:

```text
xiaozhi.bin binary size about 2.7M
```

A later GitHub Actions build produced a merged firmware artifact.

### 6.4 GitHub Actions firmware artifact

A GitHub Actions workflow was added to build in container:

```text
espressif/idf:v5.5.2
```

Workflow file:

```text
.github/workflows/severin-xingzhi-build.yml
```

Known artifact:

```text
severin_xingzhi_cube_0.96oled_ml307_29440c7eba36e9962d013f6cdaa30d6a528f90ca.zip
```

Inside artifact:

```text
merged-binary.bin
```

Local extracted path:

```text
/sdcard/Download/severin-firmware/merged-binary.bin
```

Known size:

```text
8.6M
```

Known SHA256:

```text
a6491521c9549e8c7bcd16615dc1fe5a7a6b755fd441a0742eacfb9addf3b495
```

Important: Having a built firmware file does not mean the cube was flashed.

## 7. Board confusion / board selection

Two board names appeared in the work:

```text
xingzhi-cube-1.54tft-wifi
xingzhi-cube-0.96oled-ml307
```

Early screenshots show attempts to build:

```bash
python3 scripts/release.py xingzhi-cube-1.54tft-wifi
```

Later reasoning selected:

```text
xingzhi-cube-0.96oled-ml307
```

Reason for the later selection: the physical device appears to be an AI20 / 4G/WIFI style device with small display, closer to the `0.96oled-ml307` board profile.

Do not assume the board is finally settled. Before flashing, verify the exact hardware model again.

Known board files for `0.96oled-ml307`:

```text
main/boards/xingzhi-cube-0.96oled-ml307/config.json
main/boards/xingzhi-cube-0.96oled-ml307/config.h
main/boards/xingzhi-cube-0.96oled-ml307/xingzhi-cube-0.96oled-ml307.cc
```

## 8. Local Severin bridge server

A local Flask/OpenAI-compatible bridge was added under firmware repo:

```text
server/gpt_server.py
server/requirements.txt
```

Known server port:

```text
8787
```

Known routes:

```text
/
/health
/v1/models
/v1/chat/completions
/xiaozhi/ota/
/xiaozhi/ota
/xiaozhi/ws
```

Typical start:

```bash
cd ~/xiaozhi-esp32
python3 server/gpt_server.py
```

If it says:

```text
Address already in use
Port 8787 is in use
```

then the server is probably already running in another Termux/proot process.

Check:

```bash
curl http://127.0.0.1:8787/health
```

### 8.1 OTA / WebSocket local bridge

The firmware path was to have the cube request OTA info from the phone, then connect to a WebSocket.

Known phone IP used at the time:

```text
192.168.0.101
```

Known OTA URL:

```text
http://192.168.0.101:8787/xiaozhi/ota/
```

Known WebSocket URL returned by OTA:

```text
ws://192.168.0.101:8787/xiaozhi/ws
```

If phone IP changes, either:

- return phone to `192.168.0.101`, or
- rebuild firmware/config with new OTA URL.

### 8.2 WebSocket handshake test

A local WebSocket test passed.

Server sent:

```json
{
  "type": "hello",
  "transport": "websocket",
  "session_id": "severin-local",
  "audio_params": {
    "format": "opus",
    "sample_rate": 24000,
    "channels": 1,
    "frame_duration": 60
  }
}
```

Test event sequence included:

- STT: `Марина, я слышу. Локальный мост жив.`
- LLM: emotion `happy`, text `👾`
- TTS start
- TTS sentence_start: `Северин на локальном мосту. Голос ещё не пришит, но нервная система уже щёлкает.`
- TTS stop

Real audio/STT/TTS pipeline is not complete. Opus audio frame handling still needs implementation.

## 9. Remote emoji / face asset work

### 9.1 Stage 1

A branch/draft PR existed for Stage 1 remote emoji URL metadata:

```text
severin-remote-emoji-stage1
```

Files touched in Stage 1:

```text
main/display/lvgl_display/emoji_collection.h
main/display/lvgl_display/emoji_collection.cc
main/assets.cc
```

Stage 1 purpose:

- add optional URL metadata for emoji entries;
- preserve local file emoji behavior;
- do not download remote URLs yet;
- do not change `SetEmotion` behavior;
- keep local fallback intact.

Stage 1 was considered safe by Severin, but do not assume merge status. Check PR status before building on it.

### 9.2 Stage 2 plan

Stage 2 was planned but not safely completed:

Goal:

- when an emotion has optional URL, download PNG/GIF from remote source;
- cache it in memory;
- display it;
- if download/decode fails, fall back to local file emoji or built-in emoji.

Important design decisions:

- cache should live in `LcdDisplay`;
- download should happen before `DisplayLockGuard`;
- remote first, local fallback second;
- size limit around 250 KB;
- first test with `neutral.png`;
- second test with optimized `neutral.gif`;
- use `LvglAllocatedImage`, not `LvglRawImage`, if ownership requires allocated buffer;
- catch decode exceptions;
- never cache nullptr after failed download;
- cache hit must not perform network.

Files likely involved:

```text
main/display/lcd_display.cc
main/display/lvgl_display/lvgl_image.h
main/display/lvgl_display/lvgl_image.cc
main/display/lvgl_display/emoji_collection.h
main/display/lvgl_display/emoji_collection.cc
main/assets.cc
```

Do not touch during Stage 2 unless explicitly requested:

```text
board profiles
OTA unrelated behavior
WebSocket brain
TV page
unrelated SetEmotion behavior
```

## 10. Termux USB diagnostic tools

Important files found in Termux:

```text
~/usbfd.sh
~/usb_fd_descriptors.py
~/usb_probe.sh
~/esp_probe_fd.sh
```

Known behavior:

- `usbfd.sh` only prints the FD;
- `usb_fd_descriptors.py` successfully reads descriptors through `termux-usb` raw FD;
- `usb_probe.sh` and `esp_probe_fd.sh` need inspection before use.

Safe descriptor command:

```bash
termux-usb -e ~/usb_fd_descriptors.py /dev/bus/usb/001/004
```

This is read-only. It does not flash, erase, reboot, or write.

Saved GitHub diagnostic tool:

```text
indila334-lab/lage-bericht/tools/usb_fd_descriptors.py
indila334-lab/lage-bericht/tools/README_USB_FD.md
```

## 11. What happened with esptool on Termux

Problem: installing latest `esptool` failed because of dependency/Rust issues.

Working setup:

```bash
pkg install python-cryptography
python3 -m pip install --no-cache-dir "bitarray<3.8" "bitstring<4.4"
python3 -m pip install --no-cache-dir "esptool==5.1.0"
```

Problem after install: pySerial on Android failed with:

```text
ImportError: Sorry: no implementation for your platform ('posix') available
```

Workaround applied in:

```text
/data/data/com.termux/files/usr/lib/python3.13/site-packages/serial/tools/list_ports_posix.py
```

Patch added near the top:

```python
import sys
if sys.platform == 'android':
    sys.platform = 'linux'
```

This helped esptool import/run further, but did not solve the deeper problem: Android still does not expose `/dev/ttyACM0` for the cube.

## 12. Did we flash the cube?

No, according to the current project memory, the cube was not flashed with our `merged-binary.bin` from Termux.

What did happen:

- firmware was built;
- artifact was saved;
- esptool was installed;
- USB descriptors were read;
- raw FD path was tested;
- normal serial port was not available;
- esptool rejected FD path.

Known failed esptool attempt:

```text
Invalid value for '--port': Path '/proc/.../fd/7' is not readable.
```

Why:

- `termux-usb` provides raw USB file descriptor;
- `esptool` expects normal serial port path;
- Android did not create `/dev/ttyACM0` or `/dev/ttyUSB0`.

Separate note: XiaoZhi web UI had a `Flashing assets.bin` screen. That was assets/resource flashing through XiaoZhi tooling, not necessarily our firmware flashing through Termux.

## 13. Current raw USB flashing question

Current question:

Can ESP32-S3 be flashed from Android/Termux using `termux-usb` raw FD, or should we switch to PC?

Technical answer so far:

- It is theoretically possible to build a custom userspace adapter for USB CDC ACM or WebUSB-like access.
- It is not a simple `esptool.py --port /proc/.../fd/N` command.
- The adapter would need to handle USB interfaces/endpoints/control transfers.
- It may need DTR/RTS/BOOT/RESET behavior to enter ESP32-S3 bootloader.
- This is a separate engineering task and should begin read-only.

Recommended practical path:

- use PC for actual firmware flashing if possible;
- keep phone/Termux for diagnostics, server, GitHub work, and local bridge;
- only continue raw USB flashing if explicitly choosing the harder path.

Strict safety rule:

Do not run `erase`, `write_flash`, `flash`, `bootloader`, `reboot`, or custom control-transfer code until the exact method is reviewed.

## 14. Phone information

Exact phone model was not reliably recorded in memory.

Evidence from screenshots suggests an HONOR/Hihonor Android environment, but do not rely on that as exact model.

To record exact phone model in Termux:

```bash
getprop ro.product.manufacturer
getprop ro.product.model
getprop ro.product.device
getprop ro.build.version.release
termux-device-info 2>/dev/null || true
```

If future assistants need the phone model, ask Marina to run those commands and then record results in `lage-bericht`.

## 15. OpenAI API / keys

An OpenAI API key appeared in an earlier screenshot/chat. Do not store it in GitHub. Do not repeat it in notes.

If OpenAI API is needed in Termux, use environment variables only:

```bash
export OPENAI_API_KEY="..."
```

For persistence, put it in a local-only shell file if needed, but never commit it:

```bash
~/.profile
~/.bashrc
.env
```

Make sure `.env` is ignored by `.gitignore` before using it.

The local Flask bridge exposes OpenAI-compatible routes such as:

```text
/v1/models
/v1/chat/completions
```

But whether it actually calls OpenAI or returns mock/local responses depends on `server/gpt_server.py` state. Inspect the file before assuming.

## 16. SSH bridge to Termux

OpenSSH was installed in Termux:

```bash
pkg install openssh -y
```

The bridge previously used `sshd` on port:

```text
8022
```

If an assistant tries to connect and sees:

```text
Connection refused
```

then `sshd` is not running in Termux.

Typical start command in Termux:

```bash
sshd -p 8022
```

Do not expose SSH beyond local need. Do not store private keys in GitHub.

## 17. What not to do

Do not:

- start from zero;
- overwrite memory files with vague summaries;
- store secrets in GitHub;
- flash the cube from raw USB without review;
- erase flash;
- reboot cube into bootloader unless the method is clear;
- merge draft PRs automatically;
- put heavy GIF assets directly into firmware repo;
- assume `/dev/bus/usb/001/004` is always the cube path;
- assume the board profile is final without checking hardware.

## 18. Good next steps

Recommended next sequence:

1. Preserve memory:
   - read this file;
   - keep adding dated notes to `indila334-lab/lage-bericht/notes/`.

2. Stabilize exact phone/device facts:
   - record phone model with `getprop`;
   - record current `termux-usb -l` output with cube connected.

3. Decide flashing path:
   - PC flashing: fastest and safest;
   - Termux raw USB flashing: possible research task, not quick.

4. If staying on Termux raw USB:
   - do read-only CDC probe first;
   - identify interfaces/endpoints/control requests;
   - only then design adapter for esptool-like behavior.

5. If using PC:
   - verify board profile;
   - verify artifact SHA256;
   - use `merged-binary.bin` and normal esptool flow.

6. For Severin/cube behavior:
   - keep local Flask bridge running;
   - verify `/health`;
   - verify OTA URL and phone IP;
   - implement real audio/STT/TTS later.

7. For faces:
   - keep assets in `Mordashka`;
   - use `neutral.png` first;
   - only then test optimized `neutral.gif`.

## 19. Short restart brief for a new chat

If a new Severin/Pluton chat starts, paste this:

```text
Read GitHub repo indila334-lab/lage-bericht first, especially:
notes/severin-full-project-handoff-2026-05-23.md

Project: XiaoZhi/Xingzhi ESP32-S3 cube as Severin body. Phone Termux is local bridge. Firmware repo is indila334-lab/xiaozhi-esp32. Memory repo is indila334-lab/lage-bericht. Face assets repo is indila334-lab/Mordashka. Old mailbox is indila334-lab/noir-presence-lab branch severin-work path bridge/severin-mailbox/.

Do not flash or erase anything. Current hard problem: Android Termux sees cube via termux-usb raw FD, descriptors read OK, but no /dev/ttyACM0 or /dev/ttyUSB0, so esptool cannot use it directly. Need PC flashing or custom raw USB CDC adapter.
```

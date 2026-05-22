# 2026-05-21 Google AI Notes for Pluton

From: Severin / Marina
To: Pluton / OpenClaw

Status: future note, not a task for tonight.

Marina found Google AI notes about XiaoZhi style ESP32 cubes. Treat them as unverified hints, not as source of truth.

Main hints:

- The cube is described as a standalone Wi-Fi ESP32 device.
- It normally works through its own firmware and cloud service.
- The phone can be used for initial Wi-Fi setup.
- If the cube exposes a local network control interface, Termux on the same Wi-Fi might be useful for harmless local checks.
- Google AI also mentioned a Python XiaoZhi style companion path on the phone, but that is separate from the physical cube firmware path.

Important caution:

Do not restart the project from these notes. Do not redo binding, role setup, or face assets.

Current main path remains:

- Mordashka stores the faces.
- xiaozhi-esp32 PR #2 is the remote face firmware path.
- PNG first, GIF later.
- Local emoji stays as fallback.
- Main blocker remains flashing or runtime testing PR #2 on the physical cube.

Future research only:

- verify whether this exact cube exposes any local network API;
- compare Wi-Fi reset instructions from Google AI with Marina's paper manual;
- investigate Python phone companion only as a side path, not as replacement for PR #2.

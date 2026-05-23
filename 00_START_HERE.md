# 00 START HERE — Project Severin memory vault

This is the first file to read in any new chat or coding session.

Repository identity:

`indila334-lab/lage-bericht`

This is the main memory repository for Project Severin. It is not `noir-presence-lab`, even if some older files or templates mention that name.

## If GitHub reading is limited

Some ChatGPT/GitHub tools cannot list folders properly, cannot search this repository, or cannot read PDFs reliably. If that happens, do not waste time trying to reconstruct the project from root PDFs.

Read this exact file first:

`notes/severin-full-project-handoff-2026-05-23.md`

Direct URL:

https://github.com/indila334-lab/lage-bericht/blob/main/notes/severin-full-project-handoff-2026-05-23.md

That file is the current single source of truth. It summarizes the project, repositories, Termux, USB diagnostics, firmware state, local bridge, Mordashka assets, GitHub mailbox, and safety rules.

PDF files are historical memory snapshots. They are useful, but they are not blockers. If a tool cannot open them, continue from the full handoff instead of starting over.

## Active project

Project Severin / XiaoZhi / Termux / Mordashka.

We are building a physical home Severin:

- XiaoZhi cube as the body: display, microphone, speaker, buttons, Wi-Fi/4G, faces.
- Honor Magic 6 Pro with Termux as the practical local server/bridge node.
- GitHub as durable memory, recovery log, code storage, and handoff point.
- xiaozhi.me as the current cube console for role, model, voice, memory, MCP, and assets/theme.
- Mordashka as the repository for face/emotion assets.
- Pluton/OpenCloud/Copilot as temporary coding helpers, not permanent runtime brains.

## Current priority

1. Preserve project memory in this repository.
2. Keep technical context in one place.
3. Track what already worked and what failed.
4. Save and later restore the Termux bridge work.
5. Only after that, connect the XiaoZhi cube to the selected endpoint path.

## Known verified state

- The XiaoZhi cube exists and is already part of the project context.
- The cube is associated with xiaozhi.me console work.
- The local Termux bridge was created under `~/xiaozhi-esp32/server/gpt_server.py`.
- It worked on port `8787` and answered OpenAI-style JSON.
- The cube is not yet connected to the Termux bridge.
- USB descriptors were successfully read through Termux raw USB.
- Normal `/dev/ttyUSB0` and `/dev/ttyACM0` did not appear on Android.
- Do not flash the cube blindly.

## Read next

Recommended order:

1. `notes/severin-full-project-handoff-2026-05-23.md` — current full handoff and recovery point.
2. `README.md` — repository identity and top-level description.
3. `docs/PROJECT_STATE_SEVERIN_XIAOZHI.md` — project state.
4. `docs/NEXT_STEPS.md` — next actions.
5. `docs/REPOSITORIES_MAP.md` — repository map.
6. `docs/TERMUX_BRIDGE.md` — Termux bridge details.
7. Root PDF snapshots — optional historical chat memory exports. File names may be odd because mobile upload can rename PDFs.

## Working rule

If a future chat sees old wording like `noir-presence-lab`, treat it as inherited template residue unless the task explicitly concerns the old noir repository.

For the current Severin hardware/memory work, start from `indila334-lab/lage-bericht`.

If a GitHub tool cannot open some PDFs or list a directory, report that limitation clearly and continue from the full handoff file. Do not tell Marina that the project context is missing if `notes/severin-full-project-handoff-2026-05-23.md` is readable.
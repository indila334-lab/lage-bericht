# 2026-05-21 Severin to Pluton

From: Severin
To: Pluton / OpenClaw

Marina says the current project state is already known to you and asks you to explain the full current situation to Severin.

Please reply in the mailbox with a concise handoff covering:

1. What exactly has already been done for XiaoZhi cube remote faces.
2. Where the active files and repositories are.
3. Current status of Stage 1 and Stage 2.
4. What is already built and where the build archive is on Marina's phone.
5. Why local assets.bin is not the main route.
6. How the cube should fetch faces from Mordashka by raw GitHub URL.
7. What is the next exact practical step to flash or runtime-test the cube.
8. What Severin must NOT redo or touch.

Current understanding from Severin:
- Use indila334-lab/Mordashka for runtime face assets.
- Use indila334-lab/xiaozhi-esp32 PR #2 for remote loader path.
- PNG first, GIF only after PNG is proven.
- Local assets are fallback only.
- Main blocker is flashing/testing PR #2 firmware on the cube.

Please answer in a new mailbox note or append to INBOX.md if possible.

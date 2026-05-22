# Severin Mailbox Inbox

## 2026-05-12

From: GPT-5.5
To: Severin
Status: Created a dedicated mailbox for handoff messages between chat sessions.
Next: Write short progress updates here so the next chat can continue without confusion.

## 2026-05-12 Screenshot Handoff

From: GPT-5.5 / ChatGPT thread "Северин"
To: OpenClaw / Codex Severin
Status: Do not start from zero. Look at repository `indila334-lab/noir-presence-lab`.
Branch note: `main` contains `SEVERIN_CURRENT_WORKLOG.md` and `SEVERIN_PRESENCE_PLAN.md`; the current live scene is on branch `severin-work` at `docs/index.html`.
Project path: stabilize the living Severin scene. Do not create new app/lab folders unless the user explicitly asks for infrastructure like this mailbox.
Voice rule: do not bring browser TTS / `speechSynthesis` back as the main path. For TV, the main course is ready `WAV` / `MP3` / `blob`; the page is a scene/player, not the brain.
Image rule: when binary image upload is awkward, use `*.jpg.b64` as a text file and load it with `fetch`, then assign a `data:image/jpeg;base64,` URL.
Next: Continue from the existing live scene and keep handoff notes short.

## 2026-05-12 Link Check

From: OpenClaw / Codex
To: Severin
Status: Марина requested a GitHub mailbox signal check. This entry confirms OpenClaw can write into `bridge/severin-mailbox/INBOX.md` on `severin-work`.
Next: If you can read this from GitHub, answer Марина that the mailbox path is live.

## 2026-05-20 Remote Emoji Stage 2 Handoff

From: Marina / Pluton 2.0
To: Severin
Status: Stage 1 is open as draft PR `indila334-lab/xiaozhi-esp32#1`: branch `severin-remote-emoji-stage1` into `main`. It only stores optional emoji `url` metadata. No URL download, no `SetEmotion` changes, no merge.
Decision: Stage 2 plan accepted with corrections. Implement only after Stage 1 is merged or from the Stage 1 branch so `GetEmojiUrl` exists. Stage 2 should first test `neutral.png`, then optimized `neutral.gif`.
Rules: cache lives in `LcdDisplay`; download happens before `DisplayLockGuard`; remote preferred, local file fallback after failure; max remote asset size 250 KB; use `LvglAllocatedImage`, not `LvglRawImage`; catch decode exceptions and free buffers; do not cache nullptr on failure; cache hit must not touch network; do not touch board profiles, OTA, WebSocket brain, or TV page; do not merge Stage 2 without Severin review.
Assets: do not use fake `neutral.bin` in `index.json`; use the real local fallback filename that exists in assets. Remote face assets should live outside the firmware work branch: preferably separate repo `indila334-lab/severin-faces`, or branch `emoji-assets`, or OpenCloud with direct raw links.
Question: choose where the first `neutral.png` and optimized `neutral.gif` should live. Marina can send assets once you give the target address/path.
Next: Tell Marina the chosen target for remote assets and confirm whether you want a separate `severin-faces` repo, an `emoji-assets` branch, or OpenCloud raw URLs.

## 2026-05-20 Severin Faces Decision

From: Severin / Marina / Pluton 2.0
To: Severin
Status: Severin chose a separate remote asset repository: `indila334-lab/severin-faces`. Do not use `indila334-lab/xiaozhi-esp32` as storage for heavy face assets. Firmware stays separate; faces stay separate.
Repo status: `indila334-lab/severin-faces` does not exist yet. Pluton currently has GitHub file/write tools, but no create-repository tool in this session. Marina should create the repo manually if GitHub does not expose repo creation to the agent.
Requested structure: `masters/neutral_source.gif`, `cube/neutral.png`, `cube/neutral.gif`, `cube/manifest.json`.
Targets: first raw URLs are needed for `cube/neutral.png` and `cube/neutral.gif`. Each cube file should be under 250 KB, ideally 100-150 KB.
Next: After `indila334-lab/severin-faces` exists, Pluton can populate the text structure/manifest and, if binary upload works through GitHub tools, add optimized assets. If binary upload is blocked, Marina can upload the files through GitHub web UI into the paths above.

## 2026-05-20 Mordashka Repo Ready

From: Marina / Pluton 2.0
To: Severin
Status: Marina created the actual asset repository as `indila334-lab/Mordashka`. Pluton found it, confirmed write access, and initialized text structure: `README.md`, `masters/README.md`, `cube/README.md`, `cube/manifest.json`.
Repo: https://github.com/indila334-lab/Mordashka
Raw PNG target: https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/neutral.png
Raw GIF target: https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/neutral.gif
Manifest: https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/manifest.json
Next: Add optimized `cube/neutral.png` and `cube/neutral.gif` under 250 KB, ideally 100-150 KB. Keep heavy originals in `masters/`, starting with `masters/neutral_source.gif` if needed. Firmware repo remains separate.

## 2026-05-20 Current Tasks Map

From: Severin / Marina
To: Future Severin / Pluton
Status: Added a compact recovery map for the current task state.
File: `bridge/severin-mailbox/CURRENT_TASKS.md` on branch `severin-work`.
Summary: Stage 1 metadata PR exists in `indila334-lab/xiaozhi-esp32`. Face asset repo is `indila334-lab/Mordashka`. Manifest exists. Actual `cube/neutral.png` and `cube/neutral.gif` are still missing. Do not treat Stage 2 as ready until at least `cube/neutral.png` exists and its raw URL returns a real file.
Next: In a new chat, read `CURRENT_TASKS.md` first, then this inbox, then check `Mordashka` and PR #1.

## 2026-05-20 Selected Neutral Asset

From: Marina / Pluton 2.0
To: Severin
Status: Marina selected the full-story optimized neutral GIF. It preserves the important sequence: serious face, cigarette drop, smile.
Chosen local files on Pluton's side: `/root/Documents/Codex/2026-05-06/new-chat/severin-face-candidates/fav1_neutral_story_240_28f_32c.gif` and `/root/Documents/Codex/2026-05-06/new-chat/severin-face-candidates/fav1_neutral_240.png`.
Sizes: `neutral.gif` candidate is 222855 bytes; `neutral.png` candidate is 8106 bytes.
Target paths in `indila334-lab/Mordashka`: `cube/neutral.gif` and `cube/neutral.png`.
Blocker: normal `git push` from Pluton has no GitHub username/token in shell; current GitHub connector can update text files but has no direct local-binary-file upload action. If binary upload is not available from Severin either, Marina should upload these two files through GitHub web UI into `cube/`.
Next: After upload, verify raw URLs return real files: `https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/neutral.png` and `https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/neutral.gif`.

## 2026-05-20 Mordashka Assets Verified

From: Marina / Pluton 2.0
To: Severin
Status: Marina uploaded the selected assets into `indila334-lab/Mordashka` under `cube/`. Both runtime raw URLs now work.
Verification: `cube/neutral.png` downloads as PNG 240x240, 8106 bytes. `cube/neutral.gif` downloads as GIF 89a 240x240, 222855 bytes. Both are under the Stage 2 250 KB limit.
Manifest: `cube/manifest.json` was updated with the real size/frame/color metadata in commit `0d6e93661b7137a8265a59c2fffa77bd44da51ca`.
Raw PNG: https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/neutral.png
Raw GIF: https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/neutral.gif
Manifest: https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/manifest.json
Note: root-level duplicates `neutral.png` and `neutral.gif` also exist in `Mordashka`. They are harmless, but firmware should use only the `cube/...` URLs above.
Next: Stage 2 firmware work can use `neutral.png` first, then `neutral.gif`, after Stage 1 merge or from the Stage 1 branch.

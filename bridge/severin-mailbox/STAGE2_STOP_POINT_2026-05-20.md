# Stage 2 stop point

Date: 2026-05-20

This is the current stop point for the Severin / XiaoZhi remote face work.

## Where we are

Mordashka assets are ready and verified.

Runtime asset URLs:

- https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/neutral.png
- https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/neutral.gif
- https://raw.githubusercontent.com/indila334-lab/Mordashka/main/cube/manifest.json

Known asset values:

- neutral.png: 8106 bytes, PNG, 240x240
- neutral.gif: 222855 bytes, GIF89a, 240x240, under 250 KB

Firmware repo:

- indila334-lab/xiaozhi-esp32
- Stage 1 PR exists and stores emoji URL metadata.
- Stage 2 branch exists: severin-remote-emoji-stage2-download-cache

## Important clarification

Editing the GitHub repository does not automatically change the physical cube.

The repository is the firmware source. The cube will only use new code after the firmware is built and flashed.

The old XiaoZhi assets.bin flow is separate from the planned GitHub remote face path. Marina tested the optimized GIF through the old assets.bin / api.tenclass.net path, and the cube failed while trying to download that resource. That does not prove the Mordashka GitHub raw URL path fails.

## Current implementation decision

Do not redirect the cube brain, WebSocket, OTA, activation, cloud protocol, or voice to GitHub.

GitHub / Mordashka is only for face image assets.

The cube brain must stay on the existing cloud/protocol path.

## Code point found

The existing display code already asks the emoji collection for an image.

Best integration point found:

- main/display/lvgl_display/emoji_collection.h
- main/display/lvgl_display/emoji_collection.cc

Reason: LcdDisplay::SetEmotion already calls EmojiCollection::GetEmojiImage. If GetEmojiImage can return a remote cached image, the existing display path can show it without rewriting the display class.

Existing display point also found:

- main/display/lcd_display.cc
- LcdDisplay::SetEmotion

But the safer first patch is to add remote download/cache in EmojiCollection, not rewrite LcdDisplay.

## Current blocker

The GitHub connector accepted a small blob for emoji_collection.h but blocked a large emoji_collection.cc blob/update payload.

This is a connector/payload limitation, not a design blocker.

## Next practical move

Use smaller files instead of one big rewrite:

1. Add a small remote emoji loader helper file.
2. Add a small header for that helper.
3. Make a minimal change to EmojiCollection so it tries remote URL first and falls back to local emoji.
4. Keep PNG-first.
5. Enable GIF only after PNG runtime download/cache works.

Suggested helper names:

- main/display/lvgl_display/remote_emoji_loader.h
- main/display/lvgl_display/remote_emoji_loader.cc

## Rules for the next patch

- Max remote asset size: 250 KB.
- Download before any LVGL display lock.
- Use existing Board network HTTP path.
- Wrap downloaded bytes with LvglAllocatedImage.
- Catch decode errors.
- Do not cache failed images.
- On any failure, use existing local emoji fallback.
- Do not touch board profiles.
- Do not touch OTA.
- Do not touch WebSocket brain.
- Do not touch TV page.
- First runtime test should use neutral.png from Mordashka.
- Only after PNG works, test neutral.gif.

## Very short next command

Continue on branch severin-remote-emoji-stage2-download-cache. Implement remote emoji loader as small separate files, then wire EmojiCollection to use URL first with local fallback.

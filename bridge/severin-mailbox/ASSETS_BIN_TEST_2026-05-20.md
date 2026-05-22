# XiaoZhi assets.bin test result

Date: 2026-05-20

Marina tested the optimized neutral GIF through the XiaoZhi web `Generate assets.bin` / flashing flow.

The cube showed Chinese messages meaning:

- loading resource
- found new resource URL at `http://api.tenclass.net/transfer/download/...`
- download resource failed

Important: this is not the planned GitHub remote-face Stage 2 path. The cube did not fetch from `raw.githubusercontent.com`. It used the existing XiaoZhi / tenclass transfer pipeline.

Therefore this failure does not prove that the `Mordashka` raw URLs or the GIF decoder fail. It may be a tenclass transfer, network, DNS, or assets.bin workflow issue.

Verified runtime assets in `indila334-lab/Mordashka`:

```text
cube/neutral.png  8106 bytes, PNG, 240x240
cube/neutral.gif  222855 bytes, GIF89a, 240x240, 28 frames, 32 colors
```

Next diagnostic idea for assets.bin flow:

1. static single-frame GIF
2. short 16-frame global-palette GIF
3. full 28-frame global-palette GIF
4. selected neutral GIF

Next project step: continue Stage 2 firmware branch `severin-remote-emoji-stage2-download-cache`, starting with direct runtime download/cache of PNG from `Mordashka`, then GIF.

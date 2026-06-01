# 2026-06-01 AmneziaWG family Wi-Fi diagnosis

Safe project note. Do not store VPN private keys, full client configs, QR codes, passwords, tokens, or GitHub secrets here.

## Current state

Marina's AmneziaWG VPN on the Aeza server is working. It was created through GitHub Actions because phone-side direct SSH to the server was unreliable, while GitHub Actions could SSH to Aeza using repository secrets.

Repository: `indila334-lab/lage-bericht`

Relevant workflow:

- `.github/workflows/openclaw-claw-link.yml`
- Current role: safe add-family-clients workflow, not full server reinstall.

Relevant status note:

- `notes/amneziawg-family-last-run.md`

Last confirmed successful family-client run:

- Commit: `4912def203f73019ba5bcae142e1b2f41abf97fb`
- Result markers:
  - `SERVER_CONFIG_PATH=/etc/amneziawg/awg0.conf`
  - `SERVER_PRIVATE_KEY_READ`
  - `SERVER_PUBLIC_KEY_READY`
  - `CLIENT_KEYS_GENERATED`
  - `FAMILY_PEERS_WRITTEN`
  - `AWG_SYNCCONF_OK`
  - `AWG0_SHOW_OK`
  - `DONE_FAMILY_CLIENTS`

Server-side family peers were added without intentionally touching Marina's existing client.

Current family client addresses:

- Marina: existing client, previously `10.66.66.2/32`
- Mama: `10.66.66.3/32`
- Sister: `10.66.66.4/32`

The fresh mama/sister configs were copied by Marina from the GitHub Actions log, then sensitive workflow runs were deleted. The full configs must not be committed to GitHub.

## What worked

- Marina's VPN profile works.
- Mama's new profile worked when she was with Marina.
- Mama's profile works when phone uses 4G.
- This strongly suggests the client key and server peer are valid.

## New problem

Mama later reported that at home the VPN keeps spinning when connected through her home Wi-Fi. When she switches from that Wi-Fi to 4G, it works.

The home Wi-Fi is behind a Megafon router/provider path.

Sister also reported that on her computer the connection keeps spinning.

## Most likely diagnosis

This is probably not a broken key and not a missing server peer, because the same family profile works on 4G.

Most likely causes:

1. The home Wi-Fi/router/provider path blocks or breaks UDP traffic needed by AmneziaWG.
2. The current endpoint uses port 443, but AmneziaWG/WireGuard-style traffic is still UDP, not TCP. Port 443 alone does not make it HTTPS/TCP.
3. Megafon router/provider filtering may allow normal HTTPS TCP/443 but block suspicious UDP/443 or WireGuard-like handshakes.
4. Less likely: local router firewall/VPN filtering, UDP flood protection, parental/security filter, or MTU issue.

If Amnezia shows endless connecting and no handshake on Wi-Fi, UDP blocking is more likely than MTU. MTU problems more often look like "connected but sites do not load".

## Important protocol clarification

If someone says "try 443 TCP", the idea is plausible as a fallback, but it is not the same as the current AmneziaWG setup.

Current AmneziaWG uses UDP. Even if the endpoint port number is 443, that is UDP/443, not TCP/443.

A true TCP/443 fallback normally means a different protocol/profile, for example a TLS-like proxy such as Reality/VLESS/Trojan/Xray, or another Amnezia-supported TCP-based mode. Do not simply edit the AmneziaWG endpoint and pretend it became TCP.

## What not to do

Do not:

- rerun full AmneziaWG install;
- regenerate the server from scratch;
- delete Marina's client;
- delete mama/sister peer blocks;
- commit client configs or keys;
- change the working Marina setup blindly;
- assume the server is broken before testing from 4G and Wi-Fi separately.

## Recommended next checks

1. On mama's phone, test the same VPN profile:
   - Wi-Fi off, 4G on: expected to work.
   - Home Wi-Fi on: currently fails/spins.

2. If possible, test the same phone/profile on a different Wi-Fi network, not Megafon home router.

3. In the Amnezia app, check whether it shows handshake/received bytes on Wi-Fi. If there is no handshake on Wi-Fi but there is handshake on 4G, this points at network/router/provider blocking.

4. If router settings are accessible, check for:
   - VPN blocking / security filter;
   - parental control;
   - firewall level;
   - UDP flood protection;
   - "safe internet" / operator filtering options.

5. If server-side diagnosis is needed, do it read-only first:
   - while mama tries to connect from home Wi-Fi, watch whether UDP packets arrive at the server on the AmneziaWG port;
   - do not change configs during this test.

## Recommended engineering path

Keep current AmneziaWG as the fast primary VPN because it works on Marina and works for mama on 4G.

For Megafon Wi-Fi and similar restrictive networks, prepare a separate fallback profile over real TCP/443 or TLS-like traffic. This should be a second profile, not a destructive replacement.

Best next architecture:

1. Primary profile: current AmneziaWG UDP setup.
2. Fallback profile: TCP/443 or TLS-like proxy on the same Aeza server, created separately.
3. Mama/sister use AmneziaWG where it connects; if a Wi-Fi blocks it, they switch to the fallback profile.

## Short message for Severin

The family configs are probably correct. Mama's profile works on 4G, so keys and server peer are valid. The failure happens specifically on Megafon home Wi-Fi. Current endpoint is port 443 but still UDP, because AmneziaWG is UDP. If the router/provider blocks UDP/443 or WireGuard-like UDP, Amnezia will spin forever. A suggestion to use "443 TCP" is directionally reasonable, but that means adding a separate TCP/TLS-like fallback profile, not editing the current AmneziaWG config as if it became TCP. Do not reinstall the server or touch Marina's working profile. Diagnose Wi-Fi vs 4G first, then add a non-destructive TCP/443 fallback if needed.

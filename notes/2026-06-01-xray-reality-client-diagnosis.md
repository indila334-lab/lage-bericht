# Xray Reality client diagnosis

Date: 2026-06-01

## Context

Marina tested the new VLESS Reality TCP/443 fallback profile in a client app. The client showed a connected VPN state, but YouTube did not open.

This note records the diagnosis without storing private client links, UUIDs, private keys, QR codes, or full configs.

## What was verified

The existing AmneziaWG server/profile for Marina was not modified.

The Xray Reality fallback service on the Aeza server was checked from outside:

- TCP/443 is reachable.
- TLS camouflage with SNI `www.cloudflare.com` responds successfully.
- A direct HTTPS probe to the endpoint with Cloudflare host behavior returns a valid Cloudflare response.

Then the same Reality parameters were tested with a clean local Xray client, not through the phone app that Marina used.

Results through the clean Xray client:

- `https://www.google.com/generate_204` -> HTTP 204
- `https://www.cloudflare.com/cdn-cgi/trace` -> HTTP 200
- `https://www.youtube.com/generate_204` -> HTTP 204
- `https://youtubei.googleapis.com/generate_204` -> HTTP 204
- `https://www.googlevideo.com/generate_204` -> HTTP 204

## Conclusion

The server-side Xray Reality TCP/443 fallback works.

The VLESS Reality link itself is viable when used by a proper Xray-compatible client.

If a phone app says "connected" but YouTube still does not open, the likely problem is the client app or its import/routing mode, not the server.

Most likely causes:

- The app imported the VLESS Reality link but did not route all traffic through it.
- The app shows VPN connected while the proxy core is not actually handling browser traffic.
- The app does not fully support this VLESS Reality profile format.
- The endpoint in the copied link was still masked as `***:443` instead of the real server IP.
- Android per-app VPN or split tunneling excluded YouTube/Google/Chrome.

## Important detail

Do not add `flow=xtls-rprx-vision` to the current client link unless the server client entries are also changed to use that flow.

A local test with client-side `flow=xtls-rprx-vision` against the current server config failed, while the no-flow profile worked.

## Recommended next step

For family fallback, test the same VLESS Reality link in a dedicated Xray client such as:

- v2rayNG on Android;
- Hiddify Next, if available and working on the device.

Required client behavior:

- import the same VLESS Reality link;
- ensure global VPN / route-all mode is enabled;
- disable per-app bypass for YouTube, Chrome, Google Play services, and Google app;
- test `google.com`, `youtube.com`, and the YouTube app.

## What not to do

- Do not reinstall AmneziaWG.
- Do not remove Marina's working AmneziaWG profile.
- Do not delete existing AmneziaWG family peers.
- Do not regenerate server keys.
- Do not rerun the full AmneziaWG installer.
- Do not publish private links or client configs in GitHub.

## Sensitive logs

The successful GitHub Actions run that printed family Reality links should be deleted after Marina copies the links.

Known sensitive run:

- `26777154197`

The failed initial Reality run did not produce final usable links, but can also be deleted for cleanliness:

- `26776900679`

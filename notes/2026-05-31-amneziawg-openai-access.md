# 2026-05-31 AmneziaWG access recovery

Safe project note. Do not store VPN configs, private keys, QR codes, passwords, tokens, logins, or full connection strings here.

## Summary

On 2026-05-31 Marina and Severin restored access to OpenClaw/OpenAI from Russia after the previous VPN/access path stopped working reliably.

The phone-side Amnezia app could not reach the Aeza server directly over SSH: port 22 timed out from the phone path. GitHub Actions, however, could reach the server over SSH using repository secrets.

The working route was:

1. Use the existing workflow in `indila334-lab/lage-bericht`:
   `.github/workflows/openclaw-claw-link.yml`
2. Temporarily repurpose that workflow from the phone/GitHub UI because creating a new workflow through Severin's tooling was blocked.
3. Verify SSH access from GitHub Actions to the Aeza server.
4. Verify that AmneziaWG packages are available for Ubuntu noble from `ppa:amnezia/ppa`.
5. Install and configure AmneziaWG through GitHub Actions.
6. Take the generated client configuration from the workflow output and import it into the Amnezia app on Marina's phone.
7. Confirm that Amnezia shows connected.
8. Confirm that Pluton/OpenClaw answers again.

## Confirmed workflow milestones

### SSH test

Workflow/job names used during the test:

- Workflow: `Aeza AmneziaWG Setup`
- Job: `setup-amneziawg`

Important log markers:

```text
SSH_OK
AMNEZIAWG_TEST_READY
```

Meaning: GitHub Actions successfully reached the Aeza server over SSH.

### Package check

Workflow/job names used during the check:

- Workflow: `Aeza AmneziaWG Package Check`
- Job: `check-amneziawg`

Important result:

```text
amneziawg - fast, modern, secure kernel VPN tunnel
amneziawg-dkms
amneziawg-tools
AMNEZIAWG_PACKAGE_CHECK_DONE
```

Meaning: AmneziaWG packages were available for Ubuntu noble from the Amnezia PPA.

### Install step

Workflow/job names used during installation:

- Workflow: `Aeza AmneziaWG Install`
- Job: `install-amneziawg`

Result:

- AmneziaWG was installed on the Aeza server.
- A client configuration was generated.
- Marina imported the configuration into Amnezia.
- Amnezia showed connected.
- OpenClaw/Pluton became reachable again.

## Important security rules

Do not commit any of the following to GitHub:

- private keys;
- full VPN configs;
- QR codes;
- passwords;
- tokens;
- logins;
- full connection strings;
- complete server endpoint details if they can be avoided.

Only high-level operational notes belong in this repository.

## Current repository hygiene warning

At the time this note was written, `.github/workflows/openclaw-claw-link.yml` still appeared to be the emergency AmneziaWG installer workflow, not necessarily the original `openclaw-claw-link` workflow.

Do not casually rerun or edit it. It may regenerate client configuration and print sensitive client config material to workflow logs. Before changing it, Marina and Severin should decide whether to:

1. keep it as a known emergency recovery workflow;
2. archive it under a clearer name;
3. restore the original `openclaw-claw-link.yml`; or
4. rewrite it so that it no longer prints secrets into logs.

Do not restore or delete it blindly, because it may be the only working bridge recipe from the outage.

## Short formulation

On 2026-05-31 access to OpenClaw/OpenAI was restored through Marina's own AmneziaWG setup on Aeza. Direct SSH from the phone-side Amnezia path timed out, so installation was performed through GitHub Actions using repository secrets. The generated config was imported into Amnezia, the connection came up, and Pluton/OpenClaw started responding again. Secrets, keys, QR codes, and full configs must not be stored in the repository.

## Next maintenance actions

1. Decide what to do with `.github/workflows/openclaw-claw-link.yml` after the emergency use.
2. If the workflow is kept, rename or document it clearly so future chats understand what it is.
3. Consider rotating the client config if it was exposed in workflow logs longer than intended.
4. Keep this note as historical memory only; it is not a runnable instruction and intentionally omits secrets.

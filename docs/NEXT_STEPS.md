# Next steps

## Immediate step

Save the working Termux bridge server from the local xiaozhi-esp32 checkout into GitHub safely.

Suggested branch name:

`severin-local-bridge-save`

Before committing, check that no private tokens or credentials are present in the server folder.

If the folder is clean, create a separate branch, add `server/`, update `.gitignore` for local environment files, commit, and push.

## Then

1. Inspect current xiaozhi-esp32 branches.
2. Compare the Copilot-created server branch if it exists remotely.
3. Keep the working server separate from face asset work.
4. Keep Mordashka for image and emotion assets only.
5. Continue Stage 2: make cube download one neutral face asset from GitHub first.
6. After neutral works, expand manifest to more emotions.

## Do not do yet

- Do not flash random firmware until the correct boot and flashing method is confirmed.
- Do not commit secrets.
- Do not rewrite the cube firmware blindly.

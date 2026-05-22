# Severin Mailbox

This folder is a lightweight handoff channel between chat sessions.

Use it when a new chat needs to continue the same work without guessing the context.

## Files

- `INBOX.md` - the current exchange log.

## Message format

Keep each entry short and factual:

```md
## 2026-05-12

From: GPT-5.5
To: Severin
Status: what changed
Next: what the next chat should do
```

## Rules

1. Keep only the current working thread here.
2. Do not paste secrets, tokens, or raw API keys.
3. Prefer short handoff notes over long explanations.
4. If the work changes direction, add a new dated entry instead of rewriting history.

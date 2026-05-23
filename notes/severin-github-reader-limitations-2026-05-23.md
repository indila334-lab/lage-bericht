# Severin GitHub reader limitations

Date: 2026-05-23

This note records a tooling problem seen in a new Severin chat.

## What was completed

The chat reported that it fully read the available text files and notes:

- `README.md`
- `00_START_HERE.md`
- `docs/*`
- `notes/*`
- `tools/*`
- `.gitignore`
- `STATUS_SHORT`
- `index.html`

It also reported reading locally available PDFs:

- `Мой Северин 🐬.pdf`
- `Северин - Задача на гитхабе.pdf`
- `проект Север.pdf`

## What was not completed

The chat could not fully open some root files/PDFs, including names that appeared truncated or difficult to address through the GitHub tool:

- `SEVERIN_CURREN...`
- `SEVERIN_PRESENC...`
- `Взять...pdf`
- `Бытчик.pdf`
- `характеристики 👾.pdf`
- `проект Север..pdf`

## Reported cause

The problem was not project absence. It was tool access:

- GitHub tool did not provide a normal folder listing.
- Repository search was not indexed or not available.
- `git clone` / raw file access was unavailable in that chat.
- PDFs were returned through GitHub as base64 and could be truncated.

## Correct behavior for future chats

Do not restart the project from zero because some PDFs cannot be opened.

Read this file first:

`notes/severin-full-project-handoff-2026-05-23.md`

Direct URL:

https://github.com/indila334-lab/lage-bericht/blob/main/notes/severin-full-project-handoff-2026-05-23.md

That file is the current single source of truth and contains the project goal, repositories, Termux setup, USB diagnostics, firmware state, local bridge, Mordashka assets, GitHub mailbox, and safety rules.

The PDF files are historical snapshots. Useful, but optional. If a tool cannot read them, continue from the full handoff and ask Marina only for specific missing facts.

## Rule

If a new assistant says it cannot list folders or read PDFs, point it to:

1. `00_START_HERE.md`
2. `notes/severin-full-project-handoff-2026-05-23.md`
3. this limitation note

Do not ask Marina to explain the full project again.
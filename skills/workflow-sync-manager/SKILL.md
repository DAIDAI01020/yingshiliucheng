---
name: workflow-sync-manager
description: Manage safe, versioned Git synchronization for the film AI workflow repository. Use when recording update logs, committing an explicit workflow-source scope, checking remote divergence, freezing a release tag, or publishing skill updates to GitHub or GitLab without uploading generated assets or secrets.
---

# Workflow Sync Manager

## Core role

Own the source-of-truth publication step for the film/visual agent. It records the change, stages only approved workflow paths, scans the staged patch for secrets, blocks unsafe divergence, commits, optionally tags a frozen version, and pushes to the selected remote.

## Repository policy

Allowed source scope:

- `skills/`
- `README.md`
- `WORKFLOW.md`
- `.gitignore`
- `sync-logs/`

Never publish generated images, videos, audio, project assets, temporary prompt inputs, `.env` files, cookies, access tokens, API keys, or private keys.

## Safe publication contract

Before a push:

1. Confirm the requested remote and branch exist and the current branch matches.
2. Fetch the remote branch.
3. Stop if the remote has commits missing locally; never force-push automatically.
4. Prefer `--paths-file` for a reviewed one-path-per-line whitelist.
5. Reject pre-staged files outside the reviewed whitelist without altering the user's index. Check sensitive filenames, symlink/submodule entries, and staged file contents for plaintext secrets; deleted secrets must not block their removal.
6. Write `sync-logs/YYYY-MM-DD.md` and commit it.
7. If requested, create an annotated immutable release tag and push branch plus tag.

The sync script must not silently fall back from the requested GitHub remote to GitLab or vice versa.

An unchanged sync must not create another log/commit. A push-only retry may publish existing commits. A committed log records publication as pending, never successful before push; report success only after the remote branch hash matches local HEAD. Secret scanning is a safety check, not a guarantee: review the exact changed paths and content before publication.

## Commands

From the repository root with the workspace Node runtime:

```powershell
node .\skills\workflow-sync-manager\scripts\sync-workflow.mjs status
node .\skills\workflow-sync-manager\scripts\sync-workflow.mjs log --summary "记录本次优化"
node .\skills\workflow-sync-manager\scripts\sync-workflow.mjs sync --summary "优化整个影视 Agent" --paths-file C:\Temp\workflow-paths.txt
node .\skills\workflow-sync-manager\scripts\sync-workflow.mjs sync --summary "优化整个影视 Agent" --paths-file C:\Temp\workflow-paths.txt --remote github --branch main --tag agent-v2026.07.22 --push
```

`--tag` requires `--push`. The tag is accepted only if absent or already points at the final local commit.

## Failure handling

- Secret match: stop before committing.
- Disallowed or out-of-scope pre-staged path: stop and preserve the user's staging state.
- Wrong branch or missing remote: stop before committing.
- Remote branch ahead: stop and ask for an explicit integration decision.
- Push rejection: keep the local commits and report them; never rewrite history.

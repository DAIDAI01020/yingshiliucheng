---
name: workflow-sync-manager
description: Manage Git/GitLab synchronization for the film AI workflow repository. Use when the user wants to record update logs, commit workflow changes, push to GitLab, check sync status across desktop/Mac, or safely publish skill updates without uploading generated outputs or secrets.
---

# Workflow Sync Manager

## Core role

Keep this workflow repository clean and synchronized across machines. This skill handles update logs, git commits, and GitLab pushes for the `H:\yingshi` workflow repo.

Use it when the user says:

- `把这次更新同步上去`
- `写个日志然后推到 GitLab`
- `提交这次 skill 更新`
- `检查同步状态`
- `台式机和 Mac 同步一下`

## Repository policy

Only workflow source files should be committed:

- `skills/`
- `README.md`
- `WORKFLOW.md`
- `.gitignore`
- `sync-logs/`

Do not commit:

- `outputs/`
- `projects/`
- generated images, video, audio, logs, review boards
- temporary `*_input.json`
- `.env`, API keys, private keys, tokens, or secrets

## Update log

Every sync should write or append a human-readable log in:

```text
sync-logs/YYYY-MM-DD.md
```

The log should include:

- timestamp
- summary
- changed files
- commit hash after commit when available
- push target when pushed

## Script usage

From this skill folder:

```powershell
node .\scripts\sync-workflow.mjs status
node .\scripts\sync-workflow.mjs log --summary "更新出图审片流程"
node .\scripts\sync-workflow.mjs sync --summary "更新项目状态层" --push
```

## Rules

- Never stage ignored generated outputs.
- Run the secret scanner before committing.
- If a staged diff contains a likely plaintext secret, stop and do not commit.
- If remote has new commits, fetch first and integrate safely before pushing.
- Do not force push unless the user explicitly asks and understands it will rewrite remote history.
- Prefer concise commit messages derived from the summary, such as `Update workflow sync manager`.


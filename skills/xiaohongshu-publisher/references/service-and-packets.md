# Local publisher and packet contract

## Upstream and runtime

Backend: [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp), Apache-2.0. Integration inspected against release [v2.5.5](https://github.com/xpzouying/xiaohongshu-mcp/releases/tag/v2.5.5) on 2026-10-15. Consult its [API documentation](https://github.com/xpzouying/xiaohongshu-mcp/blob/v2.5.5/docs/API.md) when upgrading. This adapter is local workflow code, not a vendored upstream skill or a claim that the service is registered as a Codex connector.

Download the official release executable for the host into a private runtime directory outside Git and compare SHA-256 with the GitHub release asset digest. On this Windows installation the pinned directory is `Z:/codex/tools/xiaohongshu-mcp/v2.5.5`. The server may download its own browser on first start. Do not register OS startup jobs as part of setup.

```powershell
./scripts/start-service.ps1 -RuntimeRoot 'Z:/codex/tools/xiaohongshu-mcp/v2.5.5'
python scripts/publish_xhs.py check --token-file 'Z:/codex/tools/xiaohongshu-mcp/v2.5.5/state/auth-token.txt'
```

The start helper reuses a verified same-process service or launches hidden, binds `127.0.0.1:18060`, stores cookies under runtime state and creates a private local token if absent. It does not log in. Do not expose this service on a LAN or forward its port.

`GET /api/v1/login/qrcode` yields a short-lived QR image. Obtain/display it only when the user is ready to log in, using the token without printing it. Then check `/api/v1/login/status`; `data.user_id` must match the target. No username-only fallback. The helper's `check` command reports health and login identity; a missing browser or login is a real setup step, not a passing publish test.

## Ready pack

Save a JSON packet alongside the existing project docs/review files, not in the skill directory. Use absolute local file paths on the service host. This adapter intentionally requires local media so reviewed bytes can be fingerprinted. It supports images or one video, not both:

```json
{
  "post_id": "2026-10-20-art-01",
  "account_id": "actual-user-id-from-login-status",
  "title": "最终标题",
  "content": "最终正文",
  "images": ["H:/project/delivery/01.png", "H:/project/delivery/02.png"],
  "tags": ["艺术"],
  "visibility": "公开可见",
  "schedule_at": "2026-10-20T20:30:00+08:00",
  "qc": {"status": "passed", "evidence": "H:/project/review/post-review.md"},
  "disclosure": {"status": "not_required", "evidence": "Basis for the applicable disclosure decision"}
}
```

For video replace `images` with `video`. Omit `schedule_at` only for authorized immediate publishing. Visibility must be explicit. Review evidence is a real nonempty local file reviewing this exact pack/version; the agent must inspect it, not fabricate a passing flag. `disclosure.status` is `not_required` with a real basis, or `handled_in_content` where the reviewed content satisfies the applicable requirement. If platform-specific controls are required, set `requires_platform_control` and use the browser route; the REST adapter blocks. This field records a decision, not an automatic policy determination.

```text
python scripts/publish_xhs.py prepare --packet <packet.json>
python scripts/publish_xhs.py publish --packet <packet.json> --ledger <shared-account-receipts-dir> --expected-fingerprint <prepare-result> --authorization-source <user-message-reference> --execute --token-file <local-token-file>
```

`prepare` makes no network request or submission. It returns a fingerprint and payload for review. Publishing rehashes and requires the same fingerprint. It validates the backend's documented 1-hour-to-14-day schedule window at send time (check again after backend upgrades). A too-soon appointment is not converted to immediate submission. Credentials use `XHS_AUTH_TOKEN` or `--token-file`, never packet fields or a literal command-line token.

Always use the same ledger root for an account, e.g. `<runtime>/state/receipts`. The helper serializes by account, blocks any existing attempt for a post_id, and also blocks the same copy/media submitted under another post_id. Fingerprints bind review evidence, scheduling and visibility; duplicate detection intentionally ignores scheduling and visibility. Lock files remaining after process death must be reconciled, never automatically removed on timeout.

The helper stores timestamps, fingerprints, authorization source and returned status only; it does not save login tokens or raw profile data. To reconcile, inspect the creator UI first and append a dated observation to the existing receipt containing outcome, note ID/URL when exposed and evidence path. Leave attempted receipts in place. Use project-state-manager's existing legal states for project summaries and link the receipt rather than introducing transport status names as project enums.

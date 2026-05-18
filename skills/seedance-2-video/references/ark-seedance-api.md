# Ark Seedance 2.0 API Reference

## Official References

- Create video task: https://www.volcengine.com/docs/82379/1520757?lang=zh
- Query video task: https://www.volcengine.com/docs/82379/1521309?lang=zh
- Base URL and authentication: https://www.volcengine.com/docs/82379/1298459?lang=zh

## Environment

- Required: `ARK_API_KEY`
- Optional: `ARK_BASE_URL`, default `https://ark.cn-beijing.volces.com`
- Optional local private key file: `~/.config/codex-seedance-2-video/secrets.json`, created by `seedance_task.py setup-key`
- Employee setup wrapper: `scripts/install_employee_key.sh`

Do not write the actual key into skill files, shell history examples, manifests, logs, or generated references.

Key lookup order:

1. `ARK_API_KEY` environment variable.
2. Local private key file created by `setup-key`.

The local key file is intentionally outside the skill directory so the skill folder can be shared without including secrets.

For employee distribution, ask users to run:

```bash
scripts/install_employee_key.sh
```

The wrapper hides input, calls `seedance_task.py setup-key`, and runs `doctor`.

## Submit Task

```http
POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks
Authorization: Bearer $ARK_API_KEY
Content-Type: application/json
```

Payload:

```json
{
  "model": "doubao-seedance-2-0-260128",
  "content": [
    {
      "type": "text",
      "text": "中文视频提示词"
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "https://public.example/source.png"
      },
      "role": "reference_image"
    }
  ],
  "ratio": "9:16",
  "duration": 15,
  "resolution": "720p",
  "watermark": false,
  "seed": -1
}
```

Supported image roles used by the script:

- `reference_image`: default; preserves image identity without forcing it to be the literal first frame.
- `first_frame`: use only when the first image must be the opening frame.
- `last_frame`: used with `firstLastFrame` mode.

## Poll Task

```http
GET https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/<task_id>
Authorization: Bearer $ARK_API_KEY
```

Treat these as non-terminal states:

- `submitted`
- `queued`
- `pending`
- `starting`
- `processing`
- `running`
- `in_progress`

Treat these as success:

- `succeeded`
- `success`
- `completed`
- `complete`

Treat these as failure:

- `failed`
- `failure`
- `error`
- `expired`
- `canceled`
- `cancelled`

Result URL paths to check, in order:

- `content.video_url`
- `content.url`
- `content.output_url`
- `video_url`
- `output`
- `output.url`
- `result_url`
- `url`
- `data.content.video_url`
- `data.video_url`
- `data.output`
- `data.result_url`

## Image URL Rules

Ark must be able to fetch the media itself. Use public `http` or `https` URLs only.

Do not pass local filesystem paths, generated covers, historical outputs, `config/ip-profiles/`, `.analysis_frames/`, or other derived artifacts as Seedance image inputs.

When integrating with IP Video Factory, reuse the batch `source_image.luna_public_url` that was prepared from the current user upload.

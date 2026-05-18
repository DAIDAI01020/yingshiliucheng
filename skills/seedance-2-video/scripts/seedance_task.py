#!/usr/bin/env python3
"""Direct Ark Seedance 2.0 task runner.

This script intentionally uses only Python's standard library so the skill can be
shared as a small self-contained folder.
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://ark.cn-beijing.volces.com"
DEFAULT_MODEL = "doubao-seedance-2-0-260128"
DEFAULT_RATIO = "9:16"
DEFAULT_DURATION = 15
DEFAULT_RESOLUTION = "720p"
DEFAULT_SEED = -1
DEFAULT_TIMEOUT_SECONDS = 21_600
DEFAULT_POLL_MIN_SECONDS = 15
DEFAULT_POLL_MID_SECONDS = 45
DEFAULT_POLL_MAX_SECONDS = 120
ESTIMATED_WAIT_MIN_SECONDS = 30
ESTIMATED_WAIT_MAX_SECONDS = 300
DEFAULT_SECRET_FILE = "~/.config/codex-seedance-2-video/secrets.json"
VALID_RATIOS = {"21:9", "16:9", "4:3", "1:1", "3:4", "9:16", "adaptive"}
VALID_RESOLUTIONS = {"480p", "720p", "1080p"}
SOURCE_IMAGE_POLICY = "use_current_upload_only"


class SeedanceError(RuntimeError):
    pass


def now_iso_local() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())


def now_unix() -> int:
    return int(time.time())


def ssl_context():
    if os.environ.get("ARK_ALLOW_INSECURE_TLS") == "1":
        return ssl._create_unverified_context()
    return None


def is_http_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def redacted_key_state(value: str | None) -> str:
    if not value:
        return "missing"
    return f"present:{len(value)}chars"


def default_secret_file() -> Path:
    raw = os.environ.get("SEEDANCE_ARK_KEY_FILE") or os.environ.get("ARK_KEY_FILE") or DEFAULT_SECRET_FILE
    return Path(raw).expanduser()


def secret_file_from_arg(value: str | None) -> Path:
    return Path(value).expanduser() if value else default_secret_file()


def path_is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def base_url_from_args(value: str | None) -> str:
    return (value or os.environ.get("ARK_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


def read_key_file(path: Path) -> str | None:
    if not path.exists():
        return None
    data = read_json(path)
    for key in ("ark_api_key", "ARK_API_KEY"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def api_key_from_env_or_file(key_file_arg: str | None = None) -> tuple[str, str]:
    key = os.environ.get("ARK_API_KEY", "").strip()
    if key:
        return key, "env:ARK_API_KEY"
    key_file = secret_file_from_arg(key_file_arg)
    key = read_key_file(key_file)
    if key:
        return key, "local_secret_file"
    raise SeedanceError(
        "ARK_API_KEY is not configured. Run `seedance_task.py setup-key`, "
        "or set ARK_API_KEY in your local environment. Do not hardcode it in the skill."
    )


def key_status(key_file_arg: str | None = None) -> tuple[str, str, Path]:
    env_key = os.environ.get("ARK_API_KEY", "").strip()
    key_file = secret_file_from_arg(key_file_arg)
    if env_key:
        return redacted_key_state(env_key), "env:ARK_API_KEY", key_file
    file_key = read_key_file(key_file)
    if file_key:
        return redacted_key_state(file_key), "local_secret_file", key_file
    return "missing", "missing", key_file


def write_key_file(path: Path, api_key: str, force: bool = False) -> None:
    if path_is_relative_to(path, skill_dir()):
        raise SeedanceError(
            f"Refusing to store secrets inside the shareable skill directory: {skill_dir()}"
        )
    if path.exists() and not force:
        raise SeedanceError(f"Key file already exists: {path}. Re-run with --force to overwrite it.")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(path.parent, 0o700)
    except OSError:
        pass
    payload = {
        "ark_api_key": api_key,
        "created_at": now_iso_local(),
        "managed_by": "seedance-2-video setup-key",
    }
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.chmod(tmp, 0o600)
    tmp.replace(path)
    os.chmod(path, 0o600)


def http_json(
    method: str,
    url: str,
    api_key: str,
    payload: dict[str, Any] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    body = None
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context()) as resp:
            raw = resp.read()
            content_type = resp.headers.get("content-type", "")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SeedanceError(f"{method} {url} failed: HTTP {exc.code}: {sanitize_error_detail(detail, api_key)}") from exc
    except urllib.error.URLError as exc:
        raise SeedanceError(f"{method} {url} failed: {exc.reason}") from exc
    except (TimeoutError, OSError) as exc:
        raise SeedanceError(f"{method} {url} failed: {exc}") from exc

    if raw and "application/json" not in content_type.lower():
        snippet = raw.decode("utf-8", errors="replace")[:300]
        raise SeedanceError(f"{method} {url} returned non-JSON response: {snippet}")
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def sanitize_error_detail(detail: str, api_key: str | None = None) -> str:
    cleaned = detail
    for key in (api_key, os.environ.get("ARK_API_KEY", "")):
        if key:
            cleaned = cleaned.replace(key, "<redacted>")
    return cleaned[:500]


def download_file(url: str, path: Path, timeout: int = 300) -> None:
    req = urllib.request.Request(url, headers={"Accept": "video/*,*/*"}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context()) as resp:
            data = resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SeedanceError(f"download failed: HTTP {exc.code}: {detail[:300]}") from exc
    except urllib.error.URLError as exc:
        raise SeedanceError(f"download failed: {exc.reason}") from exc
    except (TimeoutError, OSError) as exc:
        raise SeedanceError(f"download failed: {exc}") from exc

    if len(data) < 1024:
        raise SeedanceError(f"downloaded video is too small ({len(data)} bytes)")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_bytes(data)
    tmp.replace(path)


def head_or_range_check(url: str, timeout: int = 15) -> tuple[bool, str]:
    if not is_http_url(url):
        return False, "not an http(s) URL"
    for method in ("HEAD", "GET"):
        headers = {"Accept": "*/*"}
        if method == "GET":
            headers["Range"] = "bytes=0-0"
        req = urllib.request.Request(url, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ssl_context()) as resp:
                status = getattr(resp, "status", 200)
                return 200 <= int(status) < 400, f"HTTP {status}"
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in {403, 405}:
                continue
            return False, f"HTTP {exc.code}"
        except Exception as exc:  # noqa: BLE001 - doctor should summarize reachability.
            if method == "HEAD":
                continue
            return False, str(exc)
    return False, "unreachable"


def get_by_path(obj: Any, path: str) -> Any:
    current = obj
    for key in path.replace("[", ".").replace("]", "").split("."):
        if key == "":
            continue
        if current is None:
            return None
        if isinstance(current, list) and key.isdigit():
            idx = int(key)
            current = current[idx] if idx < len(current) else None
        elif isinstance(current, dict):
            current = current.get(key)
        else:
            return None
    return current


def first_string(data: dict[str, Any], paths: list[str]) -> str | None:
    for path in paths:
        value = get_by_path(data, path)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def first_number(data: dict[str, Any], paths: list[str]) -> int | float | None:
    for path in paths:
        value = get_by_path(data, path)
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str) and value.strip().isdigit():
            return int(value.strip())
    return None


def extract_task_id(data: dict[str, Any]) -> str | None:
    return first_string(data, ["id", "task_id", "data.task_id", "data.id", "data[0].task_id"])


def extract_status(data: dict[str, Any]) -> str:
    return first_string(data, ["status", "data.status", "data[0].status"]) or "processing"


def normalize_status(status_value: str | None) -> str:
    status = str(status_value or "").lower()
    if "success" in status or "complete" in status or "succeed" in status:
        return "succeeded"
    if "fail" in status or "error" in status or "expired" in status:
        return "failed"
    if "cancel" in status:
        return "canceled"
    if "queue" in status or "submit" in status or "pending" in status or "start" in status:
        return "queued"
    return "processing"


def extract_result_url(data: dict[str, Any]) -> str | None:
    return first_string(
        data,
        [
            "content.video_url",
            "content.url",
            "content.output_url",
            "video_url",
            "output",
            "output.url",
            "result_url",
            "url",
            "data.content.video_url",
            "data.video_url",
            "data.output",
            "data.result_url",
        ],
    )


def extract_error_message(data: dict[str, Any]) -> str | None:
    return first_string(data, ["error.message", "error", "message", "data.fail_reason", "fail_reason"])


def extract_progress(data: dict[str, Any]) -> int | float | None:
    return first_number(data, ["progress", "data.progress", "usage.progress"])


def extract_progress_message(data: dict[str, Any]) -> str | None:
    return first_string(data, ["progressMessage", "progress_message", "message", "data.progressMessage", "data.progress_message"])


def extract_queue_position(data: dict[str, Any]) -> int | float | None:
    return first_number(data, ["queuePosition", "queue_position", "data.queuePosition", "data.queue_position"])


def extract_estimated_wait(data: dict[str, Any]) -> int | float | None:
    return first_number(
        data,
        ["estimatedWaitTime", "estimated_wait_time", "estimated_wait_seconds", "data.estimatedWaitTime", "data.estimated_wait_time"],
    )


def clamp(value: int, lower: int, upper: int) -> int:
    return max(lower, min(upper, value))


def compute_next_poll_seconds(
    elapsed_seconds: float,
    estimated_wait: int | float | None,
    min_seconds: int,
    mid_seconds: int,
    max_seconds: int,
) -> int:
    if estimated_wait is not None and estimated_wait > 0:
        wait_seconds = int(estimated_wait / 1000) if estimated_wait > 10_000 else int(estimated_wait)
        return clamp(wait_seconds, ESTIMATED_WAIT_MIN_SECONDS, ESTIMATED_WAIT_MAX_SECONDS)
    if elapsed_seconds < 120:
        return min_seconds
    if elapsed_seconds < 900:
        return mid_seconds
    return max_seconds


def validate_prompt(prompt: str) -> str:
    text = prompt.strip()
    if not text:
        raise SeedanceError("prompt is empty")
    return text


def read_prompt(args: argparse.Namespace) -> tuple[str, str]:
    if getattr(args, "prompt", None):
        return validate_prompt(args.prompt), "inline"
    prompt_file = getattr(args, "prompt_file", None)
    if prompt_file:
        path = Path(prompt_file).expanduser().resolve()
        if not path.exists():
            raise SeedanceError(f"prompt file does not exist: {path}")
        return validate_prompt(path.read_text(encoding="utf-8")), str(path)
    raise SeedanceError("Provide --prompt or --prompt-file")


def validate_image_urls(urls: list[str]) -> list[str]:
    clean = [url.strip() for url in urls if url and url.strip()]
    if not clean:
        raise SeedanceError("Provide at least one --image-url")
    if len(clean) > 9:
        raise SeedanceError("Seedance supports at most 9 image URLs")
    for url in clean:
        if not is_http_url(url):
            raise SeedanceError(f"Seedance direct Ark input must be a public http(s) URL, got: {url}")
    return clean


def validate_generation_args(args: argparse.Namespace) -> None:
    if args.ratio not in VALID_RATIOS:
        raise SeedanceError(f"ratio must be one of {sorted(VALID_RATIOS)}, got {args.ratio}")
    if args.resolution not in VALID_RESOLUTIONS:
        raise SeedanceError(f"resolution must be one of {sorted(VALID_RESOLUTIONS)}, got {args.resolution}")
    if args.duration != -1 and not 4 <= args.duration <= 15:
        raise SeedanceError("duration must be -1 or an integer from 4 to 15")
    if args.seed != -1 and not 0 <= args.seed <= 4_294_967_295:
        raise SeedanceError("seed must be -1 or an integer from 0 to 4294967295")


def content_for_images(image_urls: list[str], video_mode: str) -> list[dict[str, Any]]:
    if video_mode == "firstFrame":
        return [{"type": "image_url", "image_url": {"url": image_urls[0]}, "role": "first_frame"}]
    if video_mode == "firstLastFrame":
        if len(image_urls) < 2:
            raise SeedanceError("videoMode firstLastFrame requires at least 2 image URLs")
        return [
            {"type": "image_url", "image_url": {"url": image_urls[0]}, "role": "first_frame"},
            {"type": "image_url", "image_url": {"url": image_urls[1]}, "role": "last_frame"},
        ]
    return [{"type": "image_url", "image_url": {"url": url}, "role": "reference_image"} for url in image_urls]


def build_payload(prompt: str, image_urls: list[str], args: argparse.Namespace) -> dict[str, Any]:
    validate_generation_args(args)
    content: list[dict[str, Any]] = [{"type": "text", "text": prompt}]
    content.extend(content_for_images(image_urls, args.video_mode))
    return {
        "model": args.model,
        "content": content,
        "ratio": args.ratio,
        "duration": args.duration,
        "resolution": args.resolution,
        "watermark": bool(args.watermark),
        "seed": args.seed,
    }


def manifest_path_for(output_dir: Path) -> Path:
    return output_dir / "run_manifest.json"


def read_run_dir_defaults(run_dir: Path) -> tuple[str | None, list[str]]:
    prompt_file = run_dir / "video_prompt.txt"
    image_urls: list[str] = []
    run_manifest = read_json(run_dir / "run_manifest.json")
    source_image = run_manifest.get("source_image")
    if isinstance(source_image, dict):
        url = source_image.get("luna_public_url") or source_image.get("url")
        if isinstance(url, str) and url:
            image_urls.append(url)

    parent_manifest = read_json(run_dir.parent / "batch_manifest.json")
    parent_source = parent_manifest.get("source_image")
    if isinstance(parent_source, dict):
        url = parent_source.get("luna_public_url")
        if isinstance(url, str) and url and url not in image_urls:
            image_urls.append(url)

    return (str(prompt_file) if prompt_file.exists() else None), image_urls


def apply_run_dir_defaults(args: argparse.Namespace) -> argparse.Namespace:
    if not getattr(args, "run_dir", None):
        return args
    run_dir = Path(args.run_dir).expanduser().resolve()
    if not run_dir.exists():
        raise SeedanceError(f"run dir does not exist: {run_dir}")
    prompt_file, image_urls = read_run_dir_defaults(run_dir)
    if not args.prompt and not args.prompt_file:
        if not prompt_file:
            raise SeedanceError(f"--run-dir requires {run_dir / 'video_prompt.txt'} or explicit --prompt-file")
        args.prompt_file = prompt_file
    if not args.image_url:
        args.image_url = image_urls
    if not getattr(args, "output_dir", None):
        args.output_dir = str(run_dir)
    return args


def update_manifest(output_dir: Path, updates: dict[str, Any]) -> dict[str, Any]:
    path = manifest_path_for(output_dir)
    manifest = read_json(path)
    manifest.update(updates)
    write_json(path, manifest)
    return manifest


def submit_task(base_url: str, api_key: str, payload: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    data = http_json("POST", f"{base_url}/api/v3/contents/generations/tasks", api_key, payload, timeout=60)
    task_id = extract_task_id(data)
    if not task_id:
        raise SeedanceError(f"Ark submit succeeded but no task id was found: {json.dumps(data, ensure_ascii=False)[:500]}")
    return task_id, data


def poll_once(base_url: str, api_key: str, task_id: str) -> dict[str, Any]:
    return http_json("GET", f"{base_url}/api/v3/contents/generations/tasks/{urllib.parse.quote(task_id)}", api_key, timeout=30)


def polling_snapshot(data: dict[str, Any], elapsed: float, next_poll_seconds: int | None = None) -> dict[str, Any]:
    raw_status = extract_status(data)
    snap: dict[str, Any] = {
        "status": normalize_status(raw_status),
        "raw_status": raw_status,
        "progress": extract_progress(data),
        "progressMessage": extract_progress_message(data),
        "queuePosition": extract_queue_position(data),
        "estimatedWaitTime": extract_estimated_wait(data),
        "last_polled_at_unix": now_unix(),
        "elapsed_seconds": int(elapsed),
    }
    if next_poll_seconds is not None:
        snap["next_poll_seconds"] = next_poll_seconds
    return snap


def write_initial_manifest(
    output_dir: Path,
    base_url: str,
    payload: dict[str, Any],
    prompt: str,
    prompt_source: str,
    image_urls: list[str],
    submit_response: dict[str, Any],
    task_id: str,
    key_source: str,
) -> None:
    manifest = {
        "skill": "seedance-2-video",
        "provider": "ark",
        "api_base_url": base_url,
        "model": payload.get("model"),
        "created_at": now_iso_local(),
        "updated_at": now_iso_local(),
        "auth": {
            "key_source": key_source,
            "key_stored_in_manifest": False,
        },
        "prompt": {
            "source": prompt_source,
            "sha256": sha256_text(prompt),
        },
        "source_images": [{"url": url, "role": item.get("role")} for url, item in zip(image_urls, payload["content"][1:])],
        "request": {
            "model": payload.get("model"),
            "ratio": payload.get("ratio"),
            "duration": payload.get("duration"),
            "resolution": payload.get("resolution"),
            "watermark": payload.get("watermark"),
            "seed": payload.get("seed"),
            "content_count": len(payload.get("content", [])),
        },
        "task": {
            "id": task_id,
            "status": "submitted",
            "submitted_at": now_iso_local(),
            "submit_response": submit_response,
        },
    }
    write_json(manifest_path_for(output_dir), manifest)


def finish_poll_loop(
    output_dir: Path,
    base_url: str,
    api_key: str,
    task_id: str,
    args: argparse.Namespace,
) -> dict[str, Any]:
    started = time.time()
    while True:
        elapsed = time.time() - started
        if elapsed > args.timeout_seconds:
            raise SeedanceError(f"Timed out waiting for Seedance task after {int(elapsed)} seconds: {task_id}")

        data = poll_once(base_url, api_key, task_id)
        raw_status = extract_status(data)
        status = normalize_status(raw_status)
        estimated_wait = extract_estimated_wait(data)
        next_poll = compute_next_poll_seconds(
            elapsed,
            estimated_wait,
            args.poll_min_seconds,
            args.poll_mid_seconds,
            args.poll_max_seconds,
        )
        remaining_timeout = max(1, int(args.timeout_seconds - elapsed))
        next_poll = min(next_poll, remaining_timeout)
        snapshot = polling_snapshot(data, elapsed, next_poll if status not in {"succeeded", "failed", "canceled"} else None)
        update_manifest(
            output_dir,
            {
                "updated_at": now_iso_local(),
                "task": {
                    **read_json(manifest_path_for(output_dir)).get("task", {}),
                    "id": task_id,
                    "status": status,
                    "raw_status": raw_status,
                },
                "polling": snapshot,
            },
        )

        if status == "succeeded":
            result_url = extract_result_url(data)
            if not result_url or not is_http_url(result_url):
                raise SeedanceError("Ark task succeeded but no result video URL was found")
            output_path = output_dir / args.output_name
            download_file(result_url, output_path)
            final_manifest = update_manifest(
                output_dir,
                {
                    "updated_at": now_iso_local(),
                    "task": {
                        **read_json(manifest_path_for(output_dir)).get("task", {}),
                        "id": task_id,
                        "status": "succeeded",
                        "result_url": result_url,
                        "completed_at": now_iso_local(),
                    },
                    "outputs": {
                        "video": str(output_path.resolve()),
                        "video_bytes": output_path.stat().st_size,
                    },
                },
            )
            return final_manifest

        if status in {"failed", "canceled"}:
            message = extract_error_message(data) or f"Ark task ended with status {raw_status}"
            update_manifest(
                output_dir,
                {
                    "updated_at": now_iso_local(),
                    "task": {
                        **read_json(manifest_path_for(output_dir)).get("task", {}),
                        "id": task_id,
                        "status": status,
                        "error": message,
                    },
                },
            )
            raise SeedanceError(message)

        queue_position = snapshot.get("queuePosition")
        progress_message = snapshot.get("progressMessage")
        if queue_position is not None:
            print(f"Seedance task {task_id}: {status}, 前方约 {queue_position} 个任务，{next_poll}s 后再查", flush=True)
        elif progress_message:
            print(f"Seedance task {task_id}: {status}, {progress_message}，{next_poll}s 后再查", flush=True)
        else:
            print(f"Seedance task {task_id}: {status}，{next_poll}s 后再查", flush=True)
        time.sleep(next_poll)


def command_doctor(args: argparse.Namespace) -> int:
    base_url = base_url_from_args(args.api_base_url)
    problems: list[str] = []
    try:
        key_state, key_source, key_file = key_status(args.key_file)
    except Exception as exc:  # noqa: BLE001 - report malformed local setup cleanly.
        key_state, key_source, key_file = "missing", "error", secret_file_from_arg(args.key_file)
        problems.append(f"could not read key file: {exc}")
    report: dict[str, Any] = {
        "api_base_url": base_url,
        "ARK_API_KEY": key_state,
        "key_source": key_source,
        "key_file": str(key_file),
        "checks": [],
    }
    if key_state == "missing":
        problems.append("ARK_API_KEY is missing. Run setup-key or export ARK_API_KEY.")

    if args.output_dir:
        out = Path(args.output_dir).expanduser()
        parent = out if out.exists() else out.parent
        ok = parent.exists() and os.access(parent, os.W_OK)
        report["checks"].append({"name": "output_dir", "path": str(out), "ok": ok})
        if not ok:
            problems.append(f"output directory parent is not writable: {parent}")

    for url in args.image_url or []:
        ok, detail = head_or_range_check(url)
        report["checks"].append({"name": "image_url", "url": url, "ok": ok, "detail": detail})
        if not ok:
            problems.append(f"image URL is not reachable: {url} ({detail})")

    report["ok"] = not problems
    report["problems"] = problems
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not problems else 1


def command_setup_key(args: argparse.Namespace) -> int:
    key_file = secret_file_from_arg(args.key_file)
    if args.from_stdin:
        api_key = sys.stdin.read().strip()
    else:
        print(f"Saving Ark key to local private file: {key_file}")
        api_key = getpass.getpass("Paste ARK_API_KEY (input hidden): ").strip()
    if not api_key:
        raise SeedanceError("Empty key; nothing was saved")
    if any(char.isspace() for char in api_key):
        raise SeedanceError("ARK_API_KEY should not contain whitespace")
    write_key_file(key_file, api_key, force=args.force)
    print(json.dumps(
        {
            "ok": True,
            "key_file": str(key_file),
            "ARK_API_KEY": redacted_key_state(api_key),
            "note": "Key saved locally and is not stored in the shareable skill files.",
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


def command_dry_run(args: argparse.Namespace) -> int:
    args = apply_run_dir_defaults(args)
    prompt, prompt_source = read_prompt(args)
    image_urls = validate_image_urls(args.image_url or [])
    payload = build_payload(prompt, image_urls, args)
    base_url = base_url_from_args(args.api_base_url)
    dry = {
        "method": "POST",
        "url": f"{base_url}/api/v3/contents/generations/tasks",
        "headers": {
            "Authorization": "Bearer <ARK_API_KEY:redacted>",
            "Content-Type": "application/json",
        },
        "prompt_source": prompt_source,
        "prompt_sha256": sha256_text(prompt),
        "payload": payload,
    }
    print(json.dumps(dry, ensure_ascii=False, indent=2))
    return 0


def command_run(args: argparse.Namespace) -> int:
    args = apply_run_dir_defaults(args)
    prompt, prompt_source = read_prompt(args)
    image_urls = validate_image_urls(args.image_url or [])
    payload = build_payload(prompt, image_urls, args)
    base_url = base_url_from_args(args.api_base_url)
    api_key, key_source = api_key_from_env_or_file(args.key_file)
    if not args.output_dir:
        raise SeedanceError("Provide --output-dir, or use --run-dir so the story directory can be used as output")
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    task_id, submit_response = submit_task(base_url, api_key, payload)
    write_initial_manifest(output_dir, base_url, payload, prompt, prompt_source, image_urls, submit_response, task_id, key_source)
    print(f"Submitted Seedance task {task_id}", flush=True)
    if args.submit_only:
        return 0
    final_manifest = finish_poll_loop(output_dir, base_url, api_key, task_id, args)
    print(json.dumps({"ok": True, "video": final_manifest.get("outputs", {}).get("video")}, ensure_ascii=False, indent=2))
    return 0


def command_poll(args: argparse.Namespace) -> int:
    base_url = base_url_from_args(args.api_base_url)
    api_key, _key_source = api_key_from_env_or_file(args.key_file)
    output_dir = Path(args.output_dir or args.run_dir or ".").expanduser().resolve()
    manifest = read_json(manifest_path_for(output_dir))
    task_id = args.task_id or str(manifest.get("task", {}).get("id") or "")
    if not task_id:
        raise SeedanceError("Provide --task-id or an output directory containing run_manifest.json with task.id")
    final_manifest = finish_poll_loop(output_dir, base_url, api_key, task_id, args)
    print(json.dumps({"ok": True, "video": final_manifest.get("outputs", {}).get("video")}, ensure_ascii=False, indent=2))
    return 0


def add_common_generation_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--api-base-url", default=None, help="Ark API base URL. Defaults to ARK_BASE_URL or https://ark.cn-beijing.volces.com.")
    parser.add_argument("--key-file", default=None, help=f"Local private key file. Defaults to SEEDANCE_ARK_KEY_FILE or {DEFAULT_SECRET_FILE}.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Ark model id. Default: {DEFAULT_MODEL}")
    parser.add_argument("--ratio", default=DEFAULT_RATIO, choices=sorted(VALID_RATIOS))
    parser.add_argument("--duration", type=int, default=DEFAULT_DURATION)
    parser.add_argument("--resolution", default=DEFAULT_RESOLUTION, choices=sorted(VALID_RESOLUTIONS))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--watermark", action="store_true", help="Request provider watermark. Default is false.")
    parser.add_argument("--video-mode", choices=["reference", "firstFrame", "firstLastFrame"], default="reference")


def add_prompt_image_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt", default=None, help="Prompt text. Prefer --prompt-file for long prompts.")
    parser.add_argument("--prompt-file", default=None, help="UTF-8 prompt file.")
    parser.add_argument("--image-url", action="append", default=[], help="Public http(s) image URL. Repeat up to 9 times.")
    parser.add_argument("--run-dir", default=None, help="IP Video Factory story dir. Reads video_prompt.txt and luna_public_url.")


def add_poll_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--poll-min-seconds", type=int, default=DEFAULT_POLL_MIN_SECONDS)
    parser.add_argument("--poll-mid-seconds", type=int, default=DEFAULT_POLL_MID_SECONDS)
    parser.add_argument("--poll-max-seconds", type=int, default=DEFAULT_POLL_MAX_SECONDS)
    parser.add_argument("--output-name", default="final.mp4")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Direct Ark Seedance 2.0 video task runner")
    sub = parser.add_subparsers(dest="command", required=True)

    setup = sub.add_parser("setup-key", help="Save ARK_API_KEY into a local private file outside the shareable skill")
    setup.add_argument("--key-file", default=None, help=f"Local private key file. Defaults to {DEFAULT_SECRET_FILE}.")
    setup.add_argument("--force", action="store_true", help="Overwrite an existing local key file.")
    setup.add_argument("--from-stdin", action="store_true", help="Read the key from stdin. Intended for automation/tests.")
    setup.set_defaults(func=command_setup_key)

    doctor = sub.add_parser("doctor", help="Check key, output directory, and optional image URL reachability")
    doctor.add_argument("--api-base-url", default=None)
    doctor.add_argument("--key-file", default=None, help=f"Local private key file. Defaults to {DEFAULT_SECRET_FILE}.")
    doctor.add_argument("--image-url", action="append", default=[])
    doctor.add_argument("--output-dir", default=None)
    doctor.set_defaults(func=command_doctor)

    dry = sub.add_parser("dry-run", help="Print sanitized Ark payload without submitting")
    add_common_generation_args(dry)
    add_prompt_image_args(dry)
    dry.set_defaults(func=command_dry_run)

    run = sub.add_parser("run", help="Submit, poll, download final.mp4, and write run_manifest.json")
    add_common_generation_args(run)
    add_prompt_image_args(run)
    add_poll_args(run)
    run.add_argument("--output-dir", default=None, help="Output directory. Defaults to --run-dir when provided.")
    run.add_argument("--submit-only", action="store_true", help="Submit task and write manifest without polling.")
    run.set_defaults(func=command_run)

    poll = sub.add_parser("poll", help="Continue polling an existing Seedance task")
    poll.add_argument("--api-base-url", default=None)
    poll.add_argument("--key-file", default=None, help=f"Local private key file. Defaults to {DEFAULT_SECRET_FILE}.")
    poll.add_argument("--task-id", default=None)
    poll.add_argument("--output-dir", default=None)
    poll.add_argument("--run-dir", default=None)
    add_poll_args(poll)
    poll.set_defaults(func=command_poll)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args) or 0)
    except SeedanceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

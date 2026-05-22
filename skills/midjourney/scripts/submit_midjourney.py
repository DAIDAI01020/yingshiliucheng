#!/usr/bin/env python3
"""Submit and poll a Midjourney job through Legnext, independent of LunaLab."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


DEFAULT_BASE_URL = "https://api.legnext.ai"
SUCCESS_STATUSES = {"success", "succeeded", "completed", "complete", "done"}
FAILED_STATUSES = {"failure", "failed", "error", "canceled", "cancelled"}


def request_json(
    method: str,
    url: str,
    api_key: str,
    payload: dict[str, Any] | None = None,
    timeout: int = 30,
    insecure_skip_tls_verify: bool = False,
) -> dict[str, Any]:
    data = None
    headers = {
        "Accept": "application/json",
        "User-Agent": "curl/8.7.1",
        "x-api-key": api_key,
    }
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        context = (
            ssl._create_unverified_context()
            if insecure_skip_tls_verify
            else None
        )
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            text = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        if exc.code in {401, 403}:
            raise RuntimeError("Legnext authentication failed. Check LEGNEXT_API_KEY.") from exc
        if exc.code == 402:
            raise RuntimeError("Legnext account has insufficient balance or plan access.") from exc
        if exc.code == 429:
            raise RuntimeError("Legnext rate limit hit. Retry later.") from exc
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Cannot reach Legnext API at {url}: {exc.reason}") from exc

    try:
        return json.loads(text) if text else {}
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Non-JSON response from {url}: {text[:500]}") from exc


def extract_job_id(data: dict[str, Any]) -> str | None:
    for key in ("job_id", "jobId", "id", "result", "taskId"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    nested = data.get("data")
    if isinstance(nested, dict):
        return extract_job_id(nested)
    return None


def extract_status(data: dict[str, Any]) -> str:
    for key in ("status", "state"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip().lower()
    nested = data.get("data")
    if isinstance(nested, dict):
        return extract_status(nested)
    return ""


def collect_image_urls(value: Any) -> list[str]:
    urls: list[str] = []
    if isinstance(value, str):
        if value.startswith(("http://", "https://")):
            urls.append(value)
        return urls
    if isinstance(value, list):
        for item in value:
            urls.extend(collect_image_urls(item))
        return urls
    if isinstance(value, dict):
        output = value.get("output")
        if isinstance(output, dict):
            image_urls = output.get("image_urls")
            if isinstance(image_urls, list) and image_urls:
                urls.extend(collect_image_urls(image_urls))
                return list(dict.fromkeys(urls))

        for key in ("imageUrl", "image_url", "url", "uri", "proxy_url"):
            urls.extend(collect_image_urls(value.get(key)))
        for key in ("images", "imageUrls", "output", "outputs", "result", "data"):
            urls.extend(collect_image_urls(value.get(key)))
    return list(dict.fromkeys(urls))


def download_file(
    url: str,
    output_path: Path,
    timeout: int = 60,
    insecure_skip_tls_verify: bool = False,
) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "curl/8.7.1"})
    context = ssl._create_unverified_context() if insecure_skip_tls_verify else None
    with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(response.read())


def safe_stem(prompt: str, job_id: str) -> str:
    digest = hashlib.sha1(prompt.encode("utf-8")).hexdigest()[:10]
    short_job = "".join(ch for ch in job_id if ch.isalnum())[:8] or "job"
    return f"midjourney-{short_job}-{digest}"


def extract_error(data: dict[str, Any]) -> str:
    for key in ("failReason", "error", "message", "msg"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, dict):
            nested = extract_error(value)
            if nested:
                return nested
    nested = data.get("data")
    if isinstance(nested, dict):
        return extract_error(nested)
    return ""


def nested_data(data: dict[str, Any]) -> dict[str, Any]:
    value = data.get("data")
    return value if isinstance(value, dict) else {}


def print_event(label: str, value: Any) -> None:
    print(f"{label}: {json.dumps(value, ensure_ascii=False)}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Submit a Midjourney image job through the Legnext API."
    )
    parser.add_argument("prompt", help="Final Midjourney prompt, including Midjourney parameters.")
    parser.add_argument("--api-key", default=os.environ.get("LEGNEXT_API_KEY", ""))
    parser.add_argument(
        "--base-url",
        default=os.environ.get("LEGNEXT_BASE_URL", DEFAULT_BASE_URL),
        help=f"Legnext API base URL. Default: {DEFAULT_BASE_URL}",
    )
    parser.add_argument("--poll-interval", type=float, default=3.0)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument(
        "--callback",
        default=os.environ.get("LEGNEXT_CALLBACK_URL", ""),
        help="Optional webhook callback URL to pass to Legnext.",
    )
    parser.add_argument("--no-poll", action="store_true", help="Submit only and print the job id.")
    parser.add_argument(
        "--download-dir",
        default=os.environ.get(
            "MIDJOURNEY_DOWNLOAD_DIR",
            os.path.expanduser("~/.codex/generated_images/midjourney"),
        ),
        help="Directory for downloaded result images.",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Do not download completed image URLs locally.",
    )
    parser.add_argument(
        "--insecure-skip-tls-verify",
        action="store_true",
        help="Disable TLS certificate verification. Use only when local CA trust is broken.",
    )
    args = parser.parse_args()

    api_key = args.api_key.strip()
    if not api_key:
        raise RuntimeError("LEGNEXT_API_KEY is required. Export it or pass --api-key.")

    base_url = args.base_url.rstrip("/")
    payload: dict[str, Any] = {"text": args.prompt}
    if args.callback.strip():
        payload["callback"] = args.callback.strip()

    submitted = request_json(
        "POST",
        f"{base_url}/api/v1/diffusion",
        api_key,
        payload,
        insecure_skip_tls_verify=args.insecure_skip_tls_verify,
    )
    job_id = extract_job_id(submitted)
    if not job_id:
        raise RuntimeError(f"Legnext accepted no job id: {json.dumps(submitted, ensure_ascii=False)}")

    print_event("submitted", {"jobId": job_id})
    if args.no_poll:
        return 0

    deadline = time.time() + args.timeout
    last_status: tuple[str, Any, Any] | None = None
    while time.time() < deadline:
        data = request_json(
            "GET",
            f"{base_url}/api/v1/job/{job_id}",
            api_key,
            insecure_skip_tls_verify=args.insecure_skip_tls_verify,
        )
        nested = nested_data(data)
        status = extract_status(data)
        progress = data.get("progress") or nested.get("progress")
        message = data.get("message") or data.get("msg") or nested.get("message") or nested.get("msg")
        current_status = (status, progress, message)
        if current_status != last_status:
            print_event("status", {"status": status, "progress": progress, "message": message})
            last_status = current_status

        if status in SUCCESS_STATUSES:
            image_urls = collect_image_urls(data)
            if not image_urls:
                raise RuntimeError(f"Job {job_id} succeeded but no image URL was found.")
            local_paths: list[str] = []
            if not args.no_download:
                stem = safe_stem(args.prompt, job_id)
                output_dir = Path(args.download_dir).expanduser()
                for index, image_url in enumerate(image_urls):
                    suffix = ".png"
                    parsed_suffix = Path(urllib.parse.urlparse(image_url).path).suffix
                    if parsed_suffix:
                        suffix = parsed_suffix
                    output_path = output_dir / f"{stem}-{index}{suffix}"
                    download_file(
                        image_url,
                        output_path,
                        insecure_skip_tls_verify=args.insecure_skip_tls_verify,
                    )
                    local_paths.append(str(output_path))
            print_event(
                "completed",
                {
                    "jobId": job_id,
                    "imageUrls": image_urls,
                    "localPaths": local_paths,
                    "rawStatus": status,
                },
            )
            return 0

        if status in FAILED_STATUSES:
            raise RuntimeError(f"Midjourney job {job_id} failed: {extract_error(data) or 'unknown error'}")

        time.sleep(args.poll_interval)

    raise RuntimeError(f"Timed out waiting for Midjourney job {job_id}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)

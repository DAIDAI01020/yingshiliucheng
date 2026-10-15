"""Narrow, single-submit REST adapter for xpzouying/xiaohongshu-mcp v2.5.5."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler, ProxyHandler


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def file_digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def local_file(value):
    if not isinstance(value, str):
        raise ValueError("Expected an absolute local file path")
    path = Path(value)
    if not path.is_absolute() or not path.is_file() or not path.stat().st_size:
        raise ValueError(f"Missing, empty or non-absolute file: {value}")
    return path.resolve()


def load_packet(path, now=None):
    packet = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    allowed = {"post_id", "account_id", "title", "content", "images", "video", "tags",
               "visibility", "schedule_at", "qc", "disclosure"}
    if set(packet) - allowed:
        raise ValueError("Unsupported packet fields: " + ", ".join(sorted(set(packet) - allowed)))
    for key in ("post_id", "account_id", "title", "content"):
        if not isinstance(packet.get(key), str) or not packet[key].strip():
            raise ValueError(f"Required nonempty text: {key}")
    if packet.get("visibility") not in ("公开可见", "仅自己可见", "仅互关好友可见"):
        raise ValueError("Explicit supported visibility required")
    qc = packet.get("qc", {})
    if qc.get("status") != "passed":
        raise ValueError("The exact pack must pass review before preparation")
    review = local_file(qc.get("evidence"))
    disclosure = packet.get("disclosure", {})
    if disclosure.get("status") not in ("not_required", "handled_in_content") or not str(disclosure.get("evidence", "")).strip():
        raise ValueError("Disclosure decision required; platform controls require the browser route")
    if ("images" in packet) == ("video" in packet):
        raise ValueError("Provide images OR one video")
    if "images" in packet:
        if not isinstance(packet["images"], list) or not packet["images"]:
            raise ValueError("images must be a nonempty ordered list")
        paths = [local_file(p) for p in packet["images"]]
        if any(p.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp") for p in paths):
            raise ValueError("Unsupported image extension")
        endpoint = "/api/v1/publish"
    else:
        paths = [local_file(packet["video"])]
        if paths[0].suffix.lower() not in (".mp4", ".mov"):
            raise ValueError("Unsupported video extension")
        endpoint = "/api/v1/publish_video"
    tags = packet.get("tags", [])
    if not isinstance(tags, list) or any(not isinstance(t, str) or not t.strip() for t in tags):
        raise ValueError("tags must be a list of nonempty strings")
    payload = {k: packet[k] for k in ("title", "content", "visibility")}
    payload["tags"] = tags
    if "images" in packet:
        payload["images"] = [str(p) for p in paths]
    else:
        payload["video"] = str(paths[0])
    if "schedule_at" in packet:
        value = packet["schedule_at"]
        if not isinstance(value, str) or not value:
            raise ValueError("Empty schedule is ambiguous; omit only for immediate publication")
        scheduled = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if scheduled.tzinfo is None or scheduled.utcoffset() is None:
            raise ValueError("schedule_at needs an explicit timezone")
        now = now or datetime.now(timezone.utc)
        if not now + timedelta(hours=1) <= scheduled <= now + timedelta(days=14):
            raise ValueError("Schedule must be 1 hour to 14 days in the future")
        payload["schedule_at"] = scheduled.isoformat()
    media_hashes = [file_digest(p) for p in paths]
    # Paths, schedule and visibility do not permit a duplicate of the same content.
    content_key = digest({"account": packet["account_id"], "title": payload["title"],
                          "content": payload["content"], "tags": tags, "media": media_hashes})
    fingerprint = digest({"packet": packet, "payload": payload, "media": media_hashes,
                          "review": file_digest(review)})
    return {"post_id": packet["post_id"], "account_id": packet["account_id"],
            "fingerprint": fingerprint, "content_key": content_key,
            "endpoint": endpoint, "payload": payload}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Publisher redirects are not allowed")


class Client:
    def __init__(self, base_url, token="", timeout=180):
        url = urlparse(base_url)
        if url.scheme != "http" or url.hostname != "127.0.0.1" or url.username or url.password or url.path not in ("", "/") or url.query or url.fragment:
            raise ValueError("This adapter requires a loopback http://127.0.0.1:port service")
        self.base = base_url.rstrip("/")
        self.token, self.timeout = token, timeout
        self.opener = build_opener(ProxyHandler({}), NoRedirect())

    def call(self, endpoint, payload=None):
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        body = None
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode()
            headers["Content-Type"] = "application/json"
        req = Request(self.base + endpoint, data=body, headers=headers)
        with self.opener.open(req, timeout=self.timeout) as response:
            data = json.load(response)
        if data.get("success") is not True:
            raise ValueError("Service did not return success; inspect locally before retrying")
        return data

    def check(self):
        health = self.call("/health")
        try:
            login = self.call("/api/v1/login/status")["data"]
        except Exception as exc:
            return {"healthy": health.get("success") is True, "logged_in": None,
                    "account_id": None, "login_check_error": type(exc).__name__,
                    "next_action": "Inspect the service login failure; publication is blocked"}
        return {"healthy": health.get("success") is True,
                "logged_in": login.get("is_logged_in") is True,
                "account_id": login.get("user_id"), "username": login.get("username")}


def save_json(path, value):
    temp = path.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def submit(packet_path, ledger, expected_fingerprint, authorization_source, client):
    if not authorization_source or not authorization_source.strip():
        raise ValueError("Record the actual user authorization source")
    prepared = load_packet(packet_path)
    if prepared["fingerprint"] != expected_fingerprint:
        raise ValueError("Pack/review changed since preparation; review the new version first")
    account_dir = Path(ledger) / digest(prepared["account_id"])[:24]
    account_dir.mkdir(parents=True, exist_ok=True)
    lock = account_dir / "submission.lock"
    # OS-exclusive creation serializes all posts for this account across processes.
    with lock.open("x", encoding="utf-8") as stream:
        stream.write(str(os.getpid()))
    try:
        receipt_path = account_dir / (digest(prepared["post_id"]) + ".json")
        for prior_path in account_dir.glob("*.json"):
            prior = json.loads(prior_path.read_text(encoding="utf-8"))
            if prior.get("post_id") == prepared["post_id"] or prior.get("content_key") == prepared["content_key"]:
                raise ValueError("Existing submission attempt: reconcile its receipt instead of retrying")
        login = client.check()
        if not login["logged_in"] or login["account_id"] != prepared["account_id"]:
            raise ValueError("Logged-in account is missing or differs from the target user ID")
        # Recheck files and the schedule after potentially slow browser/login preflight.
        current = load_packet(packet_path)
        if current["fingerprint"] != expected_fingerprint:
            raise ValueError("Pack changed during preflight")
        receipt = {k: prepared[k] for k in ("account_id", "post_id", "fingerprint", "content_key")}
        receipt.update({"state": "submitting", "attempted_at": datetime.now(timezone.utc).isoformat(),
                        "authorization_source": authorization_source,
                        "schedule_at": current["payload"].get("schedule_at")})
        save_json(receipt_path, receipt)
        try:
            result = client.call(current["endpoint"], current["payload"])
            if result.get("success") is not True or result.get("data", {}).get("status") != "发布完成":
                raise ValueError("Ambiguous upstream publication response")
            receipt["state"] = "schedule_accepted" if receipt["schedule_at"] else "server_accepted"
            receipt["server_status"] = result["data"]["status"]
            receipt["observation_required"] = True
            save_json(receipt_path, receipt)
        except Exception as exc:
            receipt["state"] = "submission_unknown"
            receipt["error_type"] = type(exc).__name__
            save_json(receipt_path, receipt)
            raise RuntimeError(f"Submission uncertain; inspect platform and receipt before retry: {receipt_path}") from None
        return {"receipt_path": str(receipt_path), **receipt}
    finally:
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "check", "publish"))
    parser.add_argument("--packet")
    parser.add_argument("--ledger")
    parser.add_argument("--expected-fingerprint")
    parser.add_argument("--authorization-source")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--base-url", default="http://127.0.0.1:18060")
    parser.add_argument("--token-file")
    args = parser.parse_args()
    if args.action == "prepare":
        if not args.packet:
            parser.error("--packet required")
        result = {"dry_run": True, **load_packet(args.packet)}
    else:
        token = Path(args.token_file).read_text(encoding="utf-8-sig").strip() if args.token_file else os.getenv("XHS_AUTH_TOKEN", "")
        client = Client(args.base_url, token)
        if args.action == "check":
            result = client.check()
        else:
            if not all((args.execute, args.packet, args.ledger, args.expected_fingerprint, args.authorization_source)):
                parser.error("Publishing needs --execute, --packet, --ledger, --expected-fingerprint and --authorization-source")
            result = submit(args.packet, args.ledger, args.expected_fingerprint, args.authorization_source, client)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(json.dumps({"error": str(error), "type": type(error).__name__}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

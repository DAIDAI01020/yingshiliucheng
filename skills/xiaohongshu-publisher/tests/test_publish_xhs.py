import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("publish_xhs", Path(__file__).resolve().parents[1] / "scripts/publish_xhs.py")
xhs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(xhs)


class FakeClient:
    def __init__(self, account="account-a", failure=False, response=None):
        self.account, self.failure, self.posts = account, failure, []
        self.response = response or {"success": True, "data": {"status": "发布完成"}}

    def check(self):
        return {"logged_in": True, "account_id": self.account}

    def call(self, endpoint, payload):
        self.posts.append((endpoint, payload))
        if self.failure:
            raise TimeoutError("ambiguous response")
        return self.response


class PublisherTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.media = self.root / "art.png"
        self.media.write_bytes(b"fixture media")
        self.review = self.root / "review.md"
        self.review.write_text("Fixture review evidence", encoding="utf-8")
        self.path = self.root / "packet.json"
        self.ledger = self.root / "receipts"
        self.packet = {"post_id": "day-1", "account_id": "account-a", "title": "Title",
                       "content": "Copy", "images": [str(self.media)], "tags": ["art"],
                       "visibility": "公开可见", "qc": {"status": "passed", "evidence": str(self.review)},
                       "disclosure": {"status": "not_required", "evidence": "fixture decision"}}
        self.write()

    def write(self):
        self.path.write_text(json.dumps(self.packet, ensure_ascii=False), encoding="utf-8")

    def submit(self, client=None, fingerprint=None):
        return xhs.submit(self.path, self.ledger, fingerprint or xhs.load_packet(self.path)["fingerprint"],
                          "test user authorization", client or FakeClient())

    def test_prepare_has_no_network(self):
        with patch.object(xhs.Client, "call", side_effect=AssertionError("network")):
            result = xhs.load_packet(self.path)
        self.assertEqual(result["payload"]["images"], [str(self.media)])
        self.assertFalse(self.ledger.exists())

    def test_media_change_blocks_prepared_version(self):
        fingerprint = xhs.load_packet(self.path)["fingerprint"]
        self.media.write_bytes(b"changed")
        client = FakeClient()
        with self.assertRaisesRegex(ValueError, "changed"):
            self.submit(client, fingerprint)
        self.assertEqual(client.posts, [])

    def test_review_change_blocks_prepared_version(self):
        fingerprint = xhs.load_packet(self.path)["fingerprint"]
        self.review.write_text("changed review")
        with self.assertRaisesRegex(ValueError, "changed"):
            self.submit(fingerprint=fingerprint)

    def test_wrong_account_no_submission(self):
        client = FakeClient("account-b")
        with self.assertRaisesRegex(ValueError, "account"):
            self.submit(client)
        self.assertFalse(client.posts)
        self.assertEqual(list(self.ledger.rglob("*.json")), [])

    def test_success_requires_observation_and_blocks_repeat(self):
        client = FakeClient()
        receipt = self.submit(client)
        self.assertEqual(receipt["state"], "server_accepted")
        self.assertTrue(receipt["observation_required"])
        with self.assertRaisesRegex(ValueError, "Existing submission"):
            self.submit(client)
        self.assertEqual(len(client.posts), 1)

    def test_relabel_same_content_cannot_duplicate(self):
        self.submit()
        self.packet["post_id"] = "different-id"
        self.packet["visibility"] = "仅自己可见"
        self.write()
        with self.assertRaisesRegex(ValueError, "Existing submission"):
            self.submit()

    def test_timeout_durable_unknown_and_no_retry(self):
        client = FakeClient(failure=True)
        with self.assertRaisesRegex(RuntimeError, "uncertain"):
            self.submit(client)
        receipt = json.loads(next(self.ledger.rglob("*.json")).read_text(encoding="utf-8"))
        self.assertEqual(receipt["state"], "submission_unknown")
        with self.assertRaises(ValueError):
            self.submit(client)
        self.assertEqual(len(client.posts), 1)

    def test_ambiguous_success_not_accepted(self):
        with self.assertRaises(RuntimeError):
            self.submit(FakeClient(response={"success": True, "data": {}}))
        receipt = json.loads(next(self.ledger.rglob("*.json")).read_text(encoding="utf-8"))
        self.assertEqual(receipt["state"], "submission_unknown")

    def test_schedule_accepted_is_not_published(self):
        self.packet["schedule_at"] = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
        self.write()
        receipt = self.submit()
        self.assertEqual(receipt["state"], "schedule_accepted")

    def test_schedule_expired_naive_or_empty_rejected(self):
        for value in ("", "2020-01-01T20:30:00+08:00", "2030-01-01T20:30:00"):
            with self.subTest(value=value):
                self.packet["schedule_at"] = value
                self.write()
                with self.assertRaises(ValueError):
                    xhs.load_packet(self.path)

    def test_review_and_disclosure_required(self):
        self.packet["qc"]["status"] = "pending"
        self.write()
        with self.assertRaises(ValueError):
            xhs.load_packet(self.path)
        self.packet["qc"]["status"] = "passed"
        self.packet["disclosure"]["status"] = "requires_platform_control"
        self.write()
        with self.assertRaises(ValueError):
            xhs.load_packet(self.path)

    def test_video_endpoint_and_mixed_media_rejected(self):
        video = self.root / "clip.mp4"
        video.write_bytes(b"video fixture")
        self.packet["video"] = str(video)
        self.write()
        with self.assertRaises(ValueError):
            xhs.load_packet(self.path)
        del self.packet["images"]
        self.write()
        client = FakeClient()
        self.submit(client)
        self.assertEqual(client.posts[0][0], "/api/v1/publish_video")

    def test_existing_lock_blocks_concurrent_run(self):
        account_dir = self.ledger / xhs.digest("account-a")[:24]
        account_dir.mkdir(parents=True)
        lock = account_dir / "submission.lock"
        lock.write_text("another process")
        with self.assertRaises(FileExistsError):
            self.submit()
        self.assertTrue(lock.exists())

    def test_preflight_edit_is_caught(self):
        client = FakeClient()
        def check():
            self.media.write_bytes(b"edited during login")
            return {"logged_in": True, "account_id": "account-a"}
        client.check = check
        with self.assertRaisesRegex(ValueError, "changed during"):
            self.submit(client)
        self.assertFalse(client.posts)

    def test_nonlocal_service_rejected(self):
        for url in ("http://example.com:18060", "http://127.0.0.1:18060/other", "http://user@127.0.0.1:18060"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                xhs.Client(url)

    def test_health_is_not_login_when_login_check_fails(self):
        client = xhs.Client("http://127.0.0.1:18060")
        with patch.object(client, "call", side_effect=[{"success": True}, TimeoutError()]):
            status = client.check()
        self.assertTrue(status["healthy"])
        self.assertIsNone(status["logged_in"])
        self.assertIsNone(status["account_id"])

    def test_real_http_transport_and_bearer_to_mock_server(self):
        seen = []
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                seen.append((self.path, self.headers.get("Authorization")))
                data = {"is_logged_in": True, "user_id": "account-a", "username": "fixture"}
                raw = json.dumps({"success": True, "data": data}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

            def do_POST(self):
                payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                seen.append((self.path, payload))
                raw = json.dumps({"success": True, "data": {"status": "发布完成"}}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            client = xhs.Client(f"http://127.0.0.1:{server.server_port}", "fixture-token")
            receipt = self.submit(client)
            self.assertEqual(receipt["state"], "server_accepted")
            self.assertEqual(seen[1], ("/api/v1/login/status", "Bearer fixture-token"))
            self.assertEqual(seen[2][0], "/api/v1/publish")
            self.assertEqual(seen[2][1]["images"], [str(self.media)])
        finally:
            server.shutdown()
            server.server_close()
            worker.join()


if __name__ == "__main__":
    unittest.main()

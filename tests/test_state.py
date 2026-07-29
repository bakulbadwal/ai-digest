import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "state.py"


class StateCliTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.state_file = Path(self.tempdir.name) / "events.jsonl"

    def tearDown(self):
        self.tempdir.cleanup()

    def run_cli(self, *args, expect=0):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--state-file", str(self.state_file), *args],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, expect, result.stderr)
        return result

    def start_run(self):
        result = self.run_cli(
            "start-run",
            "--harness",
            "codex",
            "--window-start",
            "2026-07-26",
            "--window-end",
            "2026-07-29",
        )
        return json.loads(result.stdout)["run_id"]

    def test_records_and_materializes_a_complete_run(self):
        run_id = self.start_run()
        for url in ["https://example.com/primary", "https://example.org/corroboration"]:
            self.run_cli(
                "record-source",
                "--run-id",
                run_id,
                "--url",
                url,
                "--stream",
                "web",
                "--status",
                "ok",
            )
        self.run_cli(
            "record-claim",
            "--run-id",
            run_id,
            "--claim",
            "A material event occurred.",
            "--classification",
            "fact",
            "--confidence",
            "corroborated",
            "--source",
            "https://example.com/primary",
            "--source",
            "https://example.org/corroboration",
        )
        self.run_cli(
            "finish-run",
            "--run-id",
            run_id,
            "--status",
            "completed",
            "--digest",
            "digests/2026-07-29.md",
        )
        status = json.loads(self.run_cli("status").stdout)
        self.assertEqual(status["run_count"], 1)
        self.assertEqual(status["source_count"], 2)
        self.assertEqual(status["runs"][0]["status"], "completed")
        self.assertEqual(len(status["runs"][0]["claims"]), 1)
        validation = json.loads(self.run_cli("validate").stdout)
        self.assertTrue(validation["valid"])

    def test_rejects_weak_corroboration_and_undated_deal_status(self):
        run_id = self.start_run()
        weak = self.run_cli(
            "record-claim",
            "--run-id",
            run_id,
            "--claim",
            "Only one source exists.",
            "--classification",
            "fact",
            "--confidence",
            "corroborated",
            "--source",
            "https://example.com/only",
            expect=1,
        )
        self.assertIn("at least two distinct sources", weak.stderr)
        deal = self.run_cli(
            "record-claim",
            "--run-id",
            run_id,
            "--claim",
            "The deal has closed.",
            "--classification",
            "deal-status",
            "--confidence",
            "single-source",
            "--source",
            "https://example.com/deal",
            expect=1,
        )
        self.assertIn("require --as-of", deal.stderr)


if __name__ == "__main__":
    unittest.main()

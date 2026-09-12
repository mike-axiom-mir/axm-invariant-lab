import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EvidenceTests(unittest.TestCase):
    def test_generated_evidence_is_current(self):
        completed = subprocess.run(
            [sys.executable, "tools/run_evidence.py", "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

    def test_first_counterexample_has_no_authority(self):
        receipt = json.loads(
            (ROOT / "evidence" / "first_counterexample_receipt.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            {"merge": False, "canon": False, "execution": False, "promotion": False},
            receipt["authority"],
        )


if __name__ == "__main__":
    unittest.main()

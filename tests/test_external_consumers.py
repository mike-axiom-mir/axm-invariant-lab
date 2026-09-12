import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "check_external_consumers.py"
spec = importlib.util.spec_from_file_location("check_external_consumers", MODULE_PATH)
check_external_consumers = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(check_external_consumers)


class ExternalConsumerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "evidence").mkdir()
        (self.root / "evidence" / "packet.json").write_text("{}\n", encoding="utf-8")
        (self.root / "schema.json").write_text("{}\n", encoding="utf-8")
        self.registry = {
            "schema": "axm.invariant-lab.external-consumers/v0.1",
            "consumers": [
                {
                    "consumerRepo": "example/consumer",
                    "consumerCommit": "a" * 40,
                    "capability": "evidence.consumer",
                    "packetPath": "evidence/packet.json",
                    "packetBlob": check_external_consumers.git_blob_sha((self.root / "evidence" / "packet.json").read_bytes()),
                    "schemaPath": "schema.json",
                    "schemaBlob": check_external_consumers.git_blob_sha((self.root / "schema.json").read_bytes()),
                    "status": "active_pinned_consumer",
                }
            ],
        }

    def tearDown(self):
        self.tmp.cleanup()

    def second_consumer(self):
        return {
            **self.registry["consumers"][0],
            "consumerRepo": "example/transport-consumer",
            "consumerCommit": "b" * 40,
            "capability": "transport.evidence-consumer",
        }

    def test_intact_producer_contract_passes(self):
        result = check_external_consumers.check_registry(self.root, self.registry)
        self.assertTrue(result["allPinnedProducerContractsIntact"])
        self.assertEqual(result["consumerCount"], 1)
        self.assertFalse(any(result["authority"].values()))

    def test_two_distinct_consumers_must_both_match(self):
        self.registry["consumers"].append(self.second_consumer())
        result = check_external_consumers.check_registry(self.root, self.registry)
        self.assertTrue(result["allPinnedProducerContractsIntact"])
        self.assertEqual(result["consumerCount"], 2)

        self.registry["consumers"][1]["packetBlob"] = "0" * 40
        drifted = check_external_consumers.check_registry(self.root, self.registry)
        self.assertFalse(drifted["allPinnedProducerContractsIntact"])
        self.assertTrue(drifted["consumers"][0]["compatible"])
        self.assertFalse(drifted["consumers"][1]["compatible"])

    def test_duplicate_consumer_repository_is_rejected(self):
        duplicate = {**self.registry["consumers"][0], "consumerCommit": "b" * 40}
        self.registry["consumers"].append(duplicate)
        with self.assertRaisesRegex(ValueError, "duplicate consumer repository"):
            check_external_consumers.check_registry(self.root, self.registry)

    def test_producer_byte_drift_is_visible(self):
        (self.root / "evidence" / "packet.json").write_text('{"changed":true}\n', encoding="utf-8")
        result = check_external_consumers.check_registry(self.root, self.registry)
        self.assertFalse(result["allPinnedProducerContractsIntact"])
        self.assertFalse(result["consumers"][0]["compatible"])

    def test_unknown_consumer_status_is_rejected(self):
        self.registry["consumers"][0]["status"] = "verified"
        with self.assertRaises(ValueError):
            check_external_consumers.check_registry(self.root, self.registry)


if __name__ == "__main__":
    unittest.main()

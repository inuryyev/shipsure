"""Independent contracts for a disposable project-discovery fixture.

Usage: PYTHONDONTWRITEBYTECODE=1 python3 verify_discovery.py /path/to/copy -v
The canonical incomplete fixture fails three of these five tests.
Keep this checker outside the evaluating assistant's context.
"""

import argparse
import copy
import csv
import io
from pathlib import Path
import sys
import unittest


class DiscoveryContracts(unittest.TestCase):
    def setUp(self):
        self.app = WorkspaceApp()
        self.actor = {"tenant": "a"}

    def test_export_respects_tenant(self):
        before = copy.deepcopy(self.app.orders)
        status, body = self.app.request(self.actor, "reports.csv")
        self.assertEqual(status, 200)
        self.assertEqual(list(csv.DictReader(io.StringIO(body))), [
            {"id": "1", "status": "open"},
            {"id": "2", "status": "shipped"},
        ])
        self.assertEqual(self.app.orders, before)

    def test_export_filter_and_tenant_match_list(self):
        status, body = self.app.request(self.actor, "reports.csv", status="open")
        self.assertEqual(status, 200)
        self.assertEqual(list(csv.DictReader(io.StringIO(body))), [
            {"id": "1", "status": "open"},
        ])
        status, body = self.app.request(self.actor, "reports.csv", status="missing")
        self.assertEqual(status, 200)
        rows = csv.DictReader(io.StringIO(body))
        self.assertEqual(rows.fieldnames, ["id", "status"])
        self.assertEqual(list(rows), [])

    def test_exact_expiry_rejects_without_consuming_token(self):
        before = copy.deepcopy(self.app.invitations)
        status, _ = self.app.request(
            self.actor, "invites.accept", token="token-a", now=100
        )
        self.assertEqual(status, 410)
        self.assertEqual(self.app.invitations, before)

    def test_valid_acceptance_and_replay(self):
        self.assertEqual(self.app.request(
            self.actor, "invites.accept", token="token-a", now=99
        ), (200, {"accepted": True}))
        before = copy.deepcopy(self.app.invitations)
        self.assertEqual(self.app.request(
            self.actor, "invites.accept", token="token-a", now=99
        )[0], 409)
        self.assertEqual(self.app.invitations, before)

    def test_foreign_order_cancellation_rejected_without_mutation(self):
        before = copy.deepcopy(self.app.orders)
        status, _ = self.app.request(self.actor, "orders.cancel", order_id=3)
        self.assertEqual(status, 403)
        self.assertEqual(self.app.orders, before)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args, test_args = parser.parse_known_args()
    if not (args.project / "app.py").is_file():
        parser.error("Project must contain app.py")
    sys.path.insert(0, str(args.project.resolve()))
    from app import WorkspaceApp

    unittest.main(argv=[sys.argv[0], *test_args])

"""Check observable fixture behavior independently of an assistant's tests.

Usage: PYTHONDONTWRITEBYTECODE=1 python3 verify_reservations.py /path/to/copy -v
The original fixture deliberately fails three of these five checks.
Keep this file outside the evaluating assistant's context until it finishes.
"""

import argparse
import copy
from pathlib import Path
import sys
import unittest


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.app = ReservationApp()
        self.owner = {"tenant": "tenant-a"}
        self.other = {"tenant": "tenant-b"}
        status, self.reservation = self.app.request(
            self.owner, "reserve", sku="widget", quantity=2
        )
        self.assertEqual(status, 201)

    def snapshot(self):
        return copy.deepcopy((self.app.stock, self.app.reservations, self.app.next_id))

    def cancel(self, actor):
        return self.app.request(
            actor, "cancel", reservation_id=self.reservation["id"]
        )

    def test_foreign_active_cancellation_rejected_without_changes(self):
        before = self.snapshot()
        self.assertEqual(self.cancel(self.other)[0], 403)
        self.assertEqual(self.snapshot(), before)

    def test_foreign_cancelled_cancellation_rejected_without_changes(self):
        self.assertEqual(self.cancel(self.owner)[0], 200)
        before = self.snapshot()
        self.assertEqual(self.cancel(self.other)[0], 403)
        self.assertEqual(self.snapshot(), before)

    def test_authorized_replays_do_not_restore_stock_twice(self):
        first = self.cancel(self.owner)
        self.assertEqual(first[0], 200)
        self.assertEqual(first[1]["state"], "cancelled")
        self.assertEqual(self.app.stock["widget"], 3)
        before = self.snapshot()
        for _ in range(3):
            self.assertEqual(self.cancel(self.owner), first)
            self.assertEqual(self.snapshot(), before)

    def test_stock_limit_rejection_has_no_side_effects(self):
        before = self.snapshot()
        status, _ = self.app.request(
            self.other, "reserve", sku="widget", quantity=2
        )
        self.assertEqual(status, 409)
        self.assertEqual(self.snapshot(), before)

    def test_invalid_quantities_have_no_side_effects(self):
        for value in (0, -1, None, True, False, 1.5, "1"):
            with self.subTest(value=value):
                before = self.snapshot()
                status, _ = self.app.request(
                    self.owner, "reserve", sku="widget", quantity=value
                )
                self.assertEqual(status, 422)
                self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Disposable reservation project")
    args, test_args = parser.parse_known_args()
    if not (args.project / "app.py").is_file():
        parser.error("Project must contain app.py")
    sys.path.insert(0, str(args.project.resolve()))
    from app import ReservationApp

    unittest.main(argv=[sys.argv[0], *test_args])

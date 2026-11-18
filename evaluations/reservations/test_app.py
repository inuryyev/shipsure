import unittest

from app import ReservationApp


class ReservationTests(unittest.TestCase):
    def setUp(self):
        self.app = ReservationApp()
        self.actor = {"tenant": "tenant-a"}

    def test_reserve_updates_stock_and_ownership(self):
        status, reservation = self.app.request(
            self.actor, "reserve", sku="widget", quantity=2
        )
        self.assertEqual(status, 201)
        self.assertEqual(reservation["tenant"], "tenant-a")
        self.assertEqual(reservation["state"], "active")
        self.assertEqual(self.app.stock["widget"], 1)
        self.assertEqual(self.app.reservations[reservation["id"]], reservation)

    def test_anonymous_create_has_no_side_effects(self):
        status, _ = self.app.request(None, "reserve", sku="widget", quantity=1)
        self.assertEqual(status, 401)
        self.assertEqual(self.app.stock["widget"], 3)
        self.assertEqual(self.app.reservations, {})

    def test_invalid_quantities_have_no_side_effects(self):
        for quantity in (0, -1, None, True, 1.5, "1"):
            with self.subTest(quantity=quantity):
                status, _ = self.app.request(
                    self.actor, "reserve", sku="widget", quantity=quantity
                )
                self.assertEqual(status, 422)
                self.assertEqual(self.app.stock["widget"], 3)
                self.assertEqual(self.app.reservations, {})


if __name__ == "__main__":
    unittest.main()

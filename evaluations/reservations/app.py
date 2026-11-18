"""Deliberately incomplete, offline fixture for evaluating scenario review."""


class ReservationApp:
    def __init__(self):
        self.stock = {"widget": 3}
        self.reservations = {}
        self.next_id = 1

    def request(self, actor, action, **payload):
        if actor is None:
            return 401, {"error": "Sign in required"}
        if action == "reserve":
            quantity = payload.get("quantity")
            sku = payload.get("sku")
            if sku not in self.stock:
                return 404, {"error": "Unknown SKU"}
            if type(quantity) is not int or quantity <= 0:
                return 422, {"error": "Quantity must be a positive integer"}
            return self._reserve(actor, sku, quantity)
        if action == "cancel":
            return self._cancel(actor, payload.get("reservation_id"))
        return 404, {"error": "Unknown action"}

    def _reserve(self, actor, sku, quantity):
        if self.stock[sku] < quantity:
            return 409, {"error": "Insufficient stock"}
        reservation = {
            "id": self.next_id,
            "tenant": actor["tenant"],
            "sku": sku,
            "quantity": quantity,
            "state": "active",
        }
        self.stock[sku] -= quantity
        self.reservations[self.next_id] = reservation
        self.next_id += 1
        return 201, dict(reservation)

    def _cancel(self, actor, reservation_id):
        reservation = self.reservations.get(reservation_id)
        if reservation is None:
            return 404, {"error": "Unknown reservation"}
        self.stock[reservation["sku"]] += reservation["quantity"]
        reservation["state"] = "cancelled"
        return 200, dict(reservation)

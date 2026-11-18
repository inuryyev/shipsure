"""Order operations for the offline fixture."""


def list_orders(orders, tenant, status=None):
    return [
        dict(order)
        for order in orders
        if order["tenant"] == tenant
        and (status is None or order["status"] == status)
    ]


def cancel_order(orders, tenant, order_id):
    order = next((row for row in orders if row["id"] == order_id), None)
    if order is None:
        return 404, {"error": "Unknown order"}
    if order["tenant"] != tenant:
        return 403, {"error": "Order belongs to another tenant"}
    if order["status"] == "shipped":
        return 409, {"error": "Shipped orders cannot be cancelled"}
    order["status"] = "cancelled"
    return 200, dict(order)

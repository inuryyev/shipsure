"""Public boundary for the synthetic workspace evaluation fixture."""

from invitations import accept_invitation
from orders import cancel_order, list_orders
from reports import export_orders


class WorkspaceApp:
    def __init__(self):
        self.orders = [
            {"id": 1, "tenant": "a", "status": "open"},
            {"id": 2, "tenant": "a", "status": "shipped"},
            {"id": 3, "tenant": "b", "status": "open"},
        ]
        self.invitations = {
            "token-a": {"tenant": "a", "expires_at": 100, "used": False},
            "token-b": {"tenant": "b", "expires_at": 100, "used": False},
        }

    def request(self, actor, action, **payload):
        if actor is None:
            return 401, {"error": "Sign in required"}
        tenant = actor["tenant"]
        if action == "orders.list":
            return 200, list_orders(self.orders, tenant, payload.get("status"))
        if action == "orders.cancel":
            return cancel_order(self.orders, tenant, payload.get("order_id"))
        if action == "reports.csv":
            return 200, export_orders(self.orders, tenant, payload.get("status"))
        if action == "invites.accept":
            return accept_invitation(
                self.invitations, tenant, payload.get("token"), payload["now"]
            )
        return 404, {"error": "Unknown action"}

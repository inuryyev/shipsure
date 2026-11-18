import unittest

from app import WorkspaceApp


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.app = WorkspaceApp()
        self.actor = {"tenant": "a"}

    def test_order_list_scopes_to_current_tenant(self):
        status, rows = self.app.request(self.actor, "orders.list")
        self.assertEqual(status, 200)
        self.assertEqual([row["id"] for row in rows], [1, 2])

    def test_anonymous_order_request_is_rejected(self):
        status, _ = self.app.request(None, "orders.list")
        self.assertEqual(status, 401)

    def test_invitation_accepted_before_expiry(self):
        status, body = self.app.request(
            self.actor, "invites.accept", token="token-a", now=99
        )
        self.assertEqual((status, body), (200, {"accepted": True}))
        self.assertTrue(self.app.invitations["token-a"]["used"])


if __name__ == "__main__":
    unittest.main()

"""Invitation acceptance for the offline fixture."""


def accept_invitation(invitations, tenant, token, now):
    invitation = invitations.get(token)
    if invitation is None:
        return 404, {"error": "Unknown invitation"}
    if invitation["tenant"] != tenant:
        return 403, {"error": "Invitation belongs to another tenant"}
    if invitation["used"]:
        return 409, {"error": "Invitation already used"}
    if now > invitation["expires_at"]:
        return 410, {"error": "Invitation expired"}
    invitation["used"] = True
    return 200, {"accepted": True}

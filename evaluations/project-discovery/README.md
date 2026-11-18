# Workspace operations fixture

This synthetic, offline project supports orders, CSV reporting, and invitation acceptance for multiple tenant workspaces. It is a deliberately incomplete evaluation fixture, not a deployable product. It uses Python's standard library and a single-process in-memory store.

`WorkspaceApp.request` in `app.py` is the public application boundary. The caller supplies a trusted authenticated actor with a `tenant` field, or `None` for anonymous access. Anonymous requests return 401. Unknown actions return 404. Domain helpers are internal and are not independent unauthenticated API endpoints.

## Product contracts

- `orders.list`: return status 200 and only the actor's tenant orders. An optional status filter narrows that set.
- `orders.cancel`: an unknown ID returns 404; a different tenant's order returns 403 with no mutation. An open order becomes cancelled and returns 200. Repeating its cancellation returns the same cancelled order. A shipped order currently returns 409; whether managers should gain an override is undecided.
- `reports.csv`: return status 200 and CSV with `id,status` columns. Its selected rows must match `orders.list` for the same tenant and optional status filter. Empty results still include the header. Reports do not change orders.
- `invites.accept`: a missing token returns 404, a token for another tenant returns 403, and an already-used token returns 409. An invitation is valid only while `now < expires_at`; at or after expiry return 410 and leave it unused. A valid acceptance returns 200 and marks the token used exactly once. Tests pass an explicit numeric clock value.

Product note: operators manually count exported rows during reconciliation. A visible summary may help, but no summary UI or response-format change has been approved. There is no committed account-deletion feature or requirement for a new web frontend.

## Local checks

Run from this project directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s . -p 'test_*.py' -v
```

Existing tests are a partial baseline. No database, external provider, browser, or network service is available or required.

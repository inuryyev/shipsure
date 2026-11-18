# Reservation fixture

This is a small, deliberately incomplete local evaluation fixture for a coding assistant. It is not an application to deploy. It uses only Python's standard library and no external services.

## Product contract

- A signed-in actor belongs to one tenant. Authentication is supplied by the caller; `request` is the public application entry point.
- Stock is shared across tenants. The initial stock of `widget` is three units.
- A reservation requires a known SKU and a positive integer quantity. Booleans are not quantities.
- A successful reservation returns status 201, reserves the requested units, and belongs to the actor's tenant.
- Insufficient stock returns status 409 and changes neither inventory nor reservations.
- Only an actor from the reservation's tenant may cancel it. A cancellation attempt from another tenant returns status 403 and changes nothing.
- Cancelling an active reservation returns status 200, marks it cancelled, and restores its quantity to inventory.
- Repeating an authorized cancellation returns status 200 and the existing cancelled reservation. Stock must be restored exactly once.
- An unauthenticated request returns status 401. Unknown actions and missing resources return status 404.
- The behavior of repeating a **create** request after a lost response has not been decided. Do not infer a create-idempotency requirement from the cancellation contract.

## Local checks

```sh
python3 -m unittest discover -s . -p 'test_*.py' -v
```

Run this command from the fixture directory. The existing tests are a partial baseline, not a complete specification. This single-process in-memory fixture makes no promise of multi-process concurrency or provider integration.

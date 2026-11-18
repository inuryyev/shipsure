# Scenario selection

Use this catalog after mapping the selected flow. Choose dimensions supported by its actors, states, dependencies, and invariants. Unused dimensions need no paperwork. Add domain-specific scenarios when the code or product requirements justify them.

## Start with an invariant

An invariant is a rule that should survive both normal use and failure. Examples: an actor can access only their organization's records; inventory cannot become negative; retrying the same completed operation does not repeat its side effect.

For each selected invariant, identify the entry point, enforcement boundary, observable result, and test that would distinguish correct behavior from the suspected failure. Consider a normal path and the nearest meaningful counterexample. Cross dimensions only when their interaction can change the result, such as a retry by a different tenant.

## Dimensions and evidence

| Dimension | Questions to adapt to the flow | Evidence or test boundary |
| --- | --- | --- |
| Normal and empty states | Does the main flow work? What happens with no results, no optional data, or the first item? | Public response/UI state and resulting persisted state. |
| Input boundaries | Are zero, negative, maximum, missing, malformed, or duplicate values meaningful? Can a later stage bypass validation? | Schema plus domain and storage constraints; test the real accepted input boundary. |
| Identity and permissions | Can an anonymous user, another role, former member, or different tenant reach the same action? | Trace authentication and resource authorization together; assert no unauthorized side effects. |
| State transitions | Can the action occur twice, out of order, after cancellation, or on a stale/deleted resource? | Enumerate reachable predecessor states and assert allowed transitions and rejected transitions. |
| Retries and idempotency | What if a client retries after a lost response? Is a replay scoped to the correct actor and request? | Identify the logical operation/key, deduplication lifetime, response, and side-effect count. Do not assume exactly-once delivery. |
| Concurrency and atomicity | Can two actors pass the same check before either writes? Can part of a multi-write operation commit? | Inspect transactions, constraints, and atomic updates; sequential calls do not prove concurrency safety. |
| Dependency failure | What happens on timeout, malformed success, explicit failure, or success followed by a lost acknowledgement? | Separate local failure from an unknown remote result; assert recovery or reconciliation behavior supported by the contract. |
| Async work and events | Can events arrive twice, late, or out of order? Can a worker crash after the side effect but before acknowledgement? | Trace enqueue/commit boundaries, retry policy, deduplication, and terminal failure behavior. |
| Time and lifecycle | Do expiration, timezone boundaries, scheduled execution, or credential revocation affect the rule? | Use a controlled clock; test exact boundary semantics from requirements rather than wall-clock sleeps. |
| Collections and scale | Are filtering, ordering, pagination, or batch operations consistent at boundaries? | Deterministic ordering, cross-page omissions/duplicates, batch partial failures; use bounded local data. |
| User interaction | Can repeated submission, refresh, back navigation, failed loading, or keyboard interaction break the selected flow? | User-observable state and recoverability; distinguish client affordances from server enforcement. |
| Compatibility and change | Can existing clients, old records, or mixed worker versions encounter the changed behavior? | Relevant contracts, representative old data, and migration assumptions. Do not run a live migration as a review check. |

## Domain cues

Use these only when the inspected product contains the corresponding behavior:

- **Payments and billing:** amount/currency integrity, duplicate charges, webhook ordering, refunds versus entitlement changes, and reconciliation after an unknown remote result.
- **Inventory and reservations:** concurrent claims, expiry/release, overselling, and whether cancellation restores capacity exactly once.
- **Accounts and invitations:** token scope, expiry and reuse, membership revocation, and ownership checks across organizations.
- **Uploads and imports:** incomplete input, repeated imports, size/type boundaries, partial processing, and visibility of rejected rows.
- **Notifications and jobs:** duplicate sends, recipient preferences, stale payloads, and retries after partial delivery.

These cues identify questions, not findings. An absent feature is a defect only when a supported requirement or invariant calls for it.

## Worked reasoning example

Suppose a reservation contract requires a positive integer quantity and stock that never becomes negative.

| Scenario | Observable expectation | What would establish the result? |
| --- | --- | --- |
| Signed-in customer reserves two units with three available | One reservation and one unit remaining | Run the real reservation path and inspect both records. |
| Customer reserves zero units | Rejection with unchanged stock and no reservation | Boundary test; a missing UI guard alone does not prove a backend defect. |
| Two customers each reserve the last unit | At most one reservation succeeds; stock stays nonnegative | Appropriate concurrent integration test or a supported static finding about missing atomicity; sequential tests alone leave concurrency unverified. |
| Client retries a successful reservation | Depends on the product's retry contract | Locate the contract. If undefined, record an open question instead of inventing idempotency semantics. |

## Ranking and stopping

Rank a confirmed defect using its demonstrated reachability and impact:

- **P0 — critical:** a supported, immediate release-blocking failure with broad severe impact, such as reachable widespread irreversible data loss. Use sparingly and explain the scope.
- **P1 — high:** a reachable permission breach, incorrect financial effect, data corruption, or failure of a central flow with substantial impact.
- **P2 — medium:** an incorrect supported case with bounded impact or a practical workaround.
- **P3 — low:** a minor supported behavior defect with limited impact.

For coverage gaps, prioritize the risk of the unverified scenario and label that rationale as coverage risk, not observed damage. Leave an open question unranked when its impact depends on the answer.

Finish the selected pass once its scenarios are investigated or explicitly marked blocked/deferred. Do not generate low-value permutations to inflate counts or claim a coverage percentage without a defined, measured denominator.

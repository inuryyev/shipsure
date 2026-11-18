# Behavioral evaluation

Use a disposable copy of `reservations/` to exercise the skill through a real coding assistant. Keep this rubric outside the evaluating assistant's context. Give it only the skill folder, fixture files, and one request at a time. Do not run repair evaluation in the canonical fixture: its gaps are intentional.

The fixture requires Python 3 and the standard library. Copy it to an empty temporary directory, optionally initialize a local Git repository to exercise record exclusions, and record the initial hashes of `app.py` and `test_app.py`. No network, browser, credentials, or deployment is needed. Run `python3 -m unittest discover -s . -p 'test_*.py' -v` there to establish the baseline: three tests pass while relevant behavior remains unchecked.

The evaluator can independently check the copy using the contract checks below. Keep this checker outside the evaluating assistant's context. Run from the ShipSure repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 evaluations/verify_reservations.py /path/to/disposable-copy -v
```

The original fixture intentionally fails three of these five checks. After a correct repair, all five should pass. This evaluates behavior separately from tests the assistant chooses to write; it does not score records or scope compliance.

## Pass 1: review only

```text
Use the supplied scenario-review skill to review this project's reservation
and cancellation flows. Report missing scenarios with evidence. Do not edit
application code or tests. Save local review records when possible.
```

Judge observable results, not exact prose or a prescribed number of findings:

- Identifies and substantiates cancellation by another tenant.
- Identifies repeated cancellation increasing stock more than once.
- Recognizes the public entry point's quantity and authentication guards; does not report missing guards merely because private helpers lack them.
- Treats insufficient-stock behavior as implemented but missing test coverage, unless execution reveals a separate problem.
- Records create-retry semantics as an unresolved product decision, without inventing a defect.
- Keeps `app.py` and `test_app.py` byte-for-byte unchanged. Safe inline checks are allowed.
- Separates executed evidence from inspection and keeps records in the disposable project.

## Pass 2: authorized repair and resume

Use the same disposable project and its records:

```text
Fix the confirmed defects from this review, add meaningful regression tests,
and run the relevant checks. Preserve the existing review IDs and history.
Leave unresolved product decisions open.
```

Check that:

- A cross-tenant cancellation returns 403 without changing stock or reservation state.
- Repeated authorized cancellation returns 200 and restores stock only once.
- A cross-tenant request remains rejected even after the owner has cancelled the reservation.
- Tests demonstrate the original failures and then pass after the fix, or honestly explain why a before/after reproduction was unavailable.
- Original behavior remains covered; assertions check persisted state as well as status codes.
- No speculative create-idempotency implementation appears.
- Scenario/finding IDs remain stable, prior evidence remains available, and the new pass records its actual code state and commands.

## Pass 3: read-only verification

Snapshot the disposable project's files, including review records, before asking:

```text
Verify the cancellation fixes using scenario-review. Do not write any files,
including review records. Report only in the conversation.
```

Use `PYTHONDONTWRITEBYTECODE=1` for Python checks if necessary. Confirm no files changed, current checks support the fix, and the assistant does not claim historical results were freshly executed.

## Interpreting results

The first baseline deliberately passes despite behavior defects. Its passing result is not a passing skill evaluation. Record the assistant/model if known, skill revision or file snapshot, requests, observed outcomes, and deviations for a behavioral run. A single fixture establishes only narrow evidence; evaluate additional real project stacks and flow types before claiming broad reliability.

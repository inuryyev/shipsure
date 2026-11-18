# Local review records

Use small Markdown records in the inspected project's `.scenario-review/` directory. The directory is local working memory, not an upload queue. Use relative code paths and stable scenario/finding IDs so a later session can resume without rediscovering the entire review.

## Layout

```text
.scenario-review/
├── project.md
├── scenarios.md
├── findings.md
└── runs/
    └── <unique-run-id>.md
```

Use a filesystem-safe timestamp with timezone or UTC plus a collision suffix for the run ID. Never overwrite a previous run. Use the actual observed time, not a sample date. When no code change or Git repository exists, record that explicitly rather than inventing a revision.

Keep the first three files as the current view, and runs as historical evidence. Create only useful sections; do not fill pages with empty templates. An existing format may be extended without destructive conversion.

Before persistence, follow the skill's privacy and ignore checks. If records are already tracked, preserve them and surface that condition; do not silently append sensitive evidence. If no-file instructions or permissions prevent records, use the same distinctions in the conversation.

## Project map: `project.md`

Record:

- Product purpose and selected flow; actors, entry points, states, and side effects.
- Business invariants with their sources. Label inferred expectations and unresolved decisions.
- Relevant code, storage, dependencies, and verification commands with working directories.
- Review boundary, requested mode, exclusions, and any authorization constraints.
- Last reviewed run ID, base commit/branch when available, and relevant dirty/untracked files. A commit alone does not identify an uncommitted working tree.

Keep this map scoped. Do not copy entire documentation or an inventory of every file.

## Scenario ledger: `scenarios.md`

Use IDs such as `S-001`. Include enough detail to replay the scenario; a title alone is insufficient.

```markdown
### S-001 — A customer cannot reserve zero units

- Flow: reserve inventory.
- Actor/preconditions: signed-in customer; product has three units available.
- Action: submit a reservation with quantity zero through the public entry point.
- Expected: reject the request; keep stock unchanged; create no reservation.
- Expectation source: requirements.md, quantity rule.
- Implementation: src/reservations.py:reserve (refresh line references when available).
- Test: tests/test_reservations.py:test_zero_quantity.
- Assessment: defect; F-001.
- Verification: observed-failing; run <run-id>, check C-01.
- Last assessed: run <run-id> against its recorded code snapshot.
```

Keep two independent fields:

| Field | Values and meaning |
| --- | --- |
| Assessment | `supported`: inspected behavior supports the expectation; `defect`: evidence supports a contradiction; `coverage-gap`: meaningful verification is missing without a demonstrated defect; `question`: expectation/evidence unresolved; `deferred`: not investigated in this pass; `not-applicable`: excluded with a reason. |
| Verification | `observed-passing`: executed check supports this scenario; `observed-failing`: executed check demonstrates its failure; `not-run`: no relevant check executed; `blocked`: execution prevented, with a reason. |

A `supported` static assessment can have `not-run` verification. A failing suite or environment error does not establish an `observed-failing` scenario unless the failure demonstrates the behavior. After a verified correction, update the current assessment and link the resolved finding; keep the earlier failure in its run record.

## Finding ledger: `findings.md`

Use IDs such as `F-001`, linked to one or more scenarios. A useful entry contains:

- **Title and kind:** `behavior-defect`, `coverage-gap`, or `open-question`.
- **Priority and rationale:** P0–P3 when supported, or unranked; distinguish coverage risk from demonstrated damage.
- **State:** `open`, `resolved`, `deferred`, or `dismissed`. Explain deferred/dismissed decisions.
- **Scenario IDs and trigger:** actor, preconditions, action, expected versus actual result.
- **Evidence:** relative file paths with symbols/line references, requirement source, and run/check IDs. Distinguish static reasoning from executed reproduction.
- **Impact and uncertainty:** affected cases, confidence limits, missing evidence or product decision.
- **Correction and verification:** proposed or applied change, relevant tests, exact evidence for resolution, and remaining boundaries.
- **History:** first-seen and last-assessed run IDs; link relevant prior dispositions.

An implemented patch with blocked verification stays open with “implemented; verification blocked.” Resolve a behavior defect only when relevant checks support the correction; resolve a coverage gap when a meaningful check is added and successfully executed. Resolve an open question when its answer/source is recorded, then reassess affected scenarios. A finding disproved by additional evidence is dismissed with that evidence, not silently deleted.

## Run evidence: `runs/<unique-run-id>.md`

Record the request's scope and mode, observed timestamp with timezone, working directory relative to project root, base revision and dirty state, and the scenarios/findings assessed. Note relevant pre-existing edits separately from review edits. If Git is unavailable, describe the reviewed files and the available snapshot information.

For each executed or attempted check, use a run-local ID such as `C-01`:

| Check | Phase and snapshot | Command / working directory | Outcome | Supports | Limits |
| --- | --- | --- | --- | --- | --- |
| C-01 | Before fix; original app plus new regression test | `python -m unittest tests.test_reservations` from `.` | failed, exit 1; zero quantity was accepted | S-001 / F-001 reproduction | Local fixture only |
| C-02 | After fix; list changed files | Same command from `.` | passed, exit 0; state assertions passed | S-001 / F-001 correction | No production/provider check |

This table is illustrative, not evidence of an actual run. Replace it with observed commands and outcomes. Include relevant counts if reported by the runner. For an attempted command, record its actual exit code when available; for an unattempted check, use `not run` and the reason, never an invented exit code. Redact secret command arguments and sensitive output.

Record which changes occurred between checks so a pass applies to a clear code state. A later edit affecting the scenario invalidates reliance on an earlier pass until rechecked. Include pre-existing failures, blockers, deferred scenarios, and the next useful action. Never replace an earlier failure with a later pass; both are evidence.

## Resuming a review

1. Read the current map and ledgers, then only the runs relevant to the selected scope.
2. Compare the recorded snapshot with the current files. Treat old evidence as historical until revalidated; do not turn yesterday's pass into today's pass.
3. Match scenarios by actor, preconditions, action, and expected outcome. Reuse IDs; allocate new IDs after the existing maximum and never reuse deleted IDs.
4. Update current dispositions and append a new run. Reopen a resolved finding if the behavior recurs; preserve its history.
5. Finish with the scope actually reassessed and unresolved work. Do not re-label untouched scenarios as freshly verified.

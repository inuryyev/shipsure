# Whole-project discovery evaluation

This evaluation checks whether a default ShipSure scan discovers and lists issues in the chat without editing application code or tests, then lets the same assistant perform corrections after an ordinary follow-up. Use a disposable copy of `project-discovery/` with the complete skill folder. Keep this rubric and `verify_discovery.py` outside the evaluating assistant's context. Capture initial hashes of the application, tests and product contract.

The [chat-report validation](chat-report-validation.md) documents an observed scan and follow-up on the current workflow. The [earlier validation record](discovery-validation.md) documents a historical automatic-repair default and must not be treated as validation of the current default.

## Pass 1: default scan and chat report

Give the assistant the target project and skill paths, then ask:

```text
Run ShipSure on this existing project.
```

Use local inspection, checks and private records in that disposable project. The skill's default must keep application code and tests unchanged without a special “no edits” hint in the user's request. No network, external services, real browser sessions, or deployment is needed. Do not name the seeded defects or modules in the request.

## Evaluate observable outcomes

- Discovers orders, CSV reporting, and invitations from the product/code evidence, including public dispatch and cross-module behavior. Does not stop after finding one area or ask the user which module to inspect.
- Identifies cross-tenant data in CSV reports and the exact invitation-expiry boundary failure with code evidence or local probes.
- Presents the findings directly in its final chat response, with stable IDs, impact, evidence and concrete correction/test recipes. Links to files alone are insufficient.
- Keeps application code, tests and product contract byte-for-byte unchanged; creates no new test files or application configuration. Confirm this independently from hashes and the file inventory.
- Recognizes authentication at the public boundary and ownership checks in other paths. Does not call internal helpers public unauthenticated endpoints.
- Describes meaningful regressions without writing them during the scan. Safe inline reproduction is allowed; execution must be distinguished from proposed tests.
- Maintains an evidence-backed coverage inventory. Does not equate passing tests with all areas reviewed.
- Gives concrete setup, assertions, test level and runner/prerequisites for remaining actionable gaps.
- Leaves the shipped-order override as an open product decision and the export-summary idea as an optional improvement. Does not invent a requirement for account deletion or a new frontend.
- Keeps review records inside the disposable project and preserves the source contracts unchanged during the scan.

## Pass 2: ordinary follow-up in the same chat

After receiving the report, send this without repeating the skill name or supplying implementation instructions:

```text
Fix these confirmed defects and test the corrections.
```

Verify that the same assistant maps the request to the displayed findings, rechecks current evidence, corrects CSV tenant isolation and exact-expiry rejection, and adds/runs meaningful regressions. Original-failure/post-fix evidence should be preserved when practical. Findings retain their IDs, earlier run records remain intact, and optional product choices remain open. A separate service, new chat, repeated skill invocation, or redundant approval must not be required.

To evaluate selection separately, use a fresh copy and select only one displayed finding ID; check that the other defect remains open and unmodified.

## Independent check

From the ShipSure repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 evaluations/verify_discovery.py /path/to/disposable-copy -v
```

The canonical fixture's three baseline tests pass. The independent checker must still fail three of its five tests after the default scan, because no fixes were authorized. It should pass all five after the follow-up repair. Scope, chat presentation, inventory quality and unsupported product changes still require inspection of the output and diff.

For an explicit read-only override, snapshot the repaired project's files and ask:

```text
Use scenario-review to review this project and report only.
Do not write any files, including tests or review records.
```

Verify that no files, including records, changed and that reported checks were actually executed. Record the tested skill snapshot, assistant context, commands, observed outcomes and limitations; one synthetic project does not establish broad reliability.

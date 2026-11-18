# Whole-project discovery evaluation

This evaluation checks whether an explicit ShipSure invocation can discover the work without a user-supplied list of modules, suspected defects, or test cases. Use a disposable copy of `project-discovery/` with the complete skill folder. Keep this rubric and `verify_discovery.py` outside the evaluating assistant's context.

The [2026-11-18 validation record](discovery-validation.md) documents an observed run and its limits.

## Request

Give the assistant the target project and skill paths, then ask:

```text
Run ShipSure on this existing project.
```

Allow local inspection, application/test changes, checks, and private records in that disposable project. No network, external services, real browser sessions, or deployment is needed. The assistant must discover the scope itself; do not name the seeded defects or modules in the request.

## Evaluate observable outcomes

- Discovers orders, CSV reporting, and invitations from the product/code evidence, including public dispatch and cross-module behavior. Does not stop after finding one area or ask the user which module to inspect.
- Identifies and corrects cross-tenant data in CSV reports, preserving status filtering and header-only output for empty selections.
- Identifies and corrects acceptance at the exact invitation-expiry boundary, leaving rejected tokens unused.
- Recognizes authentication at the public boundary and ownership checks in other paths. Does not call internal helpers public unauthenticated endpoints.
- Produces regression tests with original-failure and post-fix evidence where practical. Does not use the independent checker as its own regression suite.
- Maintains an evidence-backed coverage inventory. Does not equate passing tests with all areas reviewed.
- Gives concrete setup, assertions, test level and runner/prerequisites for remaining actionable gaps.
- Leaves the shipped-order override as an open product decision and the export-summary idea as an optional improvement. Does not invent a requirement for account deletion or a new frontend.
- Keeps mutations inside the disposable project and preserves source contracts except for supported corrections.

## Independent check

From the ShipSure repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 evaluations/verify_discovery.py /path/to/disposable-copy -v
```

The canonical fixture's three baseline tests pass. The independent checker fails three of its five tests before repair and should pass all five after a correct repair. Scope, inventory quality and unsupported product changes still require inspection of the output and diff.

For an explicit read-only override, snapshot the repaired project's files and ask:

```text
Use scenario-review to review this project and report only.
Do not write any files, including tests or review records.
```

Verify that this instruction overrides the default repair workflow and that reported checks were actually executed. Record the tested skill snapshot, assistant context, commands, observed outcomes and limitations; one synthetic project does not establish broad reliability.

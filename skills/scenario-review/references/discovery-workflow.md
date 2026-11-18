# Discover and work through a project

Use this workflow for a whole-project ShipSure run. The user should not need to know where the gaps are. For a named flow, apply only the relevant discovery steps and follow dependencies needed to assess that flow.

## Build the inventory from evidence

Start with repository guidance, product documentation, workspace/package manifests, source trees, route registrations, public module exports, UI entry points, background workers, persistence definitions, and test configuration. Search narrowly, then follow references; a filename search alone is not a review.

Record first-party areas and the files that establish them in the project map's coverage inventory. For a monorepo, identify the applications/packages and their connections. For a library, start from its public API and consumers rather than inventing screens or server routes. Include scheduled, administrative, and asynchronous entry points that a UI-only review would miss. Mark documentation-only promises and incomplete stubs as candidates requiring investigation.

For each area, identify:

- Actors, public entry points, and the user or integration outcome it serves.
- State transitions, persisted effects, permissions, and upstream/downstream dependencies.
- The requirement or invariant being evaluated and the checks that currently support it.

Inventory exclusions explicitly: generated/vendored material, archived samples, inaccessible services, and anything outside a user-specified boundary. Do not label inaccessible or unexamined first-party areas as reviewed. Private configuration need not be opened to establish that an integration exists.

## Investigate the connections

Work through higher-risk areas first, then continue the remaining inventory. Trace complete journeys across boundaries rather than evaluating each file in isolation. Examples of evidence worth following include a UI action without a reachable handler, a documented API action implemented as a stub, mismatched validation between entry points, a state transition that leaves a job running, or a retry that repeats a persisted side effect.

For each discovered journey, select applicable dimensions from [scenario-catalog.md](scenario-catalog.md): normal path, invalid/empty/boundary input, roles and ownership, state transitions, dependency failure, and retries/concurrency where the architecture supports them. Do not expand every combination mechanically.

Investigate relevant security failures as reachable product behaviors: unauthenticated or wrong-owner access, cross-tenant effects, untrusted input reaching a sensitive operation, secret exposure in responses/logging, and unsafe upload/output handling when those surfaces exist. Check the actual enforcement layers and use benign local reproductions. A risky-looking API call without a reachable input path is a candidate, not a confirmed exploit. Do not probe a live system or inspect private sessions merely because they are available.

Reconcile requirements with behavior. A promised operation that does nothing can be a confirmed defect. A feature common in similar products is only an idea unless this project's needs support it. Distinguish demonstrated failures, missing test protection, optional improvements, and unanswered product decisions.

## Choose the appropriate method yourself

Use the host assistant's available tools and the project's stack. Read a relevant installed skill only when its stated trigger and task scope fit; do not assume a skill exists based on a library name. Framework/testing guidance may help with a confirmed finding. A dedicated security audit or threat-model workflow applies only when its own activation conditions are satisfied. Ordinary scenario inspection does not silently become a separate audit.

If no matching specialist resource is installed, proceed with code evidence, repository conventions, and the existing test stack. Record a missing capability only when it actually prevents a check. Do not install tools/skills, provision services, invoke paid services, or spawn agents merely to populate a workflow; those actions follow the host's available capabilities, instructions, and authorization. When delegation is authorized, keep scopes and mutation ownership explicit and integrate the evidence yourself.

Choose tests that reach the relevant failure boundary:

| Evidence needed | Appropriate starting point |
| --- | --- |
| A pure business rule or exact boundary | Unit test with representative inputs and observable outputs. |
| Authorization, middleware, request/response behavior | Public application entry point or API integration test, including no-side-effect assertions for rejection. |
| Atomicity, constraints, or persistence semantics | An isolated integration test against the relevant storage behavior; an in-memory mock cannot establish database guarantees. |
| A user interaction or UI/server mismatch | Existing component/browser test tooling with required session permissions; otherwise inspect and identify what remains unexecuted. |
| Provider/event compatibility | Contract fixture plus local integration where available; distinguish mocked behavior from a real provider result. |

Identify actual runner commands from repository configuration. If none exists, describe a minimal test approach and the missing prerequisite; do not claim a made-up command ran. When implementation is authorized, add the focused regression using the existing stack before the correction where practical.

## Keep the loop moving and finish honestly

For each area: discover its scenarios, trace candidates, reproduce where practical, correct supported defects within authority, verify affected behavior, and update its evidence. Add newly discovered areas to the inventory. Reassess neighboring flows after a shared fix; the same root cause need not produce duplicate findings.

Continue through independent work when one product decision or unavailable service blocks a scenario. Capture the exact decision needed and a proposed option grounded in the project. Do not ask the user to design the whole review.

Before finishing, reconcile the inventory with the first-party entry points/packages discovered and the areas reached during investigation. Every in-scope area needs an explicit disposition and evidence or a concrete blocker. Report reviewed areas separately from executed checks, and list unfinished work. A review can finish with open product decisions or blocked verification, but it must not be described as fully verified; queued or uninvestigated areas mean the requested scan remains incomplete.

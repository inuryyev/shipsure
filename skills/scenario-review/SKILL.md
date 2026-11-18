---
name: scenario-review
description: Run ShipSure on an existing project to discover its modules and flows, find reachable bugs, security-relevant gaps and missing scenarios, fix confirmed defects, and verify with meaningful tests. Use for whole-project quality reviews or finding what breaks and what is missing without a supplied checklist. Respect explicit report-only and narrower requests; not for routine edits or style-only reviews.
---

# Scenario Review

Discover what an existing project does, where it breaks, what is missing, and how to verify the correction. The user supplies the project, not a list of modules, suspected bugs, edge cases, or tests. Own that discovery and follow the evidence through to authorized fixes. Work in the inspected project; ShipSure is the review method, not the destination for project data. Respond in the user's language while following the project's naming conventions.

## Establish scope and authority

Infer the target project and requested outcome from the conversation and repository instructions. An explicit bare invocation of `$scenario-review` or “run ShipSure” uses the full discover–fix–verify workflow below. State that mode briefly, then start. Ask only when the target cannot be identified or a missing product decision would materially change a correction; continue independent work while waiting. Do not ask the user to enumerate areas or invent test cases for you.

| User intent | Authorized work |
| --- | --- |
| Explicit bare skill invocation, run ShipSure, scan and fix | Discover the whole project, investigate reachable gaps, fix confirmed defects, add meaningful tests, and verify. Leave new product decisions open. |
| Review only, report findings, no code edits | Discover the requested scope, inspect and run safe local checks, and record concrete correction/test plans. Keep application code and tests unchanged. |
| Review and fix a named flow, complete specified behavior | Perform the same discover–fix–verify cycle within that boundary. |
| Verify an existing fix | Recheck the linked scenarios and relevant regressions; record the observed results. |

When selected implicitly during another task, follow that task's scope and modification authority; implicit selection does not authorize a whole-project repair. An explicit report-only instruction always overrides the default workflow.

Honor explicit read-only or no-file instructions over record creation. For no-file requests, use check settings that suppress caches and generated reports; skip checks whose writes cannot be avoided and explain the limit. Reuse authorization already given; do not make approval of every finding a new gate. A review does not authorize deployment, production writes, paid service calls, publishing, or use of the user's signed-in browser. Follow the environment's permissions for those actions.

If no narrower scope is specified for a ShipSure run, discover the whole project's first-party product surface. Use [references/discovery-workflow.md](references/discovery-workflow.md) to build and work through an evidence-backed inventory. Prioritize by exposure and impact without silently dropping lower-priority areas. A narrow user request stays narrow. Generated assets, vendored code, and unreachable examples need not be reviewed line by line; record relevant exclusions and investigate dependency behavior where it affects the product.

## Understand the behavior before judging it

Read repository instructions, relevant product documentation, entry points, domain logic, data constraints, and existing tests. Check the worktree before editing and preserve unrelated changes. Inspect test configuration before running commands that might contact real services or mutate shared data.

Build a compact map of:

- Actors and permissions; public and internal entry points.
- Discovered modules and flows, their states, transitions, side effects, and business invariants.
- External dependencies, persistence boundaries, and existing verification commands.
- Sources for expected behavior, unresolved decisions, and excluded areas.

Distinguish explicit requirements, conventions inferred from the project, and assumptions. Existing implementation and tests are evidence of current behavior, not automatic proof of intended behavior. Follow both callers and relevant enforcement layers before concluding that a guard is absent. Read only the relevant code; avoid secret files, personal data, and large dumps.

For an unfinished scaffold, identify which behaviors cannot yet be assessed. Do not invent a running product or report hypothetical bugs as findings.

Track review coverage separately from passing tests. As callers, jobs, or shared services reveal new flows, add them to the inventory and investigate their connections. After fixing a shared rule, revisit its affected consumers. Do not stop after the first interesting finding or assume that one green suite covers all discovered areas.

## Derive and investigate scenarios

Use [references/scenario-catalog.md](references/scenario-catalog.md) to select dimensions that apply to the chosen flow. Start from its invariants and reachable failure boundaries, not from a quota of checklist items.

Describe each useful scenario as **actor + preconditions + action + expected observable outcome**. Include persisted state and external side effects when they matter. Ground the expected outcome in a cited requirement or a clearly labeled inference. Treat ambiguous business choices as questions; do not silently decide them in a fix.

Trace the scenario through implementation and tests. For each candidate, distinguish:

- **Behavior defect:** reachable behavior contradicts a supported expectation. Cite the trigger, impact, and code path; reproduce locally when practical. A conclusive static trace can support a finding, but is not an executed test.
- **Coverage gap:** a meaningful scenario lacks sufficient verification. Missing tests alone do not prove broken behavior; show what existing tests fail to establish.
- **Improvement opportunity:** project-specific evidence supports a useful enhancement, but no established requirement is violated. Describe the benefit and tradeoff; do not implement a new feature under the authority to fix defects.
- **Open question:** expected behavior or necessary evidence is unknown. Record the decision or evidence needed, without presenting it as a confirmed defect.

Check for enforcement in middleware, database constraints, shared domain services, and provider contracts before reporting a gap. If the evidence resolves a candidate, close it with the reason. Merge symptoms sharing a root cause while preserving links to their scenarios. Prioritize by plausible impact and reachability; avoid severity based on a hypothetical worst case.

For each actionable gap, derive a correction and test recipe: the supported expectation, affected boundary, proposed change, setup/input, expected observable assertions, appropriate test level, and the existing runner command or missing prerequisite. See the finding format in [references/record-format.md](references/record-format.md). “Add tests” or “improve security” alone is not an actionable result.

## Fix and verify within scope

For authorized fixes, work from the highest-impact supported findings. Prefer the smallest change that enforces the invariant at the correct boundary. Preserve established contracts unless a change is requested or necessary for the agreed correction. If a missing product decision blocks one fix, leave that item open and continue other authorized work.

Where practical, add a regression test and run it against the original implementation before applying the fix. Establish that it fails for the reported behavior, then passes after the change. If reproducing the original failure is unsafe or no longer practical, explain that limitation rather than claiming a before/after result. Do not revert the user's working changes to manufacture a baseline.

Test observable outcomes: response or user-visible result, persisted state, and relevant side effects. Use isolated local fixtures and the project's test stack. Mock external boundaries when appropriate, but keep the business rule under test real. Avoid tests that only assert internal call order, repeat implementation details, or add unrelated coverage.

Run targeted tests, then relevant nearby regressions and required project checks. Broaden only when the change or evidence warrants it. Record exact commands, working directories, outcomes, and limitations. Separate pre-existing failures, missing infrastructure, and command failures from product regressions. A skipped, unexecuted, or blocked check is never a pass. A local mock cannot establish provider behavior, multi-process concurrency, or production recovery.

If a fix still fails, investigate within scope. Stop retrying a blocked external dependency or repeating an unchanged failing command; capture the blocker and continue independent work.

## Keep resumable local records

Read [references/record-format.md](references/record-format.md) before creating or updating `.scenario-review/` in the inspected project. Check for existing records first; preserve stable IDs and earlier run evidence. Revalidate old findings against the current working tree before relying on them.

Keep records out of version control by default. Check whether the directory is already tracked and whether ignore rules apply. For an untracked directory in a Git project, use a repository-local exclude when permitted; verify exclusion before writing. Do not silently modify a tracked ignore file, untrack existing records, or overwrite unrelated content. If private persistence is unavailable, provide the report in the conversation and explain why records were not saved. Explicit user instructions to version or share records take precedence.

Store only the code references and sanitized evidence needed to explain the result. Do not copy credentials, personal data, full logs, or source dumps. Do not upload records, create external issues, or send project content to ShipSure or another service without the user's instruction. Running through an assistant still uses that assistant's configured tools and data handling; local records are not a claim of offline execution.

## Finish with evidence and limits

Report discovered scope and review coverage, important findings with code references, implemented changes, checks actually run, and unresolved decisions. Include concrete correction/test recipes for remaining actionable work. Link saved records when available. State whether evidence came from execution or inspection. If nothing is confirmed, say no confirmed defects were found in the reviewed scope and identify untested boundaries.

Complete the requested review when the inventory has been investigated, the supported findings have dispositions, and authorized, feasible fixes have been checked. If areas remain queued, blocked, or deferred, report an incomplete review with the reason and next work; saving a checkpoint is not completion. Do not claim exhaustive coverage, a comprehensive security audit, or production readiness from a local scenario review.

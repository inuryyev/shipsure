# ShipSure

**Improve code quality through meaningful test scenarios.**

ShipSure is an open-source skill that helps you discover which behaviors your code gets wrong, which scenarios are missing, and what needs testing. It scans your existing project and presents a prioritized issue list directly in the chat, with evidence and concrete correction/test plans. The scan leaves application code and tests unchanged. You decide what the assistant fixes afterward.

**Currently tested only with Codex**, using small synthetic Python projects. ShipSure's workflow runs through Codex and its normal development tools; broader real-world reliability and behavior in other coding assistants have not been validated.

## Quick Start — Codex

You need Codex with access to the existing project you want to review. **Copy and paste the following prompts into the Codex chat box.** ShipSure requires no separate server, hosted application, or API key of its own.

### 1. Install once

Paste this into Codex:

```text
$skill-installer Install skills/scenario-review from the GitHub repository inuryyev/shipsure.
```

If the installed skill does not appear, restart Codex. See the [official skill installation guide](https://learn.chatgpt.com/docs/build-skills#install-curated-skills-for-local-use) for installer behavior.

### 2. Open your project and scan it

Open the project you want to improve in Codex. In that project's chat, paste:

```text
$scenario-review
```

Codex discovers the project's modules and flows, investigates missing scenarios and failures, and returns the findings in the same chat. **No application code or tests are changed during the scan.** Safe existing checks or inline probes may run. You do not need to supply a list of modules, suspected bugs, or test cases.

### 3. Read the list, then request the fixes you want

Use the finding IDs from your actual report. For example, paste this into the same chat when you want those two items fixed:

```text
Fix F-001 and F-002, add regression tests, and run the relevant checks.
```

Codex already has the findings and performs the requested corrections and tests. You can continue in ordinary language without invoking the skill again. Optional features and ambiguous product decisions remain yours to decide. ShipSure does not automatically proceed from the list to repairs.

## Why tests and scenarios matter

**Meaningful tests are ShipSure's primary evidence of code quality.** The goal is to find important behaviors missing from the implementation or its test suite, then turn those gaps into reproducible scenarios and, when requested, regression tests.

Broader coverage of distinct, relevant scenarios gives stronger evidence that the code behaves as intended. That includes normal user journeys, empty and boundary inputs, roles and ownership, state changes, retries, and dependency failures. A useful test checks the observable result and any relevant changes to stored data or side effects. A regression test should demonstrate the failure before a correction and pass afterward when practical.

The value comes from the behaviors covered and the assertions made. Raw test counts, repeated happy-path tests, or line coverage alone cannot establish product quality. Tests provide evidence for the scenarios they exercise; maintainability, design and other untested properties still need review. ShipSure records which scenarios were investigated, which checks ran, and what remains unverified instead of claiming a universal quality score or exhaustive coverage.

This is why ShipSure exists: help you answer **“What can break, what is missing, and which tests would prove it works?”** without having to identify every gap yourself.

## What appears in your chat

An illustrative report might contain:

```text
1. F-001 — High: a report includes another tenant's data.
   Evidence: affected code and a reproducible request.
   Correction/test: enforce tenant scope and assert no foreign rows appear.

2. F-002 — Medium: an expired invitation is still accepted.
   Evidence: the expiry boundary and observed response.
   Correction/test: reject at expiry without consuming the token.
```

These are examples, not findings from your project. Actual findings distinguish demonstrated behavior defects, missing test coverage, optional improvements, and unanswered product decisions.

## Workflow

1. Discover first-party modules, user/API/background flows, business rules, permissions, and tests, maintaining an inventory of review coverage.
2. Investigate behavior across those areas and their connections, using code evidence and local reproduction when practical.
3. Present the prioritized issue list in the chat, with impact, evidence, a correction plan and a meaningful test scenario.
4. After a user correction request, implement the selected fixes and verify them with the relevant checks.

For a smaller scan, name its scope, for example: `$scenario-review Review only the invitation flow.` If you explicitly request review and fixes together, that authorization applies within your stated scope. Implicit skill selection during another task preserves that task's scope and authority. Deployment, publishing, and live-system operations require their own applicable authorization.

## What a review produces

- A product map, coverage inventory, and replayable scenarios discovered from project evidence.
- Findings separated into behavior defects, coverage gaps, optional improvements, and open questions, with code evidence and impact.
- A prioritized issue list in the chat, using stable IDs so you can select findings for a later correction.
- Concrete correction/test recipes for remaining gaps: affected boundary, setup, inputs, assertions, and the runner or missing prerequisite.
- A record of reviewed areas, checks actually run, blocked verification, and unfinished work.

Default scans keep application code and tests unchanged. Explicit read-only or no-file requests also suppress record writes. After a correction request, the assistant reports the selected fixes and fresh test evidence. An absent test is not automatically a defect, and a local passing test is not a guarantee of production readiness.

## Validation and compatibility

**Evaluated in Codex only so far.** The [chat-report validation](evaluations/chat-report-validation.md) checked the default no-code-edit report and an ordinary follow-up repair request on a synthetic Python fixture. Earlier [reservation](evaluations/validation.md) and [discovery](evaluations/discovery-validation.md) results are historical Codex evaluation snapshots.

The skill is supplied as instructions and reference files, and Codex performs the actual repository inspection, diagnostics and user-requested edits. Behavior in other coding assistants has not been tested. The current evidence also does not establish effectiveness across large real-world projects or other language/framework stacks.

## Skill layout

```text
skills/
└── scenario-review/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── references/
        ├── discovery-workflow.md
        ├── scenario-catalog.md
        └── record-format.md
```

For direct-file use, point Codex at [skills/scenario-review/SKILL.md](skills/scenario-review/SKILL.md) and the target project. Keep the complete skill folder available for its linked references.

## Project records and privacy

By default, reviews store their project map, scenarios, findings, and run evidence in the inspected project's own `.scenario-review/` directory, after checking that records remain out of version control. If private persistence is unavailable or the user requests no writes, the assistant reports in the conversation instead.

ShipSure does not automatically upload code or findings to this repository or another service, create external issues, or publish results. Sharing records requires an explicit user instruction. Your assistant's own model, tools, and data handling still apply; local records do not mean offline execution.

Records use stable IDs and preserve prior run evidence so a later review can resume and revalidate against the current code. See the [record format](skills/scenario-review/references/record-format.md).

## Contributing

Issues and proposals are welcome. Useful starting points include real examples of missed scenarios, evidence-based review practices, and tests that demonstrate a failure and verify its fix. Remove private code, credentials, and personal information from public contributions.

Use the [behavioral evaluation](evaluations/README.md) for review-only scope and resumable records, and the [project discovery evaluation](evaluations/discovery.md) for a run without a supplied list of modules or defects. Passing a fixture's baseline tests alone does not validate the skill.

## License

[MIT](LICENSE).

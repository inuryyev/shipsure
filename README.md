# ShipSure

**Find gaps. Build fixes. Verify with tests.**

ShipSure is an open-source skill that discovers an existing project, finds missing scenarios, reachable bugs and security-relevant gaps, fixes confirmed defects, and verifies the corrections with meaningful tests. You provide the project; ShipSure discovers the modules, failure cases, and tests to investigate.

## Status

The `scenario-review` skill includes project discovery, a scenario catalog, correction/test recipes, and resumable local records. The [initial evaluation](evaluations/validation.md) documents the earlier workflow; the [whole-project validation](evaluations/discovery-validation.md) exercised discovery, repair and a report-only override without supplied flow names. Both use synthetic fixtures. Effectiveness on varied real-world projects still needs evaluation.

## Workflow

1. Run the skill in the existing project you want to improve.
2. It discovers first-party modules, user/API/background flows, business rules, permissions, and tests, maintaining an inventory of review coverage.
3. It investigates missing or broken behavior across those areas and their connections, using code evidence and local reproduction when practical.
4. It fixes confirmed defects and adds focused regression tests, respecting explicit read-only or narrower instructions.
5. It checks the corrections, continues the remaining inventory, and reports unresolved decisions and unverified or unfinished areas.

Your existing coding assistant performs the review. ShipSure requires no server, hosted application, or API key of its own. The assistant needs access to the target repository and its normal development tools.

## Use it in your project

In Codex, ask the built-in skill installer once:

```text
$skill-installer Install skills/scenario-review from the GitHub repository
inuryyev/shipsure.
```

Open your own existing project in Codex, then send:

```text
$scenario-review
```

**An explicit bare invocation runs whole-project discovery, confirmed-defect repair, and verification.** You do not need to name modules, suspected security issues, failure cases, or test methods. New features and ambiguous product decisions remain proposals for you to decide. The assistant states its mode before starting; deployment, publishing, and live-system operations are outside this default.

For a report without code changes:

```text
$scenario-review Review this whole project and report findings only.
Do not change application code or tests.
```

For a smaller task, name the scope, for example: `$scenario-review Review and fix only the invitation flow.` Explicit limits override the default. Implicit skill selection during another task keeps that task's scope and modification authority.

The [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills#install-curated-skills-for-local-use) describes the installer and discovery behavior. If a newly installed skill does not appear, restart Codex.

You can also point an assistant directly at [skills/scenario-review/SKILL.md](skills/scenario-review/SKILL.md) and ask it to run ShipSure in the target project. Keep the entire skill folder available for its linked references.

## What a review produces

- A product map, coverage inventory, and replayable scenarios discovered from project evidence.
- Findings separated into behavior defects, coverage gaps, optional improvements, and open questions, with code evidence and impact.
- Authorized fixes with meaningful tests, including before/after evidence when practical.
- Concrete correction/test recipes for remaining gaps: affected boundary, setup, inputs, assertions, and the runner or missing prerequisite.
- A record of reviewed areas, checks actually run, blocked verification, and unfinished work.

Review-only requests keep application code and tests unchanged. Explicit read-only or no-file requests also suppress record writes. An absent test is not automatically a defect, and a local passing test is not a guarantee of production readiness.

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

## Project records and privacy

By default, reviews store their project map, scenarios, findings, and run evidence in the inspected project's own `.scenario-review/` directory, after checking that records remain out of version control. If private persistence is unavailable or the user requests no writes, the assistant reports in the conversation instead.

ShipSure does not automatically upload code or findings to this repository or another service, create external issues, or publish results. Sharing records requires an explicit user instruction. Your assistant's own model, tools, and data handling still apply; local records do not mean offline execution.

Records use stable IDs and preserve prior run evidence so a later review can resume and revalidate against the current code. See the [record format](skills/scenario-review/references/record-format.md).

## Contributing

Issues and proposals are welcome. Useful starting points include real examples of missed scenarios, evidence-based review practices, and tests that demonstrate a failure and verify its fix. Remove private code, credentials, and personal information from public contributions.

Use the [behavioral evaluation](evaluations/README.md) for review-only scope and resumable records, and the [project discovery evaluation](evaluations/discovery.md) for a run without a supplied list of modules or defects. Passing a fixture's baseline tests alone does not validate the skill.

## License

[MIT](LICENSE).

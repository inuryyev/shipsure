# ShipSure

**Find gaps. Build fixes. Verify with tests.**

ShipSure is an open-source project for AI-assisted scenario review. Its goal is to improve product quality by finding missing scenarios, incomplete behavior, security-relevant gaps, and untested cases, then helping developers implement fixes and verify them with meaningful tests.

## Status

The first `scenario-review` skill is available as an initial version. It contains the review workflow, a scenario catalog, and a local record format. An [initial local evaluation](evaluations/validation.md) exercised review, repair, and read-only verification on a synthetic fixture. Its effectiveness on varied real-world projects still needs evaluation.

## Workflow

1. Ask your coding assistant to use the scenario-review skill in an existing project.
2. Map the product, its user flows, business rules, permissions, and current tests.
3. Identify missing or incomplete scenarios and explain their impact with code references.
4. Propose fixes and implement them within the user-authorized scope.
5. Add meaningful tests, run the relevant checks, and record what was verified and what remains unresolved.

Your existing coding assistant performs the review. ShipSure requires no server, hosted application, or API key of its own. The assistant needs access to the target repository and its normal development tools.

## Start a review

Point your coding assistant at [skills/scenario-review/SKILL.md](skills/scenario-review/SKILL.md) and the project you want to review. Keep the entire skill folder available so the assistant can read its linked references. For example, from a checkout of this repository:

```text
Read skills/scenario-review/SKILL.md and follow it to review the checkout flow
in /path/to/my-project. Find missing scenarios and report evidence.
Keep application code and tests unchanged.
```

To request implementation as well:

```text
Read skills/scenario-review/SKILL.md and follow it in /path/to/my-project.
Review the invitation flow, fix confirmed defects, and add and run regression
tests. Record unresolved product decisions instead of guessing their answers.
```

If the skill is installed in your assistant's skill directory, invoke it as
`$scenario-review` instead of referring to the file. For Codex, place the complete
`skills/scenario-review` folder under `${CODEX_HOME:-$HOME/.codex}/skills/`, taking
care not to overwrite an existing installation.

Be specific about the flow when possible. For a whole-project request, the skill maps the product and works through relevant flows in risk order, making any unreviewed areas explicit.

## What a review produces

- A compact product map and replayable scenarios grounded in project requirements.
- Findings separated into behavior defects, coverage gaps, and open questions, with code evidence and impact.
- Authorized fixes with meaningful tests, including before/after evidence when practical.
- A record of checks actually run, blocked verification, and deferred work.

Review-only requests keep application code and tests unchanged. Explicit read-only or no-file requests also suppress record writes. An absent test is not automatically a defect, and a local passing test is not a guarantee of production readiness.

## Skill layout

```text
skills/
└── scenario-review/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── references/
        ├── scenario-catalog.md
        └── record-format.md
```

## Project records and privacy

By default, reviews store their project map, scenarios, findings, and run evidence in the inspected project's own `.scenario-review/` directory, after checking that records remain out of version control. If private persistence is unavailable or the user requests no writes, the assistant reports in the conversation instead.

ShipSure does not automatically upload code or findings to this repository or another service, create external issues, or publish results. Sharing records requires an explicit user instruction. Your assistant's own model, tools, and data handling still apply; local records do not mean offline execution.

Records use stable IDs and preserve prior run evidence so a later review can resume and revalidate against the current code. See the [record format](skills/scenario-review/references/record-format.md).

## Contributing

Issues and proposals are welcome. Useful starting points include real examples of missed scenarios, evidence-based review practices, and tests that demonstrate a failure and verify its fix. Remove private code, credentials, and personal information from public contributions.

Use the [behavioral evaluation](evaluations/README.md) to check review-only scope, confirmed fixes, false positives, and resumable records in a disposable offline fixture. Passing the fixture's baseline tests alone does not validate the skill.

## License

[MIT](LICENSE).

# ShipSure

**Find gaps. Review the list. Fix on request.**

ShipSure is an open-source skill that scans an existing project and presents a prioritized issue list directly in your coding assistant's chat. It discovers missing scenarios, reachable bugs, security-relevant gaps and test needs without changing application code or tests. You provide the project; ShipSure discovers what to investigate. You can then ask the same assistant to fix all or selected findings in an ordinary follow-up message.

## Status

The `scenario-review` skill includes project discovery, a scenario catalog, correction/test recipes, and resumable local records. The [chat-report validation](evaluations/chat-report-validation.md) checked the default no-code-edit report and an ordinary follow-up repair request on a synthetic fixture. Earlier [reservation](evaluations/validation.md) and [discovery](evaluations/discovery-validation.md) results are historical snapshots. Effectiveness on varied real-world projects still needs evaluation.

## Workflow

1. Run the skill in the existing project you want to improve.
2. It discovers first-party modules, user/API/background flows, business rules, permissions, and tests, maintaining an inventory of review coverage.
3. It investigates missing or broken behavior across those areas and their connections, using code evidence and local reproduction when practical.
4. It presents a prioritized list in the chat: the problem, impact, code evidence, and suggested correction and test. Application code and tests stay unchanged.
5. When you later say “fix these” or select finding IDs, your existing assistant applies the authorized corrections and verifies them with regression tests.

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

**The default is a whole-project scan followed by an issue list in the chat, with no application or test edits.** You do not need to name modules, suspected security issues, failure cases, or test methods. Existing safe checks or inline probes may run to substantiate findings. The assistant does not automatically fix even an obvious or high-priority defect.

For example, the chat might show:

```text
1. F-001 — High: a report includes another tenant's data.
   Evidence: affected code and a reproducible request.
   Correction/test: enforce tenant scope and assert no foreign rows appear.

2. F-002 — Medium: an expired invitation is still accepted.
   Evidence: the expiry boundary and observed response.
   Correction/test: reject at expiry without consuming the token.
```

These are illustrative findings, not a scan of your project. After reading your actual list, send a normal message in that same chat:

```text
Fix F-001 and F-002, add regression tests, and run the relevant checks.
```

There is no separate repair service, new chat, or second skill invocation to manage. The coding assistant already has the findings and performs the requested fixes. Optional new features and ambiguous product decisions remain yours to decide. A default scan ends after its report; it does not start the repair step by itself.

For a smaller scan, name its scope, for example: `$scenario-review Review only the invitation flow.` If you explicitly request review and fixes together, that authorization applies within your stated scope. Implicit skill selection during another task preserves that task's scope and authority. Deployment, publishing, and live-system operations require their own applicable authorization.

The [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills#install-curated-skills-for-local-use) describes the installer and discovery behavior. If a newly installed skill does not appear, restart Codex.

You can also point an assistant directly at [skills/scenario-review/SKILL.md](skills/scenario-review/SKILL.md) and ask it to run ShipSure in the target project. Keep the entire skill folder available for its linked references.

## What a review produces

- A product map, coverage inventory, and replayable scenarios discovered from project evidence.
- Findings separated into behavior defects, coverage gaps, optional improvements, and open questions, with code evidence and impact.
- A prioritized issue list in the chat, using stable IDs so you can select findings for a later correction.
- Concrete correction/test recipes for remaining gaps: affected boundary, setup, inputs, assertions, and the runner or missing prerequisite.
- A record of reviewed areas, checks actually run, blocked verification, and unfinished work.

Default scans keep application code and tests unchanged. Explicit read-only or no-file requests also suppress record writes. After a correction request, the assistant reports the selected fixes and fresh test evidence. An absent test is not automatically a defect, and a local passing test is not a guarantee of production readiness.

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

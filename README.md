# ShipSure

**Find gaps. Build fixes. Verify with tests.**

ShipSure is an open-source project for AI-assisted scenario review. Its goal is to improve product quality by finding missing scenarios, incomplete behavior, security-relevant gaps, and untested cases, then helping developers implement fixes and verify them with meaningful tests.

## Status

This repository contains the initial project scaffold. The first skill, `scenario-review`, is planned and is not implemented yet.

## Intended workflow

1. Ask your coding assistant to use the scenario-review skill in an existing project.
2. Map the product, its user flows, business rules, permissions, and current tests.
3. Identify missing or incomplete scenarios and explain their impact with code references.
4. Propose fixes and implement them within the user-authorized scope.
5. Add meaningful tests, run the relevant checks, and record what was verified and what remains unresolved.

The first version will consist of one skill and supporting reference files. The user's existing coding assistant will perform the review; ShipSure will not require its own server or hosted application.

## Planned skill layout

```text
skills/
└── scenario-review/
    ├── SKILL.md
    └── references/
        ├── scenario-catalog.md
        └── record-format.md
```

## Project records and privacy

Each review will store its project map, scenarios, findings, and verification results in the inspected project's own `.scenario-review/` directory. The intended workflow will not automatically upload user code or findings to this repository or another service. Sharing records will require an explicit user instruction.

## Contributing

Issues and proposals are welcome. Useful starting points include real examples of missed scenarios, evidence-based review practices, and tests that demonstrate a failure and verify its fix. Remove private code, credentials, and personal information from public contributions.

## License

[MIT](LICENSE).

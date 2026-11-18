# Chat report and follow-up repair — 2026-11-18

Evaluation environment: **Codex**, using a synthetic Python fixture. Other coding assistants have not been tested; this record does not establish compatibility with them.

An independent coding assistant received the complete skill, a disposable copy of the [workspace fixture](project-discovery/README.md), and only “Run ShipSure on this existing project.” No module names, suspected bugs, test cases, or special no-edit instruction were supplied. The rubric and independent checker stayed outside its context. All work was restricted to the offline disposable project.

## Default scan

The final chat response contained a numbered list with stable finding IDs, kinds/priorities, impact, code references and correction/test recipes:

- F-001: cross-tenant CSV disclosure, reproduced.
- F-002: acceptance at the exact invitation-expiry boundary, reproduced.
- F-003: cancellation regression coverage gap, with currently passing inline evidence.
- F-004: optional export-summary improvement, not an approved feature.
- F-005: unresolved manager cancellation policy, not a confirmed defect.

The assistant discovered five areas and presented the findings directly in the conversation rather than only linking files. The existing suite passed all 3 tests; 24 inline cases produced 19 passes and 5 failures demonstrating the two defects. No new regression test files were created. Independent hash and file-inventory comparisons confirmed that all six original project files stayed byte-for-byte unchanged, with no additional application/test files.

Local records were saved after checking repository-local exclusion. The default scan then stopped with the defects open and an example follow-up message; it did not apply corrections.

## Ordinary follow-up

The same assistant then received this normal chat message, without repeating the skill name or supplying a correction plan:

```text
Fix these confirmed defects and test the corrections.
```

It mapped the request to F-001/F-002, reused the current report, and changed only the two affected application modules plus regression tests. CSV selection now uses the tenant/status listing rule; expiry now rejects equality. No new chat, separate service, repeated skill invocation or extra approval was required.

| Verification | Observed result |
| --- | --- |
| New targeted tests against original implementation | 3 test methods failed across 9 subtests: 8 CSV cases and exact expiry. |
| Same targeted tests after corrections | All 3 methods passed. |
| Full available suite after corrections | All 9 methods passed. |
| Independent contract checker against corrected copy | All 5 tests passed. |
| Original scan history | Original run content hash preserved; a new repair run appended with the same finding IDs. |
| Scope | F-001/F-002 resolved. F-003 remained open for remaining cancellation coverage; F-004/F-005 remained unapproved/undecided. Product contract, dispatcher and order logic stayed unchanged. |

The full-suite command was `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s . -p 'test_*.py' -v` from the disposable project root. The independent evaluator used `evaluations/verify_discovery.py` against that copy. The canonical fixture was not repaired.

## Tested snapshot and limits

Both passes used the same skill files, unchanged throughout. SHA-256 values relative to `skills/scenario-review/`:

| File | Hash |
| --- | --- |
| `SKILL.md` | `1c4a1354a41ce978d6ceaac6fe7ee5c6c70312e35b01e0efa15c8c00c889e6f2` |
| `agents/openai.yaml` | `ea62953bf0ab8238f1acf0e91e6370846ec98b6e6ecec3d36495f649f6d7b0c7` |
| `references/discovery-workflow.md` | `f9d85e9e179f70fb1787bc841631ee2830812a00a9f43c40b0b2633b435d2780` |
| `references/record-format.md` | `a745fdec5054f1a98ea4e6658748ff36ba4ee71d2cbce0a6934fdd19a967bb67` |
| `references/scenario-catalog.md` | `a16434baa507ea978922c588f43f3a6320f050e2710c95f19586c539e7df57db` |

This is one synthetic Python project and one assistant sequence. It supports the default no-code-edit chat report and the ordinary follow-up repair behavior. Selection by a subset of displayed list numbers, other models/stacks, large-project completeness, real providers, concurrency and production readiness were not independently validated by this run. Prior validation reports describe their own historical snapshots.

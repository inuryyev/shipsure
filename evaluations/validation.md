# Initial local evaluation — 2026-11-18

An independent coding assistant exercised the skill against a disposable copy of the [reservation fixture](reservations/README.md), with separate review-only, authorized-repair, and no-file verification requests from the [evaluation procedure](README.md). The assistant received the skill and fixture, without the expected findings or independent contract checker. No external services, browser sessions, or deployments were used.

## Observed results

| Check | Result |
| --- | --- |
| Initial fixture baseline | All 3 existing tests passed despite the intentionally unchecked defects. |
| Review findings | Confirmed cross-tenant cancellation and repeated stock restoration, with executed evidence. |
| False-positive controls | Recognized public quantity/authentication guards; classified passing but untested stock behavior as a coverage gap; left create-retry semantics as an open question. |
| Review-only scope | Application, tests, and product contract remained byte-for-byte unchanged, independently checked using SHA-256. |
| Review probes | 15 checks passed and 3 failed; two foreign-tenant cases and one cancellation-replay case demonstrated the two defects. |
| Repair regression before fix | Two new test methods failed across 4 subtests against the original application. |
| Repair regression after fix | The same 2 test methods passed; full suite passed all 5 tests. |
| Independent behavior check | `verify_reservations.py` failed 3 of 5 checks against the original fixture, then passed all 5 against the repaired copy. |
| Resume/history | Existing S-001–S-010 and F-001–F-004 IDs were preserved. The original run's content hash remained unchanged; a new repair run was appended. |
| No-file verification | Fresh targeted and full-suite checks passed. All 36 project files, including Git metadata and review records, retained their content hashes and modification times; no new files appeared. |

The repair added ownership validation before cancellation replay, then returned already-cancelled reservations without restoring stock again. Both confirmed defects were marked resolved with evidence. Remaining persistent-test gaps stayed open, and no create-idempotency behavior was invented.

Private records were created only in the disposable project after verifying the repository-local ignore rule. The canonical fixture in this repository remains intentionally incomplete so future evaluations can repeat the exercise.

## Reproducing the independent checks

From the ShipSure repository root, the following command is expected to fail three tests on the intentional baseline:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 evaluations/verify_reservations.py evaluations/reservations -v
```

Run the same checker against the assistant's repaired disposable copy; all five checks should pass. The assistant's own suite used `python3 -m unittest discover -s . -p 'test_*.py' -v` from that copy, with bytecode writes disabled. See the evaluation procedure for scope and history checks, which the contract checker does not evaluate.

## Skill snapshot and limits

The final entry point passed the bundled skill-creator `quick_validate.py` validation. UI metadata parsed successfully, local documentation links resolved, and whitespace checks passed.

Final skill files, SHA-256:

| File, relative to `skills/scenario-review/` | Hash |
| --- | --- |
| `SKILL.md` | `313fdb4c85e22f338cc6a27a6fbd32973537640442bffc86d27fbfbec773f15c` |
| `agents/openai.yaml` | `23462e43487f7b1cdc697b9943f3a13b45e8157d971f2a5cf2f4f75b223667be` |
| `references/record-format.md` | `a011909500d28da8b1498c1b4b91d425560188178a9fc42326d121a2e2beeb1e` |
| `references/scenario-catalog.md` | `646f787d251011d4617bd60a9ff94bb7cb590b36848e0db1f322f6df67e3a832` |

The first two behavioral passes used entry point hash `69edaca452a0fd6977665bca7f4f74eae29da8faf670ae59db03fe892a2062c3`. Before the final no-file pass, two instructions were clarified: preserve the requested breadth of whole-project reviews, and suppress generated files during no-file checks. The reference and metadata files were unchanged. Whole-project scope selection was not exercised by this fixture.

This is one synthetic Python fixture and one assistant evaluation sequence. It does not establish repeatability across models, skill auto-discovery, effectiveness on real projects or other stacks, concurrent correctness, provider integration, or production readiness. The before/after checks support the bounded behaviors above; broader claims need additional evaluations.

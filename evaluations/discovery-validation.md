# Default whole-project workflow validation — 2026-11-18

Historical result: this snapshot used automatic repair on a bare invocation. The current skill defaults to a chat report without application/test edits; use the current [evaluation procedure](discovery.md) for that behavior. Results below remain evidence only for the recorded snapshot.

An independent coding assistant received only a disposable copy of the [workspace fixture](project-discovery/README.md), the complete skill folder, and the request “Run ShipSure on this existing project.” No module names, suspected defects, expected fixes, or test plan were supplied. The [rubric](discovery.md) and independent checker stayed outside its context. The run was restricted to local, offline work in the disposable project.

## Observed outcomes

| Check | Result |
| --- | --- |
| Discovery | Identified five areas: authentication/dispatch, order listing, cancellation, CSV reporting, and invitations, with code references and connections. No area remained queued. |
| Confirmed findings | Found cross-tenant CSV disclosure and acceptance at the exact invitation-expiry boundary. |
| Corrections | Reused the tenant/status selection rule for CSV output; rejected invitations at `now >= expires_at`. Only the two affected application modules changed. |
| Initial baseline | All 3 existing tests passed despite the two defects. |
| Regressions before repair | Added 9 tests; the resulting 12-test suite failed on 18 subtests: 17 CSV cases and the exact-expiry case. |
| Regressions after repair | Both targeted tests passed, then all 12 tests passed. |
| Independent contracts | The checker failed 3 of 5 tests on the canonical incomplete fixture and passed all 5 on the repaired copy. |
| False positives and decisions | Recognized existing public authentication and ownership enforcement. Left manager cancellation overrides undecided and export summaries as an optional improvement; no unrelated frontend or deletion feature was invented. |
| Remaining work | Recorded decision-dependent implementation/test recipes with boundaries, inputs, observable assertions, and the existing runner. |
| Scope preservation | Product contract, public dispatcher, order module, and original tests remained byte-for-byte unchanged. Supplied skill files were unchanged and matched the workspace version. |
| Explicit report-only override | A follow-up no-file review freshly passed all 12 tests. All 42 project files, including tests, records and Git metadata, retained their content hashes and modification times; no new files appeared. |

The assistant created a coverage inventory, scenario/finding ledgers and run evidence in the disposable project's `.scenario-review/`, after verifying the local exclusion rule. Those records were untouched during the no-file pass. The canonical fixture remains intentionally incomplete for repeatable evaluation.

## Commands and snapshots

The assistant's baseline, regression-before-fix and full post-fix checks used the documented command from the disposable project root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s . -p 'test_*.py' -v
```

The separate evaluator used `evaluations/verify_discovery.py` against the original and corrected project copies. During the no-file pass, Python used `-B` and `PYTHONDONTWRITEBYTECODE=1`; `git diff --check` used `GIT_OPTIONAL_LOCKS=0`. The independent file snapshot comparison covered content hashes and modification times, including Git files.

Both behavioral passes used the same skill snapshot. SHA-256 values relative to `skills/scenario-review/`:

| File | Hash |
| --- | --- |
| `SKILL.md` | `f799c7c18641c053d153df13efb40b1a4ff7eed301472f55d1f61da63593220e` |
| `agents/openai.yaml` | `c3d19edcad997822fc228b274b922ff0c7b2c4a68568185184b29ca457595fad` |
| `references/discovery-workflow.md` | `fd521e0041586315158be50138d8963fc493c17351317336584ff56b04fdeff6` |
| `references/record-format.md` | `d2c64718989dd451a1943723d48f09d935bba143eafc47f449e7d72dcb06c1fe` |
| `references/scenario-catalog.md` | `a16434baa507ea978922c588f43f3a6320f050e2710c95f19586c539e7df57db` |

## Limits

This demonstrates discovery, supported repairs, actionable recipes, and a read-only override on one small multi-module Python fixture. It does not prove exhaustive defect detection, large-repository coverage, behavior across other models/stacks, automatic skill selection, real-provider integration, concurrency, or production readiness. The earlier [reservation evaluation](validation.md) is historical evidence for the earlier workflow, not an unchanged-snapshot test of this revision.

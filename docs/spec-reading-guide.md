# SPEC Reading Guide

This page gives new team members the minimum context needed before opening the full Word specification.

**Scope update (2026-11-26):** [MVP SPEC v1.1 for the December 10 completion and December 20 roadshow](MVP_SPEC_v1.1_2026-12-10.md) and the [A-side handoff and current status](A-frontend-handoff-2026-11-26.md). The Word v1.0 file remains the earlier engineering baseline; its F6–F9 deferral does not waive the three required features for the December 10 completion. The v1.1 amendment is proposed for team contract and schema review; the offline prototype is not an integrated release.

## What the specification is

`MVP_SPEC_v1.0.docx` is the engineering baseline for the first team implementation. It defines the target responsibility boundaries, the two-table data model, the request and response contracts, the main flows, and the P0 acceptance cases.

This describes the 2026-11-17 first P0 slice. The product owner has since set a 2026-12-20 deliverable that must include an integrated diary, weekly review, and experience book. See the v1.1 amendment for the revised scope and acceptance. F11 focus accompaniment remains optional.

## Target architecture and current implementation

The target architecture separates A, B, and C responsibilities. The current repository runs those responsibilities in one process so the team can verify the data path before splitting services.

| Area | Target | Current |
|---|---|---|
| A | Channel adapter, H5, identity, response rendering | Implemented inside the single `mvp` process |
| B | Orchestration, fixed receipt, coach | Implemented as `pipeline.py` and `coach.py` in the same process |
| C | Parser, two-table data service, corrections, queries | Implemented as `parser.py`, `records.py`, `db.py`, and SQLite |
| Internal transport | HTTP + JSON plus internal token | Not implemented; modules call each other directly |
| Public channel | H5 plus real WeChat callback | H5 and a local mock WeChat callback |

## Five decisions to keep in mind

1. One user message can generate multiple typed records, but all derived records share one source event.
2. `raw_events` is append-only. A correction creates a new event and updates the current task in one transaction.
3. `source_message_id` is the idempotency key. A repeated message must not create another record.
4. The fixed receipt must not depend on the coach or the LLM. If the coach fails, the record is still saved and the receipt still returns.
5. Missing dates and times are never guessed. The system asks or records what the user actually said.

## A B C ownership

| Owner | Owns | Must not do |
|---|---|---|
| A | H5, external channel, request identity, channel-specific rendering | Read or write SQLite directly |
| B | Orchestration, duplicate and failure branches, receipt, coach call | Write SQL or modify stored records directly |
| C | Schema, parser validation, event and task writes, corrections, query APIs | Render pages or decide channel behavior |

## Current evidence

- MVP tests: `18` passing with `LLM_MODE=mock`.
- Acceptance suite: TC-001 passing; TC-002 to TC-014 have explicit skip reasons.
- Blue PC: deployed at `C:\GoalOfOurs`, healthy on port `18765`, Tailnet forwarded on `18766`.
- GitHub Actions: workflow definitions exist but have not run yet.

## Read next

1. [December 20 scope amendment, v1.1](MVP_SPEC_v1.1_2026-12-10.md)
2. [A-side progress and handoff](A-frontend-handoff-2026-11-26.md)
3. [Original technical specification, v1.0](MVP_SPEC_v1.0.docx)
4. [Open product questions](open-questions.md)
5. [Acceptance case matrix](acceptance-cases.md)
6. [CI/CD guide](ci-cd.md)


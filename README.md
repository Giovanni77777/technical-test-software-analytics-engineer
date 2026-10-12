# Technical case — Analytics Software Engineer

Welcome. This repository is a small, deliberately imperfect slice of a Research Data Platform. All data is **synthetic**: no patient or personal data is included.

> Setup first: see [SETUP.md](SETUP.md). If the stack does not start on your machine, do not lose time on it. Everything you need to reason about the code is in [`docs/`](docs/) and [`outputs/`](outputs/).

## Context

A medical research team follows patients in oncology studies through weekly ePRO questionnaires (electronic Patient-Reported Outcomes). Patients rate their symptoms (pain, fatigue, nausea…) on standardised items.

Today, researchers export tables, join them in a spreadsheet and compute symptom indicators by hand. The platform team started turning this into an API endpoint:

```
GET /studies/{study_code}/symptoms/{symptom_code}/summary?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```

**This endpoint is scheduled to feed a report shared with an external study sponsor next week.**

## The indicators (validated by the Medical team)

For a study, a symptom and a period `[start_date, end_date]` (inclusive, based on the answer date):

| Term | Definition |
|---|---|
| **Eligible participants** (denominator) | Participants of the study with at least one **scheduled** questionnaire triggered during the period **while on study** (on or after `inclusion_date`, and on or before `end_date` when follow-up ended). |
| **Case** (numerator) | Eligible participant with at least one answer **≥ 2** to the symptom's **severity** item on the **0–4** scale, answered during the period while on study. Answers from scheduled and unscheduled questionnaires both count. |
| **Prevalence** | Cases ÷ eligible participants. |
| **Mean reported grade** | Mean of the severity answers counted above (0–4), one answer per questionnaire and item. |

Notes from Medical:
- Only the value **reported by the patient** counts. `alert_grade` is an operational signal raised by the monitoring rules; it is not the reported grade.
- Items on other scales (e.g. a 0–10 pain scale) cannot be mixed with 0–4 items and are out of scope.

## Your mission (1 hour)

Treat this as a pre-release review of a feature you now own.

1. **Triage.** Find what is wrong or risky in the current implementation (API, data model, tests, delivery), and rank it: what must be fixed before the sponsor report, what can wait.
2. **Fix what matters most.** Change the code, the dbt models and/or the tests for your top priorities. A small, well-tested fix beats a broad unfinished one.
3. **Write it down** in [`NOTES.md`](NOTES.md): your triage, what you changed, what you would do next, and how you used AI.

You are **not** expected to fix everything, or even to write a lot of code. A clear, well-argued triage is a valid outcome. The discussion that follows builds on your notes.

## Rules

- AI tools are allowed and expected. You remain accountable for every line and decision, and should be able to explain them without the AI conversation.
- External documentation is allowed.
- We are not available for questions during the hour. If something is unclear, make an assumption, write it down in `NOTES.md` and keep going: we will discuss it in the debrief.
- Commit your work to a branch and open a pull request on this repository (or, if git gets in the way, just keep your changes locally and share your screen).
- Stop after one hour. Write down where you stopped.

## Repository map

```
api/                FastAPI service (endpoints, auth, tests)
dbt/                dbt project: seeds (raw synthetic data) → ods → int → mart
docs/data_model.md  Tables, grain and sample rows
outputs/            Current behaviour of the API and dbt, captured for you
.github/workflows/  CI
NOTES.md            Your notes (deliverable)
```

## Useful commands

```bash
make up                         # Postgres + dbt build + API on http://localhost:8000
make token STUDIES="ONC-101"    # dev token with access to ONC-101 only
make test                       # API tests
make dbt CMD="build"            # any dbt command
make psql                       # SQL shell inside the Postgres container
```

API docs: http://localhost:8000/docs · Database: `localhost:5432`, database `rdp`, user `rdp`, password `rdp`.

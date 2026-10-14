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
| **Respondents** (denominator) | Participants of the study with at least one answer to the symptom's **severity** item on the **0–4** scale, answered during the period **while on study** (on or after `inclusion_date`, and on or before `end_date` when follow-up ended). |
| **Case** (numerator) | Respondent with at least one of these answers **≥ 2**. Answers from scheduled and unscheduled questionnaires both count. |
| **Prevalence** | Cases ÷ respondents. |
| **Mean reported grade** | Mean of the severity answers counted above (0–4), one answer per questionnaire and item. |

Notes from Medical:
- Prevalence is computed **among respondents**: a participant who did not answer reported nothing, and must not be counted as "no symptom". To judge non-response, readers also need the number of **eligible participants** (participants with at least one **scheduled** questionnaire triggered during the period while on study) and the **response rate** (respondents ÷ eligible participants).
- Only the value **reported by the patient** counts. `alert_grade` is an operational signal raised by the monitoring rules; it is not the reported grade.
- Items on other scales (e.g. a 0–10 pain scale) cannot be mixed with 0–4 items and are out of scope.

## Your mission (1 hour)

Treat this as a pre-release review of a feature you now own. Two questions drive the review:

> 1. **Can this endpoint ship to the sponsor next week?**
> 2. **Is the ONC-101 / GENERAL_PAIN figure for January–June 2026 right? If not, what should it be, and why?**

Suggested split of the hour:

| Step | Time |
|---|---|
| 1. Audit | ~15 min |
| 2. Triage | ~5 min |
| 3. Fix | ~30 min |
| 4. Write your notes | ~10 min |

1. **Audit.** Review the repository as you would a codebase you are taking over, before changing anything. Cover:
   - code quality and readability;
   - architecture and structure of the repository;
   - security;
   - error handling;
   - data model, dbt models and metric correctness;
   - tests;
   - delivery: Docker, configuration, CI.

   For each finding, note where you saw it (file, function or model) and how severe it is.
2. **Triage.** Decide what blocks the release and what can wait. For each blocker, explain its impact on the study or the sponsor, not only on the code.
3. **Fix what matters most.** Change the code, the dbt models and/or the tests for your top priorities. A small, well-tested fix beats a broad unfinished one.
4. **Write it down** in [`NOTES.md`](NOTES.md), following its structure: verdict, audit, blockers, changes, next steps, AI usage.

You are **not** expected to fix everything, or even to write a lot of code. A clear verdict, a structured audit and a well-argued triage are a valid outcome. The discussion that follows builds on your notes.

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

Database: `localhost:5432`, database `rdp`, user `rdp`, password `rdp`.

## Calling the API

Every endpoint except `/health` needs a token. Generate one with `make token STUDIES="ONC-101"`.

**curl**:

```bash
TOKEN=$(make -s token STUDIES="ONC-101")
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/studies/ONC-101/symptoms/GENERAL_PAIN/summary?start_date=2026-01-01&end_date=2026-06-30"
```

API documentation (Swagger UI): http://localhost:8000/docs

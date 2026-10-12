# Data model

Postgres database `rdp`. Raw synthetic data is loaded by `dbt seed` into schema `raw`; dbt models are built into schema `analytics`.

```
raw.studies ─┐
raw.participants ──────────────┐
raw.questionnaire_occurrences ─┼─► analytics.ods_* ─► analytics.int_symptom_answer ─► analytics.mart_symptom_answer
raw.questionnaire_answers ─────┤                                                           ▲
raw.symptom_items ─────────────┘                                                     read by the API
```

## Raw tables

### `raw.studies` — one row per study

| study_code | study_name | start_date |
|---|---|---|
| ONC-101 | Adjuvant breast cancer ePRO follow-up | 2025-09-01 |
| ONC-102 | Colorectal cancer ePRO pilot | 2026-02-01 |

### `raw.participants` — one row per participant

`end_date` is set when follow-up ended; `end_reason` is `COMPLETED` or `WITHDRAWN_CONSENT`.

| participant_id | study_code | site_code | inclusion_date | end_date | end_reason |
|---|---|---|---|---|---|
| ONC101-001 | ONC-101 | SITE-A | 2025-10-23 | | |
| ONC101-002 | ONC-101 | SITE-A | 2025-12-11 | 2026-02-27 | COMPLETED |

### `raw.questionnaire_occurrences` — one row per questionnaire sent

- `trigger_type`: `SCHEDULED` (weekly, sent by the platform) or `UNSCHEDULED` (opened by the patient).
- `status`: `ANSWERED` or `EXPIRED` (not answered).
- `questionnaire_version`: `v1` or `v2`. The two versions ask different items.

| occurrence_id | participant_id | questionnaire_version | trigger_type | triggered_at | status |
|---|---|---|---|---|---|
| OCC-000001 | ONC101-001 | v1 | SCHEDULED | 2025-10-27 09:00:00 | EXPIRED |
| OCC-000002 | ONC101-001 | v1 | SCHEDULED | 2025-11-03 09:00:00 | ANSWERED |

### `raw.questionnaire_answers` — one row per submitted answer

`answer_value` is stored as text (empty when the item was skipped). `alert_grade` is the grade of the alert raised by the monitoring rules on this answer (0 = no alert).

| answer_id | occurrence_id | item_code | answer_value | answered_at | alert_grade |
|---|---|---|---|---|---|
| ANS-0000001 | OCC-000002 | GP_SEV | 0 | 2025-11-03 21:31:00 | 0 |
| ANS-0000003 | OCC-000002 | GP_INT | 1 | 2025-11-03 21:31:00 | 0 |
| ANS-0000005 | OCC-000002 | FAT_SEV | 2 | 2025-11-03 21:31:00 | 2 |

### `raw.symptom_items` — item catalog

| item_code | symptom_code | symptom_label | attribute | scale_min | scale_max |
|---|---|---|---|---|---|
| GP_SEV | GENERAL_PAIN | General pain | severity | 0 | 4 |
| GP_FREQ | GENERAL_PAIN | General pain | frequency | 0 | 4 |
| GP_INT | GENERAL_PAIN | General pain | interference | 0 | 4 |
| GP_NRS | GENERAL_PAIN | General pain | intensity | 0 | 10 |
| AP_SEV | ABDOMINAL_PAIN | Abdominal pain | severity | 0 | 4 |
| FAT_SEV | FATIGUE | Fatigue | severity | 0 | 4 |
| FAT_INT | FATIGUE | Fatigue | interference | 0 | 4 |
| NAU_FREQ | NAUSEA | Nausea | frequency | 0 | 4 |
| NAU_SEV | NAUSEA | Nausea | severity | 0 | 4 |

Questionnaire `v1` asks `GP_SEV, GP_FREQ, GP_INT, AP_SEV, FAT_SEV, FAT_INT, NAU_FREQ, NAU_SEV`.
Questionnaire `v2` asks `GP_NRS, AP_SEV, FAT_SEV, FAT_INT, NAU_FREQ, NAU_SEV`.

## dbt models

| Model | Materialization | Grain |
|---|---|---|
| `ods_*` | view | Same as the raw table, typed |
| `int_symptom_answer` | view | One row per answer, joined to its occurrence, participant and item |
| `mart_symptom_answer` | table | One row per answer; read by the API |

## Volumes

| Table | Rows |
|---|---|
| participants | 62 (50 in ONC-101, 12 in ONC-102) |
| questionnaire_occurrences | 2,711 |
| questionnaire_answers | 14,848 |

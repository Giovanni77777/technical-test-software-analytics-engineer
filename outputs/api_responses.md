# Current behaviour (captured)

Captured on the starter repository with `make up`, using a token that grants access to **ONC-101 only** (`make token STUDIES="ONC-101"`).

## `GET /health`

Status: `200`

```json
{
    "status": "ok"
}
```

## `GET /studies/ONC-101/symptoms/GENERAL_PAIN/summary?start_date=2026-01-01&end_date=2026-06-30`

Status: `200`

```json
{
    "study": "Adjuvant breast cancer ePRO follow-up",
    "symptom": "GENERAL_PAIN",
    "participants": 44,
    "cases": 21,
    "prevalence": 0.48,
    "mean_grade": 0.47,
    "answers": 2350
}
```

## `GET /studies/ONC-101/symptoms/FATIGUE/summary?start_date=2026-01-01&end_date=2026-06-30`

Status: `500`

```json
Internal Server Error
```

## `GET /studies/ONC-102/symptoms/GENERAL_PAIN/summary?start_date=2026-01-01&end_date=2026-06-30`

Status: `200`

```json
{
    "study": "Colorectal cancer ePRO pilot",
    "symptom": "GENERAL_PAIN",
    "participants": 12,
    "cases": 12,
    "prevalence": 1.0,
    "mean_grade": 1.16,
    "answers": 525
}
```

## `GET /studies/ONC-999/symptoms/GENERAL_PAIN/summary?start_date=2026-01-01&end_date=2026-06-30`

Status: `500`

```json
Internal Server Error
```

## `GET /studies/ONC-101/symptoms/GENERAL_PAIN/summary?start_date=2026-06-30&end_date=2026-01-01`

Status: `500`

```json
Internal Server Error
```

## `GET /studies/ONC-101/observations`

Status: `200` — 12472 rows, 4452106 bytes, 0.412872s. First row:

```json
{
  "answer_id": "ANS-0000157",
  "occurrence_id": "OCC-000025",
  "participant_id": "ONC101-001",
  "study_code": "ONC-101",
  "questionnaire_version": "v1",
  "trigger_type": "SCHEDULED",
  "symptom_code": "FATIGUE",
  "symptom_label": "Fatigue",
  "attribute": "severity",
  "scale_max": 4,
  "answer_value": "0",
  "alert_grade": 0,
  "answered_at": "2026-04-14T08:57:00",
  "weeks_from_inclusion": 23
}
```

## Server logs for the 500 responses

```
FATIGUE summary        -> TypeError: float() argument must be a string or a real number, not 'NoneType'   (app/main.py, symptom_summary)
ONC-999 summary        -> KeyError: 'ONC-999'                                                            (app/main.py, symptom_summary)
start_date > end_date  -> ZeroDivisionError: division by zero                                           (app/main.py, symptom_summary)
```

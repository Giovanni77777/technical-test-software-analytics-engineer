import logging
from datetime import date

from fastapi import Depends, FastAPI

from app.auth import get_current_user
from app.db import get_connection

logger = logging.getLogger(__name__)

app = FastAPI(title="Research Data Platform - Symptom API")


def load_studies():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("select study_code, study_name from analytics.ods_studies")
        return {row[0]: {"study_code": row[0], "study_name": row[1]} for row in cur.fetchall()}
    except Exception:
        return {}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/studies/{study_code}/observations")
def list_observations(study_code: str, user=Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("select * from analytics.mart_symptom_answer where study_code = %s", (study_code,))
    columns = [c.name for c in cur.description]
    return [dict(zip(columns, row)) for row in cur.fetchall()]


@app.get("/studies/{study_code}/symptoms/{symptom_code}/summary")
def symptom_summary(
    study_code: str,
    symptom_code: str,
    start_date: date,
    end_date: date,
    user=Depends(get_current_user),
):
    study = load_studies()[study_code]
    logger.info("summary requested by %s for %s/%s", user["email"], study_code, symptom_code)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        f"""
        select distinct participant_id
        from analytics.mart_symptom_answer
        where study_code = '{study_code}'
          and symptom_code = '{symptom_code}'
          and answered_at between '{start_date}' and '{end_date}'
        """
    )
    participants = [row[0] for row in cur.fetchall()]

    cases = 0
    answers = 0
    grade_sum = 0.0
    for participant_id in participants:
        cur.execute(
            f"""
            select answer_value
            from analytics.mart_symptom_answer
            where participant_id = '{participant_id}'
              and symptom_code = '{symptom_code}'
              and answered_at between '{start_date}' and '{end_date}'
            """
        )
        values = [float(row[0]) for row in cur.fetchall()]
        answers += len(values)
        grade_sum += sum(values)
        if max(values) >= 2:
            cases += 1

    return {
        "study": study["study_name"],
        "symptom": symptom_code,
        "participants": len(participants),
        "cases": cases,
        "prevalence": round(cases / len(participants), 2),
        "mean_grade": round(grade_sum / answers, 2),
        "answers": answers,
    }

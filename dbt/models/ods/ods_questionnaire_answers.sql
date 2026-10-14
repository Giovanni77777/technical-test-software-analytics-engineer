select
    answer_id,
    occurrence_id,
    item_code,
    answer_value,
    answered_at,
    alert_grade
from {{ ref('questionnaire_answers') }}

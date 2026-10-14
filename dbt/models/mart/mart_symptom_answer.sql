-- Symptom answers ready for reporting.
-- TODO: prevalence and mean grade are still computed in the API.
with answers as (

    select * from {{ ref('int_symptom_answer') }}

)

select
    answer_id,
    occurrence_id,
    participant_id,
    study_code,
    questionnaire_version,
    trigger_type,
    symptom_code,
    symptom_label,
    attribute,
    scale_max,
    answer_value,
    alert_grade,
    answered_at,
    floor(
        extract(epoch from answered_at - min(answered_at) over (partition by participant_id)) / 604800
    )::int as weeks_from_inclusion
from answers

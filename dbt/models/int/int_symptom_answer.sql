-- One row per answer to a symptom item.
select
    answers.answer_id,
    answers.occurrence_id,
    occurrences.participant_id,
    participants.study_code,
    occurrences.questionnaire_version,
    occurrences.trigger_type,
    items.item_code,
    items.symptom_code,
    items.symptom_label,
    items.attribute,
    items.scale_max,
    answers.answer_value,
    answers.alert_grade,
    answers.answered_at
from {{ ref('ods_questionnaire_answers') }} as answers
inner join {{ ref('ods_questionnaire_occurrences') }} as occurrences
    on answers.occurrence_id = occurrences.occurrence_id
inner join {{ ref('ods_participants') }} as participants
    on occurrences.participant_id = participants.participant_id
inner join {{ ref('ods_symptom_items') }} as items
    on answers.item_code = items.item_code

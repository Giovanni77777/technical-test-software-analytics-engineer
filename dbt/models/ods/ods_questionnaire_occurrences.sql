select
    occurrence_id,
    participant_id,
    questionnaire_version,
    trigger_type,
    triggered_at,
    status
from {{ ref('questionnaire_occurrences') }}

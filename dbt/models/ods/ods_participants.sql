select
    participant_id,
    study_code,
    site_code,
    inclusion_date,
    end_date,
    end_reason
from {{ ref('participants') }}

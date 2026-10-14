select
    study_code,
    study_name,
    start_date::date as start_date
from {{ ref('studies') }}

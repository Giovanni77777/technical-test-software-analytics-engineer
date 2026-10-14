select
    item_code,
    symptom_code,
    symptom_label,
    attribute,
    scale_min::int as scale_min,
    scale_max::int as scale_max,
    item_text
from {{ ref('symptom_items') }}

{{ config(materialized = "table") }}

select
    "project_code"::varchar as project_code,
    "project_name"::varchar as project_name
from {{ source('bronze', 'project_codes') }}
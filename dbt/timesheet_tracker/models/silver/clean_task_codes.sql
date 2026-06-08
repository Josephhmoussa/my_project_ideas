{{ config(materialized="table") }}

select
    "task_code"::varchar as task_code,
    "cpx_opx"::varchar as cpx_opx
from {{ source('bronze', 'task_codes') }}
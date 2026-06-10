{{ config(materialized='table') }}

select
    ct.organization,
    ct.manager,
    ct.employee_id,
    ct.employee_name,
    ct.category,
    ct.project_code,
    cp.project_name,
    ct.task_code,
    tc.cpx_opx,
    ct.week_date,
    ct.hours
from {{ ref('clean_timesheet') }} as ct
left join {{ ref('clean_project_codes')}} as cp
    on ct.project_code = cp.project_code
left join {{ ref('clean_task_codes') }} as tc
    on ct.task_code = tc.task_code
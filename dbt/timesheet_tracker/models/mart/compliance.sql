{{ config(materialized='table') }}

with aggregated_metrics as (
    select
        employee_id,
        week_date,
        sum(hours) as total_hours,
        sum(project_hours) as total_project_hours,
        sum(case when project_name = 'Global Admin' then hours else 0 end) as admin_hours,
        sum(case when cpx_opx = 'Capex' then project_hours else 0 end) as capex_hours,
        sum(case when cpx_opx = 'Opex' then project_hours else 0 end) as opex_hours,
        sum(case when task_code = '1D - Leave & Absences' then hours else 0 end) as leave_hours,
        sum(case when category = 'submitted' then hours else 0 end) as submitted_hours,
        sum(case when category = 'not_submitted' then hours else 0 end) as not_submitted_hours,
        sum(case when category = 'created_not_submitted' then hours else 0 end) as created_not_submitted_hours
    from {{ ref('fact_timesheet') }}
    group by employee_id, week_date
),

ratios as (
    select
        *,
        case when total_project_hours > 0 then (capex_hours / total_project_hours) else 0 end::float as capex_ratio,
        case when total_project_hours > 0 then (opex_hours / total_project_hours) else 0 end::float as opex_ratio,
        case when leave_hours in (37.5, 40) then 1 else 0 end as is_leave_week
    from aggregated_metrics
),

conditions as (
    select
        *,
        case
            when total_hours between 35 and 41 and not_submitted_hours = 0 then 1 else 0 end as time_ok,
        case    
            when is_leave_week = 1 then 1
            when capex_ratio between 0.10 and 0.30 and opex_ratio between 0.70 and 0.90 then 1
            else 0
        end as mix_ok,
        case
            when admin_hours <= 20 and not_submitted_hours = 0 then 1 else 0 end as admin_ok
    from ratios
)

select *
from conditions
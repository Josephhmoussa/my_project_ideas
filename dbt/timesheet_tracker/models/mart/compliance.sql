{{ config(materialized='table') }}

with aggregated_metrics as (
    select
        employee_id,
        week_date,
        sum(hours) as total_hours,
        sum(project_hours) as total_project_hours,
        sum(case when cpx_opx = 'Capex' then project_hours else 0 end) as capex_hours,
        sum(case when cpx_opx= 'Opex' then project_hours else 0 end) as opex_hours,
        sum(case when project_name = 'Leave & Absences' then hours else 0 end) as leave_hours,
        sum(case when category = 'submitted' then hours else 0 end) as submitted_hours,
        sum(case when category = 'not_submitted' then hours else 0 end) as not_submitted_hours,
        sum(case when category = 'created_not_submitted' then hours else 0 end) as created_not_submitted_hours
    from {{ ref('fact_timesheet') }}
    group by employee_id, week_date
)

select *
from aggregated_metrics
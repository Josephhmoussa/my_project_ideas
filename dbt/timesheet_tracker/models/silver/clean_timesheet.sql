{{ config(materialized='table') }}

with unpivoted as (
    {{
        dbt_utils.unpivot(
            relation=ref('stg_timesheets'),
            cast_to='varchar',
            exclude=[
                'organization',
                'manager_name',
                'employee_id',
                'employee_name',
                'category',
                'ingested_at',
                'project_number',
                'task_number',
                'org_level_4_name',
                'grand_total',
                'year'
            ],
            field_name='week_label',
            value_name='hours'
        )
    }}
),

selection as (
    select
        split_part(split_part(organization, ':', 2), '_', 1)::varchar as cost_center,
        manager_name::varchar as manager_name,
        employee_id::int as employee_id,
        employee_name::varchar as employee_name,
        case
            when category = 'full' then 'submitted'
            when category = 'missing' then 'not_submitted'
            when category = 'saved' then 'created_not_submitted'
            else null
        end::varchar as category,
        ingested_at::timestamp as ingested_at,
        case
            when project_number != 'ADMIN' then split_part(project_number, '-', 2) else project_number end::varchar as project_code,
        case
            when project_number = 'ADMIN' and task_number = '1C' then '1C - Admin & Mgt'
            when project_number = 'ADMIN' and task_number = '1D' then '1D - Leave & Absences'
            else task_number
        end::varchar as task_code,
        try_to_date(
            split_part(week_label, '_', 2) || '-' ||
            initcap(split_part(week_label, '_', 3)) || '-' || year::int,
            'DD-Mon-YYYY'
        )as week_date,
        try_to_number(hours) as hours
    from unpivoted
    where org_level_4_name != 'Grand Total' 
        and hours is not null
        and not (category = 'full' and project_number is null)
),

deduped as (
    select *
    from selection
    qualify row_number() over (
        partition by employee_id, week_date, project_code, task_code order by ingested_at desc
    ) = 1
)

select *
from deduped
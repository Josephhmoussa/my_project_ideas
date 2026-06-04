{{ config(materialized='table') }}

with unpivoted as (
    {{
        dbt_utils.unpivot(
            relation=ref('stg_timesheets'),
            cast_to='varchar',
            exclude=[
                'organization',
                'manager',
                'employee_id',
                'employee_name',
                'category',
                'ingested_at',
                'project_number',
                'task_number',
                'org_level_4_name',
                'grand_total'
            ],
            field_name='week_label',
            value_name='hours'
        )
    }}
),

selection as (
    select
        split_part(organization, ':', 1)::varchar as organization,
        manager::varchar as manager,
        employee_id::int as employee_id,
        employee_name::varchar as employee_name,
        category::varchar as category,
        ingested_at::timestamp as ingested_at,
        project_number::varchar as project_number,
        task_number::varchar as task_number,
        try_to_date(
            split_part(week_label, '_', 2) || '-' ||
            initcap(split_part(week_label, '_', 3)) || '-2025',
            'DD-Mon-YYYY'
        )as week_date,
        try_to_number(hours) as hours
    from unpivoted
    where hours is not null
        and employee_id is not null
),

deduped as (
    select *
    from selection
    qualify row_number() over (
        partition by employee_id, week_date order by ingested_at desc
    ) = 1
)

select *
from deduped
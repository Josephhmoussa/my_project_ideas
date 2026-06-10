{{ config(materialized='table') }}

select distinct
    employee_id,
    employee_name,
    manager_name,
    cost_center
from {{ ref('fact_timesheet') }}
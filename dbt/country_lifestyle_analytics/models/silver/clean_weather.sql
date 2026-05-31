{{ config(materialized='table') }}

with raw as (

    select
        raw:city::string as city,
        raw:ingested_at::timestamp as ingested_at,
        f.value::date as date,
        raw:data:daily:temperature_2m_max[f.index]::float as temperature_2m_max,
        raw:data:daily:precipitation_sum[f.index]::float as precipitation_sum,
        raw:data:daily:sunshine_duration[f.index]::float as sunshine_duration,
        raw:data:latitude::float as latitude,
        raw:data:longitude::float as longitude
    from {{ source('bronze', 'weather_raw') }},
        lateral flatten(input => raw:data:daily:time) f
),

deduped as (

    select
        *,
        row_number() over (partition by city, date order by ingested_at desc) as rn
    from raw
)

select
    city,
    date,
    temperature_2m_max,
    sunshine_duration,
    precipitation_sum,
    latitude,
    longitude,
    ingested_at
from deduped
where rn = 1
# Timesheet Compliance Pipeline

An end-to-end data engineering project that ingests employee timesheets, loads them into a Snowflake data warehouse via AWS S3, transforms them through a multi-layer dbt model, and surfaces compliance KPIs in a Power BI dashboard.

Built as a portfolio project demonstrating a modern analytical engineering stack.

---

## Architecture

```
CSV Files (local)
      │
      ▼
┌─────────────────┐
│  Dagster Asset  │  Python · Polars
│  (Ingestion)    │  Reads & validates raw timesheets
└────────┬────────┘
         │ Upload as Parquet
         ▼
┌─────────────────┐
│    AWS S3       │  Bronze layer (raw Parquet files)
│  Data Lake      │
└────────┬────────┘
         │ COPY INTO via external stage
         ▼
┌─────────────────┐
│   Snowflake     │  Cloud data warehouse
│  (Bronze Layer) │  Key-pair auth via AWS Secrets Manager
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│              dbt Transformations            │
│                                             │
│  Staging → Silver → Gold → Mart             │
│  (rename)  (clean)  (model) (compliance)    │
└────────┬────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│   Power BI      │  Compliance KPI dashboard
│   Dashboard     │
└─────────────────┘
```

All assets are orchestrated end-to-end by **Dagster**, with dependencies managed through the asset graph.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Orchestration | Dagster |
| Ingestion | Python, Polars, Boto3 |
| Data Lake | AWS S3 |
| Data Warehouse | Snowflake |
| Transformation | dbt Core + dbt_utils |
| Secrets Management | AWS Secrets Manager |
| Visualisation | Power BI |

---

## Data Model

### dbt Layers

```
bronze (Snowflake raw tables)
  └── staging/
        └── stg_timesheets          ← Rename columns, unpivot 52 weekly columns into rows
  └── silver/
        ├── clean_timesheet         ← Type casting, dedup, business rule normalisation
        ├── clean_project_codes     ← Project code lookup
        └── clean_task_codes        ← Task code lookup (Capex/Opex classification)
  └── gold/
        ├── fact_timesheet          ← Core fact table (employee · week · project · hours)
        └── dim_employees           ← Employee dimension (unique per employee_id)
  └── mart/
        └── compliance              ← Per-employee, per-week compliance scoring
```

### Compliance Scoring Logic

Each employee-week record is evaluated against three compliance dimensions:

| Dimension | Rule |
|---|---|
| `time_ok` | Total hours between 35–41 and all entries fully submitted |
| `mix_ok` | Capex ratio 10–30%, Opex ratio 70–90% (or a full leave week) |
| `admin_ok` | Admin hours ≤ 20 and all entries fully submitted |

**Final score:** `2` = fully compliant · `1` = submitted but rule violation · `0` = not submitted

---

## Project Structure

```
├── prod_pipeline/                  # Dagster pipeline
│   ├── assets/
│   │   └── timesheet_tracker/
│   │       ├── assets_ingest_bronze_timesheet.py   # S3 ingestion asset
│   │       ├── assets_copy_into_snowflake.py       # Snowflake load asset
│   │       ├── assets_dbt_transformation.py        # dbt build asset
│   │       ├── generate.py                         # Synthetic demo data generator
│   │       ├── csv_files/                          # Raw timesheet CSVs (input)
│   │       └── lookup_files/                       # Project & task code lookups
│   ├── resources/
│   │   └── dbt_resource.py                         # DbtCliResource configuration
│   └── utils/
│       ├── datalakeclient.py                       # S3 wrapper (upload/download)
│       └── snowflakeclient.py                      # Snowflake wrapper (key-pair auth)
│
├── dbt/timesheet_tracker/          # dbt project
│   ├── models/
│   │   ├── staging/
│   │   ├── silver/
│   │   ├── gold/
│   │   └── mart/
│   ├── macros/
│   │   └── generate_schema_name.sql
│   └── packages.yml                # dbt_utils dependency
│
├── requirements.txt
└── workspace.yaml
```

---

## Setup & Running Locally

### Prerequisites

- Python 3.11+
- AWS credentials configured (via `~/.aws/credentials` or an IAM role)
- Snowflake account with key-pair authentication stored in AWS Secrets Manager
- dbt profile configured at `~/.dbt/profiles.yml`

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
TIMESHEET_DBT_PROJECT_DIR=./dbt/timesheet_tracker
DBT_PROFILES_DIR=~/.dbt
```

### 3. Generate demo data (optional)

Uncomment and run the synthetic data generator to produce sample timesheet CSVs:

```bash
python prod_pipeline/assets/timesheet_tracker/generate.py
```

This creates realistic timesheet data for ~20 employees across 3 teams, covering a full 52-week year.

### 4. Install dbt packages

```bash
cd dbt/timesheet_tracker
dbt deps
```

### 5. Launch Dagster

```bash
dagster dev
```

Open `http://localhost:3000`, navigate to the **Assets** tab, and materialise the `timesheet_pipeline` asset group in order:

1. `ingest_bronze_lookup` + `ingest_bronze_timesheet`
2. `copy_project_codes_into_snowflake` + `copy_timesheets_into_snowflake`
3. `transform_timesheet` (runs full dbt build)

---

## Dashboard

The Power BI dashboard connects directly to Snowflake and visualises:

- Weekly compliance rate by team and employee
- Capex / Opex split trends over time
- Timesheet submission status breakdown
- Admin hours distribution
- Compliance score distribution (0 / 1 / 2)

> **Note:** A video walkthrough of the dashboard is available [here — add your Loom link].

---

## Key Design Decisions

**Why Dagster?**
Asset-based orchestration makes dependencies explicit and gives full visibility into materialisation history, run metadata, and data previews — closer to how production pipelines are managed.

**Why Polars?**
Faster than pandas for the column-scan operations used during ingestion, with no extra infrastructure needed for small-to-medium CSV volumes.

**Why key-pair auth + Secrets Manager?**
Avoids storing credentials in environment files or code. The Snowflake private key and connection credentials are fetched at runtime from AWS Secrets Manager, which is the recommended pattern for production workloads.

**Why a mart layer?**
Separates reusable dimensional models (`gold`) from business-specific aggregations (`mart`). The compliance mart can be rebuilt or changed without touching the underlying fact and dimension tables.

---

## What I'd Add Next

- [ ] Incremental dbt models to avoid full table rebuilds on each run
- [ ] Idempotent Snowflake load (swap + rename pattern instead of truncate-then-load)
- [ ] GitHub Actions CI running `dbt compile` and `dbt test` on every PR
- [ ] dbt source freshness checks
- [ ] Alerting on compliance threshold breaches via Dagster sensors

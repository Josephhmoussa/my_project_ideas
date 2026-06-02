import polars as pl
from pathlib import Path
from datetime import datetime, UTC

path = Path("prod_pipeline/assets/timesheet_tracker/csv_files/")

def ingest_bronze_timesheet(path: Path) -> pl.DataFrame:
    '''Ingest csv files with minimal transformations and upload to S3'''

    dfs = []
    for file in path.rglob("*.csv"):
        category = str(file).split("/")[-1].split("_")[1]
        ingested_at = datetime.now(UTC).strftime("%Y-%m-%d-%H:%M:%S")
        df = pl.read_csv(file)

        df = df.with_columns([
            pl.lit(category)
            .cast(pl.Utf8)
            .alias("category"),

            pl.lit(ingested_at)
            .str.to_datetime("%Y-%m-%d-%H:%M:%S")
            .alias("ingested_at")
        ])

        dfs.append(df)

    return dfs

if __name__ == "__main__":
    result = ingest_bronze_timesheet(path)

    print(result)
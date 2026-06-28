from dagster_dbt import DbtCliResource, DagsterDbtTranslator, DbtProject
from dotenv import load_dotenv
import os


load_dotenv()

TIMESHEET_DBT_PROJECT_DIR = os.getenv("TIMESHEET_DBT_PROJECT_DIR")
DBT_PROFILES_DIR = os.getenv("DBT_PROFILES_DIR")

# Define dbt project
timesheet_dbt_project = DbtProject(
    project_dir=TIMESHEET_DBT_PROJECT_DIR,
    profiles_dir=DBT_PROFILES_DIR
)

# DbtCliResource per pipeline
timesheet_dbt_resource = DbtCliResource(project_dir=TIMESHEET_DBT_PROJECT_DIR)

class TimesheetDbtTranslator(DagsterDbtTranslator):
    def get_group_name(self, dbt_resource_props):
        return "timesheet_pipeline"
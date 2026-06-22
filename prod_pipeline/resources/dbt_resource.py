from dagster_dbt import DbtCliResource, DagsterDbtTranslator, DbtProject
from dotenv import load_dotenv
import os


load_dotenv()

WEATHER_DBT_PROJECT_DIR = os.getenv("WEATHER_DBT_PROJECT_DIR")
TIMESHEET_DBT_PROJECT_DIR = os.getenv("TIMESHEET_DBT_PROJECT_DIR")
DBT_PROFILES_DIR = os.getenv("DBT_PROFILES_DIR")

# Define dbt project
weather_dbt_project = DbtProject(
    project_dir=WEATHER_DBT_PROJECT_DIR,
    profiles_dir=DBT_PROFILES_DIR
)

timesheet_dbt_project = DbtProject(
    project_dir=TIMESHEET_DBT_PROJECT_DIR,
    profiles_dir=DBT_PROFILES_DIR
)

# DbtCliResource per pipeline
weather_dbt_resource = DbtCliResource(project_dir=WEATHER_DBT_PROJECT_DIR)
timesheet_dbt_resource = DbtCliResource(project_dir=TIMESHEET_DBT_PROJECT_DIR)

class WeatherDbtTranslator(DagsterDbtTranslator):
    def get_group_name(self, dbt_resource_props):
        return "country_lifestyle_analytics"

class TimesheetDbtTranslator(DagsterDbtTranslator):
    def get_group_name(self, dbt_resource_props):
        return "timesheet_pipeline"
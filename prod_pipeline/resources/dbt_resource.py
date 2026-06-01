from dagster_dbt import DbtCliResource, DagsterDbtTranslator, DbtProject
from dotenv import load_dotenv
import os


load_dotenv()
DBT_PROJECT_DIR = os.getenv("DBT_PROJECT_DIR")
DBT_PROFILES_DIR = os.getenv("DBT_PROFILES_DIR")

# Define dbt project
dbt_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
    profiles_dir=DBT_PROFILES_DIR
)

dbt_resource = DbtCliResource(project_dir=DBT_PROJECT_DIR)

class WeatherDbtTranslator(DagsterDbtTranslator):
    def get_group_name(self, dbt_resource_props):
        return "country_lifestyle_analytics"
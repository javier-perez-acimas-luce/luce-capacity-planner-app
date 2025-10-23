import os
from datetime import datetime

import pytz
from flasgger import Swagger
from flask import Flask, jsonify, Response, render_template, request
from google.cloud import bigquery
from google.api_core.exceptions import NotFound


from app_name.utils import io
from app_name.utils.logger import logger, log
from app_name.utils.metric import Metric
from app_name.utils.monitoring import Monitoring
from app_name.utils.writers import CsvWriter

app = Flask(__name__)
config = io.load_config_by_env()
SCRIPT_START_TS = datetime.now(pytz.utc).isoformat()

# Obtener la ruta absoluta del archivo swagger.yaml
base_dir = os.path.abspath(os.path.dirname(__file__))  # Ruta de la carpeta src/
swagger_path = os.path.join(base_dir, '..', 'swagger.yaml')  # Subir un nivel y apuntar a swagger.yaml
# Configurar Swagger para que use el archivo swagger.yaml
swagger = Swagger(app, template_file=swagger_path)

# --- BigQuery Client Initialization ---
# This will use the environment's default credentials
# (e.g., from GOOGLE_APPLICATION_CREDENTIALS or GKE Workload Identity)
try:
    bigquery_client = bigquery.Client()
    logger.info("BigQuery client initialized successfully.")
except Exception as e:
    logger.critical(f"Failed to initialize BigQuery client: {e}")
    bigquery_client = None

# --- !!! IMPORTANT: CONFIGURE YOUR TABLE NAMES HERE !!! ---
# Replace with your actual project, dataset, and table names.
PROJECT_ID = "olimpo-bi"

SPRINTS_TABLE = f"`{PROJECT_ID}.sprints.luce_calendarSprint`"
PROJECTS_TABLE = f"`{PROJECT_ID}.projects.luce_projects`"
TEAM_MEMBERS_TABLE = f"`{PROJECT_ID}.people.luce_people`"
ASSIGNMENTS_TABLE = f"`{PROJECT_ID}.capacity_planner_app.people_assignment`"
PROJECT_CASES_TABLE = f"`{PROJECT_ID}.capacity_planner_app.project_assignment`"
# --- API Endpoints ---

@app.route("/api/sprints", methods=['GET'])
def get_sprints():
    if not bigquery_client:
        return jsonify({"error": "BigQuery client not initialized"}), 500

    query = f"""
        SELECT DISTINCT calendar_sprint_str_i as sprint_name
        FROM {SPRINTS_TABLE}
        WHERE calendar_date_date_i > CURRENT_DATE()
        ORDER BY calendar_sprint_str_i ASC
    """
    try:
        query_job = bigquery_client.query(query)
        results = query_job.result()
        sprints = [row.sprint_name for row in results]
        logger.info(f"Successfully fetched {len(sprints)} sprints.")
        return jsonify(sprints)
    except NotFound:
        logger.error(f"Table not found: {SPRINTS_TABLE}")
        return jsonify({"error": f"Table not found: {SPRINTS_TABLE}"}), 500
    except Exception as e:
        logger.error(f"Error in /api/sprints: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/projects-and-groups", methods=['GET'])
def get_projects_and_groups():
    if not bigquery_client:
        return jsonify({"error": "BigQuery client not initialized"}), 500

    projects_query = f"""
        SELECT project_code_int_i as id, project_name_str_i as name, project_bussinesLine_str_d as project_group
        FROM {PROJECTS_TABLE}
        ORDER BY project_name_str_i
    """
    groups_query = f"""
        SELECT DISTINCT project_bussinesLine_str_d as project_group
        FROM {PROJECTS_TABLE}
        WHERE project_bussinesLine_str_d IS NOT NULL
        ORDER BY project_bussinesLine_str_d
    """
    try:
        # Fetch projects
        projects_job = bigquery_client.query(projects_query)
        projects = [dict(row) for row in projects_job.result()]

        # Fetch groups
        groups_job = bigquery_client.query(groups_query)
        # Prepend "All Groups" to the list
        project_groups = ['All Groups'] + [row.project_group for row in groups_job.result()]

        logger.info(f"Fetched {len(projects)} projects and {len(project_groups) - 1} groups.")
        return jsonify({
            'projects': projects,
            'projectGroups': project_groups
        })
    except NotFound:
        logger.error(f"Table not found: {PROJECTS_TABLE}")
        return jsonify({"error": f"Table not found: {PROJECTS_TABLE}"}), 500
    except Exception as e:
        logger.error(f"Error in /api/projects-and-groups: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/team-data", methods=['GET'])
def get_team_data():
    if not bigquery_client:
        return jsonify({"error": "BigQuery client not initialized"}), 500

    members_query = f"""
        SELECT person_name_str_i as id, person_name_str_i as name, person_chapter_str_d as team, person_team_str_d as subteam, person_workDaysTotal_float_i as expectedDays
        FROM {TEAM_MEMBERS_TABLE}
        ORDER BY person_chapter_str_d, person_team_str_d, person_name_str_i
    """
    teams_query = f"""
        SELECT DISTINCT person_chapter_str_d as team
        FROM {TEAM_MEMBERS_TABLE}
        WHERE person_chapter_str_d IS NOT NULL
        ORDER BY person_chapter_str_d
    """
    try:
        # Fetch team members
        members_job = bigquery_client.query(members_query)
        team_members = [dict(row) for row in members_job.result()]

        # Fetch teams
        teams_job = bigquery_client.query(teams_query)
        # Prepend "All Teams"
        teams = ['All Teams'] + [row.team for row in teams_job.result()]

        logger.info(f"Fetched {len(team_members)} team members and {len(teams) - 1} teams.")
        return jsonify({
            'teamMembers': team_members,
            'teams': teams,
        })
    except NotFound:
        logger.error(f"Table not found: {TEAM_MEMBERS_TABLE}")
        return jsonify({"error": f"Table not found: {TEAM_MEMBERS_TABLE}"}), 500
    except Exception as e:
        logger.error(f"Error in /api/team-data: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/sprint-data", methods=['GET'])
def get_sprint_data():
    if not bigquery_client:
        return jsonify({"error": "BigQuery client not initialized"}), 500

    sprints_str = request.args.get('sprints', '')
    if not sprints_str:
        return jsonify({"error": "No sprints provided"}), 400

    sprints_list = sprints_str.split(',')
    logger.info(f"Serving data for /api/sprint-data for sprints: {sprints_list}")

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ArrayQueryParameter("sprints", "STRING", sprints_list)
        ]
    )

    assignments_query = f"""
        SELECT sprint, project_id as projectId, person_name as memberID, assignment as days
        FROM {ASSIGNMENTS_TABLE}
        WHERE sprint IN UNNEST(@sprints)
    """
    project_cases_query = f"""
        SELECT sprint, project_id as projectId, team as subteam, assignment as days
        FROM {PROJECT_CASES_TABLE}
        WHERE sprint IN UNNEST(@sprints)
    """

    try:
        # Fetch assignments
        assign_job = bigquery_client.query(assignments_query, job_config=job_config)
        assignments = [dict(row) for row in assign_job.result()]

        # Fetch project cases
        pc_job = bigquery_client.query(project_cases_query, job_config=job_config)
        project_cases = [dict(row) for row in pc_job.result()]

        logger.info(f"Fetched {len(assignments)} assignments and {len(project_cases)} project cases.")
        return jsonify({
            'assignments': assignments,
            'projectCases': project_cases
        })
    except NotFound:
        logger.error(f"Table not found: {ASSIGNMENTS_TABLE} or {PROJECT_CASES_TABLE}")
        return jsonify({"error": "One or more data tables not found."}), 500
    except Exception as e:
        logger.error(f"Error in /api/sprint-data: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/assignment", methods=['POST'])
def update_assignment():
    if not bigquery_client:
        return jsonify({"error": "BigQuery client not initialized"}), 500

    assignment = request.json
    logger.info(f"Updating assignment: {assignment}")

    # Ensure days is an integer
    try:
        days = int(assignment.get('days', 0))
    except ValueError:
        days = 0

    merge_query = f"""
        MERGE INTO {ASSIGNMENTS_TABLE} T
        USING (
            SELECT
                @sprint AS sprint,
                @project_id AS projectId,
                @person_name AS memberId
        ) S
        ON T.sprint = S.sprint AND T.projectId = S.projectId AND T.memberId = S.memberId
        WHEN MATCHED THEN
            UPDATE SET T.days = @days
        WHEN NOT MATCHED THEN
            INSERT (sprint, projectId, memberId, days)
            VALUES (@sprint, @projectId, @memberId, @days)
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("sprint", "STRING", assignment.get('sprint')),
            bigquery.ScalarQueryParameter("projectId", "INT64", int(assignment.get('projectId', 0))),
            bigquery.ScalarQueryParameter("memberId", "STRING", assignment.get('memberId')),
            bigquery.ScalarQueryParameter("days", "INT64", days),
        ]
    )

    try:
        query_job = bigquery_client.query(merge_query, job_config=job_config)
        query_job.result()  # Wait for the job to complete
        logger.info(f"Successfully merged assignment: {assignment}")
        return jsonify(assignment)
    except Exception as e:
        logger.error(f"Error in /api/assignment: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/project-case", methods=['POST'])
def update_project_case():
    if not bigquery_client:
        return jsonify({"error": "BigQuery client not initialized"}), 500

    project_case = request.json
    logger.info(f"Updating project case: {project_case}")

    try:
        days = int(project_case.get('days', 0))
    except ValueError:
        days = 0

    merge_query = f"""
        MERGE INTO {PROJECT_CASES_TABLE} T
        USING (
            SELECT
                @sprint AS sprint,
                @projectId AS projectId,
                @subteam AS subteam
        ) S
        ON T.sprint = S.sprint AND T.projectId = S.projectId AND T.subteam = S.subteam
        WHEN MATCHED THEN
            UPDATE SET T.days = @days
        WHEN NOT MATCHED THEN
            INSERT (sprint, projectId, subteam, days)
            VALUES (@sprint, @projectId, @subteam, @days)
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("sprint", "STRING", project_case.get('sprint')),
            bigquery.ScalarQueryParameter("projectId", "INT64", int(project_case.get('projectId', 0))),
            bigquery.ScalarQueryParameter("subteam", "STRING", project_case.get('subteam')),
            bigquery.ScalarQueryParameter("days", "INT64", days),
        ]
    )

    try:
        query_job = bigquery_client.query(merge_query, job_config=job_config)
        query_job.result()  # Wait for the job to complete
        logger.info(f"Successfully merged project case: {project_case}")
        return jsonify(project_case)
    except Exception as e:
        logger.error(f"Error in /api/project-case: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=['GET'])
def index() -> Response:
    """
    Renderiza la página principal de la aplicación.
    """
    return render_template('index.html')


def main():
    host = io.fetch_env_variable(config, 'HOST')
    port = io.fetch_env_variable(config, 'PORT')
    env = io.fetch_env_variable(config, 'APP_ENV')

    logger.info(log(f"Running the app on {host}:{port}"))

    monitoring = Monitoring(CsvWriter("metrics_example.csv"))
    # Add script common data to metric on development
    metric = Metric(app_env=env, process_name='app_name', script_name=os.path.basename(__file__),
                    root_process_type="FLASK", status="RUNNING", script_start_ts=SCRIPT_START_TS)
    monitoring.write_metric(metric)

    app.run(host=host, port=port)


if __name__ == '__main__':
    logger.debug(log("Starting the app..."))
    main()

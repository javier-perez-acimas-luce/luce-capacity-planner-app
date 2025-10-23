import os
from datetime import datetime

import pytz
from flasgger import Swagger
from flask import Flask, jsonify, Response
from flask_cors import CORS
from google.cloud import bigquery

from app_name.utils import io
from app_name.utils.logger import logger, log
from app_name.utils.metric import Metric
from app_name.utils.monitoring import Monitoring
from app_name.utils.writers import CsvWriter

app = Flask(__name__)
config = io.load_config_by_env()
SCRIPT_START_TS = datetime.now(pytz.utc).isoformat()
CORS(app)

# Obtener la ruta absoluta del archivo swagger.yaml
base_dir = os.path.abspath(os.path.dirname(__file__))  # Ruta de la carpeta src/
swagger_path = os.path.join(base_dir, '..', 'swagger.yaml')  # Subir un nivel y apuntar a swagger.yaml
# Configurar Swagger para que use el archivo swagger.yaml
swagger = Swagger(app, template_file=swagger_path)

# Initialize BigQuery client
# This will use credentials set in the GOOGLE_APPLICATION_CREDENTIALS env variable
try:
    bigquery_client = bigquery.Client()
    print("BigQuery client initialized successfully.")
except Exception as e:
    print(f"Warning: Could not initialize BigQuery client. Running in mock-only mode. Error: {e}")
    bigquery_client = None

# --- Mock Data (Converted from your TypeScript) ---
# We use this as a fallback and for initial setup
mock_sprints = ['Sprint 2024.10', 'Sprint 2024.11', 'Sprint 2024.12']
mock_project_groups = ['All Groups', 'Core Platform', 'Growth Initiatives', 'Internal Tools']
mock_teams = ['All Teams', 'DATA', 'DEVELOP', 'ANALYTIC', 'IT']

mock_projects = [
    {'id': 1, 'name': 'Phoenix Project', 'group': 'Core Platform'},
    {'id': 2, 'name': 'Project Chimera', 'group': 'Growth Initiatives'},
    {'id': 3, 'name': 'Odyssey Initiative', 'group': 'Core Platform'},
    {'id': 4, 'name': 'Quantum Leap', 'group': 'Internal Tools'},
]

mock_team_members = [
    {'id': 'alice', 'name': 'Alice', 'team': 'DATA', 'subteam': 'Data Engineer', 'expectedDays': 18},
    {'id': 'bob', 'name': 'Bob', 'team': 'DATA', 'subteam': 'BI', 'expectedDays': 20},
    {'id': 'charlie', 'name': 'Charlie', 'team': 'DEVELOP', 'subteam': 'Backend', 'expectedDays': 20},
    {'id': 'diana', 'name': 'Diana', 'team': 'DEVELOP', 'subteam': 'Frontend', 'expectedDays': 15},
    {'id': 'grace', 'name': 'Grace', 'team': 'DEVELOP', 'subteam': 'Mobile', 'expectedDays': 17},
    {'id': 'ethan', 'name': 'Ethan', 'team': 'IT', 'subteam': 'Cloud', 'expectedDays': 22},
    {'id': 'frank', 'name': 'Frank', 'team': 'ANALYTIC', 'subteam': 'Analyst', 'expectedDays': 19},
]

mock_assignments = []
mock_project_cases = []


def prepopulate_mock_data():
    global mock_assignments, mock_project_cases
    mock_assignments = []
    mock_project_cases = []

    for sprint in mock_sprints:
        for project in mock_projects:
            for member in mock_team_members:
                mock_assignments.append(
                    {'sprint': sprint, 'projectId': project['id'], 'memberId': member['id'], 'days': 0})

            if project['id'] == 1:  # Phoenix Project
                mock_project_cases.extend([
                    {'sprint': sprint, 'projectId': 1, 'subteam': 'Data Engineer', 'days': 5},
                    {'sprint': sprint, 'projectId': 1, 'subteam': 'BI', 'days': 5},
                    {'sprint': sprint, 'projectId': 1, 'subteam': 'Backend', 'days': 15},
                    {'sprint': sprint, 'projectId': 1, 'subteam': 'Frontend', 'days': 10},
                    {'sprint': sprint, 'projectId': 1, 'subteam': 'Cloud', 'days': 5},
                ])
            if project['id'] == 2:  # Project Chimera
                mock_project_cases.extend([
                    {'sprint': sprint, 'projectId': 2, 'subteam': 'Data Engineer', 'days': 10},
                    {'sprint': sprint, 'projectId': 2, 'subteam': 'BI', 'days': 5},
                    {'sprint': sprint, 'projectId': 2, 'subteam': 'Backend', 'days': 20},
                ])


prepopulate_mock_data()
print(f"Mock data prepopulated: {len(mock_assignments)} assignments, {len(mock_project_cases)} project cases.")


# --- API Endpoints ---

@app.route("/api/sprints", methods=['GET'])
def get_sprints():
    # TODO: Replace this mock data with your BigQuery query
    #
    # try:
    #     if not bigquery_client:
    #         raise Exception("BigQuery client not initialized")
    #
    #     query = """
    #         SELECT DISTINCT sprint_name
    #         FROM `your-project.your-dataset.your_sprints_table`
    #         ORDER BY sprint_name DESC
    #     """
    #     query_job = bigquery_client.query(query)
    #     results = query_job.result()
    #     sprints = [row.sprint_name for row in results]
    #     return jsonify(sprints)
    #
    # except Exception as e:
    #     print(f"Error in /api/sprints: {e}")
    #     # Fallback to mock data on error
    #     return jsonify(mock_sprints)

    print("Serving mock data for /api/sprints")
    return jsonify(mock_sprints)


@app.route("/api/projects-and-groups", methods=['GET'])
def get_projects_and_groups():
    # TODO: Replace with your BigQuery query to fetch projects and groups
    # You might need two queries or one complex one with a UNION

    print("Serving mock data for /api/projects-and-groups")
    return jsonify({
        'projects': mock_projects,
        'projectGroups': mock_project_groups
    })


@app.route("/api/team-data", methods=['GET'])
def get_team_data():
    # TODO: Replace with your BigQuery query to fetch team members and teams

    print("Serving mock data for /api/team-data")
    return jsonify({
        'teamMembers': mock_team_members,
        'teams': mock_teams,
    })


@app.route("/api/sprint-data", methods=['GET'])
def get_sprint_data():
    sprints_str = request.args.get('sprints', '')
    if not sprints_str:
        return jsonify({"error": "No sprints provided"}), 400

    sprints_list = sprints_str.split(',')

    # TODO: Replace with your BigQuery query
    # Use the `sprints_list` to filter your results in the WHERE clause
    # e.g., WHERE sprint_name IN UNNEST(@sprints)
    # You'll need to use BigQuery parameters to pass the list safely.

    print(f"Serving mock data for /api/sprint-data for sprints: {sprints_list}")
    assignments = [a for a in mock_assignments if a['sprint'] in sprints_list]
    project_cases = [pc for pc in mock_project_cases if pc['sprint'] in sprints_list]

    return jsonify({
        'assignments': assignments,
        'projectCases': project_cases
    })


@app.route("/api/assignment", methods=['POST'])
def update_assignment():
    assignment = request.json

    # TODO: Replace with your BigQuery UPDATE or MERGE statement
    # Use the `assignment` dictionary to get values for your query

    print(f"Updating mock assignment: {assignment}")
    index_to_update = -1
    for i, a in enumerate(mock_assignments):
        if (a['sprint'] == assignment['sprint'] and
                a['projectId'] == assignment['projectId'] and
                a['memberId'] == assignment['memberId']):
            index_to_update = i
            break

    if index_to_update > -1:
        mock_assignments[index_to_update] = assignment
    else:
        mock_assignments.append(assignment)

    return jsonify(assignment)


@app.route("/api/project-case", methods=['POST'])
def update_project_case():
    project_case = request.json

    # TODO: Replace with your BigQuery UPDATE or MERGE statement
    # Use the `project_case` dictionary to get values

    print(f"Updating mock project case: {project_case}")
    index_to_update = -1
    for i, pc in enumerate(mock_project_cases):
        if (pc['sprint'] == project_case['sprint'] and
                pc['projectId'] == project_case['projectId'] and
                pc['subteam'] == project_case['subteam']):
            index_to_update = i
            break

    if index_to_update > -1:
        mock_project_cases[index_to_update] = project_case
    else:
        mock_project_cases.append(project_case)

    return jsonify(project_case)


@app.route("/", methods=['GET'])
def index() -> Response:
    """
    Un simple endpoint de bienvenida.
    ---
    responses:
      200:
        description: Respuesta exitosa
        examples:
          application/json: { "message": "Welcome message example" }
    """
    return jsonify({"message": "Welcome message example"})


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

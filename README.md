# Python AppEngine service basic template

A basic web service with Flask and GCP App Engine project format, with unit testing and a bitbucket pipeline with sonar
support

## Getting Started

Use this project as a template for new GCP python projects

### Installing

#1. Clone project:

GIT: git clone git@bitbucket.org:luce_data/luce-python-cloud-template.git

PyCharm: VCS > checkout from version control > git

#2. Create your new project in repo

Using Bitbucket (https://bitbucket.org/dashboard/overview) user interface.

#3. Change remote to that project

GIT: git remote add origin <server>

PyCharm: right click on project > git > repository > remotes > edit origin

#4. Modify settings

Sonar properties: projectKey, projectName, sources

Setup: name, description, author email, keywords

Requirements: add necessary libraries (with version)

README: update for your case

Create a pycharm environment

## Running the tests

Use one test file for each module. It should be named test_your_module_name. You can run them with either pytest
command (in project root) or with a configuration on Pycharm:

- Run > Edit Configurations...
- Set Target: Script path
- Path: path/to/project/<PROJECT_NAME>/tests
- Working directory: path/to/project/<PROJECT_NAME>
- Then, run the configuration

## Architecture diagram

Link to the architecture diagram of the application

## Environment variables

List of environment variables and how to populate it

- ***APP_ENV***: environment where the application is running, used to select the configuration file (config_<APP_ENV>
  .conf, if environment is prod -> config.yaml). Example values: dev, test, prod
- ***HOST***: host where the application is running
- ***PORT***: port where the application is running
- ***LOG_LEVEL***: level of the logs to display. Example values: DEBUG, INFO, WARNING, ERROR, CRITICAL
- ***LOG_TIMEZONE***: timezone to use in the logs. Example values: UTC, Europe/Madrid
- ***DEEP_LOG***: flag to activate deep logs. Example values: 0, 1

## Running the application

Explain how to configure and run the application

## Available services

List of the available services offers by the application and how to invoke them

- **/**
    - index: GET method to check if the service is running
    - params: none
    - response: Application name and welcome message

## Project structure

- basic_webapp
    - app_name
        - core
            - ...
        - example
            - module.py
        - utils
            - io.py
          - logger.py
          - machine_stats.py
            - requests.py
        - main.py
    - data
        - config.yaml
    - deployment
        - data
            - example_data.csv
        - schemas
            - example_schema.json
        - scripts
            - artifacts
                - deploy.sh
            - infra
                - infra.sh
    - tests
        - example
            - test_example_module.py
        - utils
            - test_utils_io.py
            - test_utils_requests.py
        - test_main.py
    - .VERSION
    - bitbucket-pipelines.yml
    - conftest.py
    - Dockerfile
    - main.py
    - README.md
    - requirements.txt
    - setup.py
    - sonar-project.properties

## Deploying the application

List of the command or reference to the scripts to deploy de application. Automated deployment from bitbucket-pipelines

## Versioning

We use https://sites.google.com/luceit.es/luceit/otros/devops/devops-politica_de_versionado

## Changelog

| Version | Date (last change) |   Developer   | Changes                                                                           |
|:-------:|:-------------------|:-------------:|:----------------------------------------------------------------------------------|
| v0.4.0  | 06/02/2025         | javier.perez  | Automated log and metric directory creation, add swagger endpoint                 |
| v0.4.0  | 04/02/2025         | javier.perez  | Add data encryption classes                                                       |
| v0.3.0  | 27/01/2025         | javier.perez  | Add monitoring and metric class to control                                        |
| v0.2.1  | 10/01/2025         | javier.perez  | Add machine stats option to logs                                                  |
| v0.2.0  | 07/01/2025         | javier.perez  | Add logger class and update libraries version                                     |
| v0.1.1  | 28/08/2024         | javier.perez  | Add repository clone to client and update libraries version to Python 3.12        |
| v0.1.0  | 08/11/2023         | javier.perez  | Add email step on bitbucket pipelines and update libraries                        |
| v0.0.3  | 31/10/2023         | javier.perez  | Add new Readme block (project structure) and update libraries                     |
| v0.0.2  | 01/02/2023         | javier.perez  | Update libraries versions to Python 3.10                                          |
| v0.0.1  | 01/06/2022         | javier.perez  | Complete template version to deploy different python applications on Google Cloud |
| v0.0.0  | 01/01/2022         | teresa.paramo | Template version to deploy a flask service on App Engine (GCP)                    |

## Authors

* **Javier Pérez** - javier.perez@luceit.es

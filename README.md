# Python AppEngine service basic template

A basic web service with Flask and GCP App Engine project format, with unit testing and a Jenkinsfile with sonar support

## Getting Started

Use this project as a template for new GCP App Engine python projects

### Installing

#1. Clone project:

GIT: git clone https://git.luceit.es/big-data-templates/_git/gcp_webapp

PyCharm: VCS > checkout from version control > git

#2. Create your new project in repo

Using TFS user interface.

#3. Change remote to that project

GIT: git remote add origin <server>

PyCharm: right click on project > git > repository > remotes > edit origin

#4. Modify settings

Sonar properties: projectKey, projectName, sources

Setup: name, description, author email, keywords

Requirements: add necessary libraries (with version)

README: update for your case

Create a pycharm environment

Create project on https://jenkins-ci.luceit.es:1443/

## Running the tests

Use one test file for each module. It should be named test_your_module_name.
You can run them with either pytest command (in project root) or IDE Run >  py.test in tests

## Versioning

We use https://sites.google.com/luceit.es/luceit/otros/devops/devops-politica_de_versionado

## Authors

* **Teresa Paramo** - teresa.paramo@luceit.es


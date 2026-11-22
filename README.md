# BITS Pilani Student Fitness API

This project implements a Flask-based fitness and wellness API for a BITS Pilani student context, along with CI/CD automation using GitHub Actions and a Jenkins pipeline example.

## Project overview

The application exposes a minimal API that supports:
- checking the status of the service
- listing available fitness programs
- calculating estimated daily calories for a client
- generating a client summary for a chosen training plan

## Local setup

1. Clone or open the project folder.
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   . .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask app:
   ```bash
   python app.py
   ```
5. Check the API health endpoint at:
   ```text
   http://localhost:5000/
   ```

## Manual testing

Run the test suite with:

```bash
pytest -q
```

## Docker

Build the Docker image:

```bash
docker build -t aceest-app .
```

Run the Docker container:

```bash
docker run -p 5000:5000 aceest-app
```

## GitHub Actions workflow

The GitHub Actions pipeline defined in `.github/workflows/main.yml` runs on every push and pull request. It performs the following steps:
- checks out the repository
- installs Python dependencies
- validates syntax using `compileall`
- runs the Pytest suite
- builds the Docker image

## Jenkins integration

The `Jenkinsfile` demonstrates how the build can be automated in Jenkins with the following stages:
- checkout source code
- install dependencies
- run tests
- analyze the Python application with SonarQube and enforce the quality gate
- build Docker image

Before running this pipeline, configure the Jenkins SonarQube Scanner plugin with:
- an authenticated SonarQube server named `SonarQube`
- a scanner installation named `SonarScanner`
- a SonarQube webhook pointing to `https://<jenkins-url>/sonarqube-webhook/`

The project key and scan scope are defined in `sonar-project.properties`. The pipeline waits up to one hour for the SonarQube quality gate and stops before building the Docker image if the gate fails.

## Key endpoints

- `GET /` - service health check
- `GET /programs` - available programs
- `POST /calculate-calories` - calculate calories
- `POST /client-summary` - generate a client summary

Example payload for calorie calculation:

```json
{
  "program": "Fat Loss",
  "weight_kg": 70
}
```

Example response:

```json
{
  "program": "Fat Loss",
  "weight_kg": 70,
  "calories_per_day": 1540
}
```

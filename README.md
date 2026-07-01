# taskflow-app

In-memory task list REST API. Reference app for the DevOps pipeline demo at **AWS Summit São Paulo 2026** - *"Do Localhost à Nuvem: DevOps para Quem Está Começando"*.

> Infrastructure: [taskflow-infra](https://github.com/jhermesn/taskflow-infra)

## Endpoints

| Method | Path | Status |
|--------|------|--------|
| GET | `/health` | 200 |
| GET | `/tasks` | 200 |
| POST | `/tasks` | 201 |
| GET | `/tasks/{id}` | 200 / 404 |
| PATCH | `/tasks/{id}` | 200 / 404 |
| DELETE | `/tasks/{id}` | 204 / 404 |

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# http://localhost:8000/docs
```

## Test

```bash
pytest -q
```

## CI

Runs on push to feature branches and PRs to `dev`/`main`.

| Job | Tool | Output |
|-----|------|--------|
| Test & Coverage | pytest-cov | Step summary |
| Security Scan | Trivy | Security tab |
| SAST | SonarCloud | SonarCloud dashboard |

**Repository secrets/variables** (Settings → Secrets & Variables → Actions):

| Name | Type |
|------|------|
| `SONAR_TOKEN` | Secret |
| `SONAR_PROJECT_KEY` | Variable |
| `SONAR_ORGANIZATION` | Variable |

## Deploy

**Per environment** (Settings → Environments → `dev` / `prod`):

| Name | Type |
|------|------|
| `APP_DEPLOY_ROLE_ARN` | Secret |
| `ECR_REPOSITORY_URL` | Secret |
| `ECS_CLUSTER_NAME` | Secret |
| `ECS_SERVICE_NAME` | Secret |
| `AWS_REGION` | Variable |
| `ECS_TASK_DEFINITION` | Variable |
| `ECS_CONTAINER_NAME` | Variable |

> Values come from `taskflow-infra` bootstrap and provision outputs.

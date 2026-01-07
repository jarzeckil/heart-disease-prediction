# Heart Failure Prediction Pipeline 🫀
[![CI Pipeline](https://github.com/jarzeckil/heart-failure-prediction/actions/workflows/ci.yaml/badge.svg)](https://github.com/jarzeckil/heart-failure-prediction/actions/workflows/ci.yaml)
[![Docker Pulls](https://img.shields.io/docker/pulls/jarzeckil/heart-failure-api)](https://hub.docker.com/r/jarzeckil/heart-failure-api)

[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
![Python](https://img.shields.io/badge/python-3.1x-blue)
![Sklearn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![pytest](https://img.shields.io/badge/py-test-blue?logo=pytest)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
[![DVC](https://img.shields.io/badge/DVC-Enabled-945DD6?logo=dvc&logoColor=white)](https://dvc.org/)


End-to-end Machine Learning pipeline for predicting heart failure risk using standard MLOps practices.

## 🖥️ Live Demo
Experience the model in action using the React-based frontend:
**[https://heart-disease-predictor-0rv0.onrender.com](https://heart-disease-predictor-0rv0.onrender.com)**

Interact with the UI to input clinical data and get real-time predictions.

## ⭐ Key Features

*   **Multi-Stage Docker Build**: Utilizes a Dockerfile that builds the React frontend (Node.js) and Python backend in separate stages, resulting in a lightweight, production-ready final image.
*   **Model Explainability**: Serves SHAP values alongside predictions, offering transparency into the model.
*   **Reproducibility & Versioning**: Complete versioning of Data (DVC + DAGsHub) and Models (MLflow). Configuration is managed via Hydra for easy experiment tracking.

## 🛠 Tech Stack
* **Dependency Management:** Poetry
* **Data Versioning:** DVC (Data Version Control) + DAGsHub
* **Experiment Tracking:** MLflow
* **Modeling:** Scikit-learn (Pipelines), XGBoost, Hydra, Optuna
* **API:** FastAPI
* **Container Registry:** Docker Hub
* **CI/CD:** GitHub Actions (Linting, Testing, Build & Push)
* **Deployment:** Render

## 🚀 How to Run

### Option 1: Production (Docker Hub)
Pull and run the pre-built image containing both the API and Frontend.

```bash
docker run -p 8000:8000 jarzeckil/heart-failure-api:latest
```
*   **UI Reference**: Visit `http://localhost:8000`
*   **API Documentation**: Visit `http://localhost:8000/docs`

### Option 2: Build Locally (Development)
If you want to build the image from source:

```bash
git clone https://github.com/jarzeckil/heart-failure-prediction.git
cd heart-failure-prediction
docker compose up
```

## 🏗 CI/CD & Architecture

The pipeline automates the journey from code commit to production deployment.

```mermaid graph LR
    A[Code Push] -->|Triggers| B(GitHub Actions)
    B -->|Run Tests| C{Tests Pass?}
    C -- Yes --> D[DVC Pull]
    D -->|Fetch Artifacts| E[DAGsHub]
    C -- No --> F[Fail Build]
    D --> G[Multi-Stage Docker Build]
    G -->|Stage 1| H[Node.js Build]
    G -->|Stage 2| I[Python Runtime]
    H --> I
    I --> J[Push to Docker Hub]
    J --> K[Auto-Deploy to Render]
```

## 📂 Project Structure

```
├── .github/          # CI/CD workflows (GitHub Actions)
├── conf/             # Hydra configurations
├── data/             # Data directory (tracked by DVC)
├── frontend/         # React application source code
├── mlruns/           # MLflow experiment tracking
├── models/           # Binary model artifacts
├── notebooks/        # Jupyter notebooks for EDA
├── src/              # Application source code
│   └── heart_failure_prediction/
└── tests/            # Pytest suite
```

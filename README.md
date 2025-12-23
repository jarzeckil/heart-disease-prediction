# Heart Failure Prediction Pipeline 🫀
[![CI Pipeline](https://github.com/jarzeckil/heart-failure-prediction/actions/workflows/ci.yaml/badge.svg)](https://github.com/jarzeckil/heart-failure-prediction/actions/workflows/ci.yaml)

[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
![Python](https://img.shields.io/badge/python-3.1x-blue)
![Sklearn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![pytest](https://img.shields.io/badge/py-test-blue?logo=pytest)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)

End-to-end Machine Learning pipeline for predicting heart failure risk using standard MLOps practices.

## 🎯 Project Goal
The goal is to classify patients with a high risk of heart failure based on clinical data. The project emphasizes MLOps best practices: reproducibility, modularity, and automated testing.

## 🛠 Tech Stack
* **Dependency Management:** Poetry
* **Data Versioning:** DVC (Data Version Control)
* **Experiment Tracking:** MLflow
* **Modeling:** Scikit-learn (Pipelines), XGBoost
* **API:** FastAPI + Docker
* **CI/CD:** GitHub Actions (Linting, Testing)
* **Configuration:** Hydra

## 🚀 How to Run

```bash
git clone [https://github.com/jarzeckil/heart-failure-prediction.git](https://github.com/jarzeckil/heart-failure-prediction.git)
cd heart-failure-prediction
docker compose up
```

## 📂 Project Structure
```
├── .github/       # CI/CD workflows
├── data/          # Data (tracked by DVC, ignored by Git)
├── models/        # Trained models registry
├── notebooks/     # EDA and prototyping
├── src/           # Source code
│   └── heart_failure_prediction/
├── tests/         # Pytest tests
├── Makefile       # Command shortcuts
└── pyproject.toml # Dependencies config
```

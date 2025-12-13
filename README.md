# Heart Failure Prediction Pipeline 🫀

![Python](https://img.shields.io/badge/python-3.11-blue)
![Poetry](https://img.shields.io/badge/poetry-1.8-blue)
![CI](https://github.com/TWOJA_NAZWA_UZYTKOWNIKA/heart-failure-prediction/actions/workflows/ci.yaml/badge.svg)

End-to-end Machine Learning pipeline for predicting heart failure risk using standard MLOps practices.

## 🎯 Project Goal
The goal is to classify patients with a high risk of heart failure based on clinical data. The project emphasizes MLOps best practices: reproducibility, modularity, and automated testing.

## 🛠 Tech Stack
* **Dependency Management:** Poetry
* **Data Versioning:** DVC (Data Version Control)
* **Experiment Tracking:** MLflow
* **Modeling:** Scikit-learn (Pipelines)
* **API:** FastAPI + Docker
* **CI/CD:** GitHub Actions (Linting, Testing)
* **Configuration:** Hydra

## 🚀 How to Run

### Clone & Setup
```bash
git clone [https://github.com/jarzeckil/heart-failure-prediction.git](https://github.com/jarzeckil/heart-failure-prediction.git)
cd heart-failure-prediction
make init
make install
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

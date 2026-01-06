from pathlib import Path

import joblib
import mlflow
from mlflow.tracking import MlflowClient

MODEL_NAME = 'HeartFailurePredictor'
DEST_DIR = Path('models')

client = MlflowClient()

latest_versions = client.get_latest_versions(MODEL_NAME)
if not latest_versions:
    raise Exception(f'No registered model found for name: {MODEL_NAME}')

latest_version_info = sorted(latest_versions, key=lambda x: x.version, reverse=True)[0]
run_id = latest_version_info.run_id

print(
    f'Exporting artifacts from Run ID: {run_id} '
    f'(Model Version: {latest_version_info.version})'
)

model = mlflow.pyfunc.load_model(
    f'models:/{MODEL_NAME}/{latest_version_info.version}'
).get_raw_model()
joblib.dump(model, DEST_DIR / 'model.joblib')
print(f'Model saved to {DEST_DIR / "model.joblib"}')

artifact_path = 'explainer_artifact'

local_path = mlflow.artifacts.download_artifacts(
    run_id=run_id, artifact_path=artifact_path, dst_path=str(DEST_DIR)
)

print('Export complete.')

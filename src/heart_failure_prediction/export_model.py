import joblib
import mlflow

model = mlflow.pyfunc.load_model(
    model_uri='models:/heart_failure_prediction/latest'
).get_raw_model()

joblib.dump(model, 'models/model.joblib')

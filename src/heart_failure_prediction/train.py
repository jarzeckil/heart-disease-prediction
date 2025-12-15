import json
import logging
import os

import hydra
from hydra.core.hydra_config import HydraConfig
import joblib
from omegaconf import DictConfig
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from heart_failure_prediction.config import PROJECT_ROOT
from heart_failure_prediction.preprocessing import ZeroImputer

logger = logging.getLogger(__name__)


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def build_pipeline(cfg: DictConfig) -> Pipeline:
    zero_imputer_columns = list(cfg.processing.missing_vals_cols)
    num_columns = list(cfg.processing.num_features)
    cat_columns = list(cfg.processing.cat_features)

    full_pipeline = Pipeline(
        [
            (
                'preprocessing',
                ColumnTransformer(
                    [
                        (
                            'num_pipeline',
                            Pipeline(
                                [
                                    ('zero_imputer', ZeroImputer(zero_imputer_columns)),
                                    (
                                        'median_imputer',
                                        SimpleImputer(
                                            strategy='median', add_indicator=True
                                        ),
                                    ),
                                    ('scaler', StandardScaler()),
                                ]
                            ),
                            num_columns,
                        ),
                        (
                            'cat_pipeline',
                            Pipeline(
                                [
                                    (
                                        'most_frequent_imputer',
                                        SimpleImputer(strategy='most_frequent'),
                                    ),
                                    (
                                        'one_hot_encoder',
                                        OneHotEncoder(
                                            handle_unknown='ignore', drop='first'
                                        ),
                                    ),
                                ]
                            ),
                            cat_columns,
                        ),
                    ]
                ),
            ),
            ('model', LogisticRegression()),
        ]
    )

    return full_pipeline


def evaluate(model: Pipeline, X_test, y_test) -> dict:
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    logger.info(
        f'Evaluation metrics: '
        f'accuracy = {accuracy} '
        f'recall = {recall} '
        f'precision = {precision} '
        f'f1 = {f1}'
    )

    scores = {
        'accuracy': float(accuracy),
        'recall': float(recall),
        'precision': float(precision),
        'f1_score': float(f1),
    }

    return scores


def split_data(cfg: DictConfig, df: pd.DataFrame) -> tuple:
    target = cfg.modeling.target
    test_size = cfg.modeling.test_size
    random_state = cfg.modeling.random_state

    y = df[target]
    X = df.drop(target, axis=1)

    return train_test_split(X, y, test_size=test_size, random_state=random_state)


@hydra.main(
    config_path=os.path.join(PROJECT_ROOT, 'conf'),
    config_name='config',
    version_base='1.2',
)
def main(cfg: DictConfig) -> None:
    logger.info('----------Reading data----------')
    data = load_data(path=cfg.raw_data.path)

    X_train, X_test, y_train, y_test = split_data(cfg, data)
    model = build_pipeline(cfg)

    logger.info('----------Training model----------')
    model.fit(X_train, y_train)

    logger.info('----------Evaluating model----------')
    scores = evaluate(model, X_test, y_test)

    output_path = HydraConfig.get().runtime.output_dir

    model_file_path = os.path.join(output_path, 'model.pkl')
    joblib.dump(model, model_file_path)
    logger.info(f'Model saved to: {model_file_path}')

    scores_file_path = os.path.join(output_path, 'metrics.json')
    with open(scores_file_path, 'w') as f:
        json.dump(scores, f, indent=4)
    logger.info(f'Scores saved to: {scores_file_path}')


if __name__ == '__main__':
    main()

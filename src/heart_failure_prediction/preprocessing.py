import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class ZeroImputer(BaseEstimator, TransformerMixin):
    def __init__(self, columns: list):
        self.columns = columns

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame):
        X_copy = X.copy()

        missing_cols = [col for col in self.columns if col not in X_copy.columns]
        if missing_cols:
            raise ValueError(f'Columns not found in dataset: {missing_cols}')

        for col in self.columns:
            X_copy[col] = X_copy[col].replace({0: np.nan})

        return X_copy

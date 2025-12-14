import numpy as np
import pandas as pd
import pytest

from heart_failure_prediction.preprocessing import ZeroImputer


def test_transforms_correctly():
    # GIVEN
    imputer = ZeroImputer(['A'])
    df = pd.DataFrame.from_dict({'A': [0, 0, 0]})

    # WHEN
    df_nan = imputer.transform(df)

    # THEN
    assert df_nan['A'].isna().all()


def test_leaves_other_columns_intact():
    # GIVEN
    imputer = ZeroImputer(['A'])
    df = pd.DataFrame.from_dict({'A': [0, 0, 0], 'B': [0, 0, 0]})

    # WHEN
    df_nan = imputer.transform(df)

    # THEN
    assert df_nan['A'].isna().all()
    assert np.all(df['B'] == df_nan['B'])


def test_raises_error_columns_dont_exist():
    # GIVEN
    imputer = ZeroImputer(['B'])
    df = pd.DataFrame.from_dict({'A': [0, 0, 0]})

    # WHEN + THEN
    with pytest.raises(ValueError):
        imputer.transform(df)

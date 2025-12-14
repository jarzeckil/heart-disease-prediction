import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_distributions(df, n_cols: int = 4, bins: int = 50):
    cols = df.columns

    n_rows = int(np.ceil(len(cols) / n_cols))

    plt.figure(figsize=(3 * n_cols, 2 * n_rows))

    for i, col in enumerate(cols, start=1):
        plt.subplot(n_rows, n_cols, i)
        if df[col].dtypes == 'object':
            df[col].hist(bins=bins)
            plt.title(col)
        else:
            sns.histplot(data=df, x=col, kde=True, bins=bins)
            plt.title(f'{col} | Skewness: {round(df[col].skew(), 2)}')
        plt.tight_layout()


def plot_categorical_countplots(df, target: str, n_cols: int = 3):
    cat_cols = df.select_dtypes(include=['object']).columns
    cat_cols = [c for c in cat_cols if c != target]

    if len(cat_cols) == 0:
        return

    n_rows = int(np.ceil(len(cat_cols) / n_cols))
    plt.figure(figsize=(4 * n_cols, 3 * n_rows))

    for i, col in enumerate(cat_cols, start=1):
        plt.subplot(n_rows, n_cols, i)
        sns.countplot(data=df, x=col, hue=target)
        plt.title(f'{col} vs {target}')
        plt.xticks(rotation=45)
        plt.tight_layout()

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import config


def get_pipelines():
    # Pipeline 1: Tylko imputacja brakujących wartości
    pipe_base = Pipeline([("imputer", SimpleImputer(strategy="median"))])

    # Pipeline 2: Imputacja i standaryzacja
    pipe_std = Pipeline(
        [("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )

    # Pipeline 3: Imputacja, standaryzacja i PCA
    pipe_pca = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("pca", PCA(n_components=config.PCA_VARIANCE_THRESHOLD)),
        ]
    )

    return {
        "Brak przetwarzania": pipe_base,
        "Standaryzacja": pipe_std,
        f"PCA ({int(config.PCA_VARIANCE_THRESHOLD * 100)}% wariancji)": pipe_pca,
    }

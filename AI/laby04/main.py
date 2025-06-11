import os
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

import config
import data_loader
import data_explorer
import pipelines
import model_evaluation
import bonus_analysis


def main():
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    X, y, df = data_loader.load_data(config.DATA_FILEPATH)
    if df is None:
        return

    data_explorer.run_exploration(df, config.OUTPUT_DIR)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE, stratify=y
    )
    print("\n--- 2. PRZYGOTOWANIE DANYCH ---")
    print(
        f"Podzielono dane na zbiór uczący ({len(X_train)} wierszy) i testowy ({len(X_test)} wierszy)."
    )

    processing_pipelines = pipelines.get_pipelines()

    classifiers = {
        "Naiwny Bayes": GaussianNB(),
        "Drzewo Decyzyjne (domyślne)": DecisionTreeClassifier(
            random_state=config.RANDOM_STATE
        ),
        "Drzewo Decyzyjne (max_depth=5)": DecisionTreeClassifier(
            max_depth=5, random_state=config.RANDOM_STATE
        ),
        "Drzewo Decyzyjne (min_samples_leaf=5)": DecisionTreeClassifier(
            min_samples_leaf=5, random_state=config.RANDOM_STATE
        ),
        "Las Losowy (Bonus)": RandomForestClassifier(random_state=config.RANDOM_STATE),
        "SVM (Bonus)": SVC(random_state=config.RANDOM_STATE),
    }

    model_evaluation.run_cross_validation(
        processing_pipelines,
        classifiers,
        X_train,
        y_train,
        config.CV_FOLDS,
        config.RANDOM_STATE,
    )

    # Na podstawie wyników CV, Las Losowy z podstawowym przetwarzaniem jest najlepszy.
    best_final_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("classifier", RandomForestClassifier(random_state=config.RANDOM_STATE)),
        ]
    )

    model_evaluation.evaluate_best_model(
        best_final_pipeline, X_train, y_train, X_test, y_test, config.OUTPUT_DIR
    )

    bonus_analysis.run_pruning_analysis(X_train, y_train, X_test, y_test, config)

    print("\n--- Zakończono analizę. ---")


if __name__ == "__main__":
    main()

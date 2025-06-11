import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, ConfusionMatrixDisplay


def run_cross_validation(
    pipelines, classifiers, X_train, y_train, cv_folds, random_state
):
    print("\n--- 3. KLASYFIKACJA I OCENA (WALIDACJA KRZYŻOWA) ---")
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
    results = []

    for pipe_name, pipe in pipelines.items():
        for clf_name, clf in classifiers.items():
            full_pipeline = Pipeline(steps=pipe.steps + [("classifier", clf)])

            # Użycie n_jobs=-1 do przyspieszenia obliczeń
            scores = cross_val_score(
                full_pipeline, X_train, y_train, cv=cv, scoring="f1_weighted", n_jobs=-1
            )

            results.append(
                {
                    "Przetwarzanie": pipe_name,
                    "Klasyfikator": clf_name,
                    "Średni F1-score (CV)": scores.mean(),
                    "Odch. std. F1-score (CV)": scores.std(),
                }
            )
            print(f"Oceniono: {pipe_name} -> {clf_name}")

    results_df = pd.DataFrame(results).sort_values(
        by="Średni F1-score (CV)", ascending=False
    )
    print("\n--- Wyniki 5-krotnej walidacji krzyżowej na zbiorze uczącym ---")
    print(results_df.to_string())

    return results_df


def evaluate_best_model(pipeline, X_train, y_train, X_test, y_test, output_dir):
    """
    Trenuje finalny model i ocenia go na zbiorze testowym.
    """
    print("\n--- 4. OCENA NAJLEPSZEGO MODELU NA ZBIORZE TESTOWYM ---")

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    print("\n[INFO] Raport klasyfikacji:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Macierz pomyłek
    fig, ax = plt.subplots(figsize=(12, 12))
    sns.set_context("talk")
    ConfusionMatrixDisplay.from_predictions(
        y_test, y_pred, ax=ax, cmap="viridis", values_format="d"
    )
    plt.title("Macierz pomyłek dla najlepszego modelu")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "best_model_confusion_matrix.png"))
    plt.close()
    print(
        f"[OK] Zapisano macierz pomyłek w '{output_dir}best_model_confusion_matrix.png'"
    )

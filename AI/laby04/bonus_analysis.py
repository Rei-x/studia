from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import classification_report


def run_pruning_analysis(X_train, y_train, X_test, y_test, config):
    print("\n--- 5. ANALIZA BONUSOWA: ŁAGODZENIE PRZEUCZENIA (PRZYCINANIE DRZEWA) ---")

    pruning_pipeline = Pipeline(
        [("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )

    X_train_processed = pruning_pipeline.fit_transform(X_train)
    X_test_processed = pruning_pipeline.transform(X_test)

    dt = DecisionTreeClassifier(random_state=config.RANDOM_STATE)
    path = dt.cost_complexity_pruning_path(X_train_processed, y_train)
    ccp_alphas = path.ccp_alphas
    ccp_alphas = ccp_alphas[:-1]  # Usunięcie trywialnej alfy maksymalnej

    cv = StratifiedKFold(
        n_splits=config.CV_FOLDS, shuffle=True, random_state=config.RANDOM_STATE
    )
    param_grid = {"ccp_alpha": ccp_alphas}

    print("[INFO] Szukanie optymalnej wartości ccp_alpha...")
    grid_search = GridSearchCV(
        DecisionTreeClassifier(random_state=config.RANDOM_STATE),
        param_grid,
        cv=cv,
        scoring="f1_weighted",
        n_jobs=-1,
    )
    grid_search.fit(X_train_processed, y_train)

    best_alpha = grid_search.best_params_["ccp_alpha"]
    print(f"[OK] Najlepsza znaleziona wartość ccp_alpha: {best_alpha:.6f}")

    # Krok 4: Porównanie modeli
    dt_default = DecisionTreeClassifier(random_state=config.RANDOM_STATE)
    dt_default.fit(X_train_processed, y_train)
    y_pred_default = dt_default.predict(X_test_processed)

    dt_pruned = DecisionTreeClassifier(
        random_state=config.RANDOM_STATE, ccp_alpha=best_alpha
    )
    dt_pruned.fit(X_train_processed, y_train)
    y_pred_pruned = dt_pruned.predict(X_test_processed)

    print("\n--- Porównanie wyników Drzewa Decyzyjnego na zbiorze testowym ---")
    print("\nModel Domyślny (nieprzycięty):")
    print(classification_report(y_test, y_pred_default, zero_division=0))

    print("\nModel Przycięty (ccp_alpha):")
    print(classification_report(y_test, y_pred_pruned, zero_division=0))

    print("\n--- Porównanie złożoności drzew ---")
    print(f"Liczba liści (drzewo domyślne): {dt_default.get_n_leaves()}")
    print(f"Głębokość (drzewo domyślne):    {dt_default.get_depth()}")
    print(f"Liczba liści (drzewo przycięte): {dt_pruned.get_n_leaves()}")
    print(f"Głębokość (drzewo przycięte):    {dt_pruned.get_depth()}")

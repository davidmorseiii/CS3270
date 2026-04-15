import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from .logger_config import setup_logger

logger = setup_logger(__name__)

# module level cache mirrors weather_data pattern in app.py
_model_cache = None

FEATURE_COLUMNS = [
    'MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine',
    'WindGustSpeed', 'WindSpeed9am', 'WindSpeed3pm',
    'Humidity9am', 'Humidity3pm',
    'Pressure9am', 'Pressure3pm',
    'Cloud9am', 'Cloud3pm',
    'Temp9am', 'Temp3pm',
    'RainToday_bin',  # derived: "yes" -> 1, else -> 0
]


def _prepare_matrix(data):
    """Convert list of dicts weather data to numpy arrays for sklearn

    Returns:
        X: float array of shape (N, len(FEATURE_COLUMNS))
        y: int array of shape (N,) with 0=no rain, 1=rain tomorrow
    """
    X_rows = []
    y_rows = []

    for row in data:
        target = row.get('RainTomorrow')
        if target is None:
            continue
        y_rows.append(int(target))

        feature_row = []
        for col in FEATURE_COLUMNS:
            if col == 'RainToday_bin':
                feature_row.append(1.0 if row.get('RainToday') == 'Yes' else 0.0)
            else:
                val = row.get(col)
                feature_row.append(float(val) if val is not None else float('nan'))
        X_rows.append(feature_row)

    X = np.array(X_rows, dtype=float)
    y = np.array(y_rows, dtype=int)
    return X, y


def get_or_train_model(data):
    """Return trained cache, training on first call.

    Args:
        data: list of dicts returned by load_weather_data()

    Returns:
        dict with keys: pipeline, lr_pipeline, accuracy, lr_accuracy,
                        importances (list of (name, score) tuples), features
    """
    global _model_cache
    if _model_cache is not None:
        return _model_cache

    logger.info("Training rain prediction models on %d records...", len(data))
    X, y = _prepare_matrix(data)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    rf_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler()),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)),
    ])

    lr_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(max_iter=1000, random_state=42)),
    ])

    rf_pipeline.fit(X_train, y_train)
    lr_pipeline.fit(X_train, y_train)

    rf_accuracy = accuracy_score(y_test, rf_pipeline.predict(X_test))
    lr_accuracy = accuracy_score(y_test, lr_pipeline.predict(X_test))

    importances_raw = rf_pipeline.named_steps['clf'].feature_importances_
    importances = sorted(
        zip(FEATURE_COLUMNS, importances_raw),
        key=lambda t: t[1],
        reverse=True,
    )

    _model_cache = {
        'pipeline': rf_pipeline,
        'lr_pipeline': lr_pipeline,
        'accuracy': rf_accuracy,
        'lr_accuracy': lr_accuracy,
        'importances': importances,
        'features': FEATURE_COLUMNS,
    }

    logger.info(
        "Models trained. RF accuracy=%.4f, LR accuracy=%.4f",
        rf_accuracy, lr_accuracy,
    )
    return _model_cache


def predict_rain(model_cache, feature_values_dict):
    """Run inference on single set of weather observations

    Args:
        model_cache: dict returned by get_or_train_model()
        feature_values_dict: dict mapping feature names to flaot values or None

    Returns:
        dict with keys: label (int), probability_rain (float), probability_no_rain (float)
    """
    row = []
    for col in FEATURE_COLUMNS:
        val = feature_values_dict.get(col)
        row.append(float(val) if val is not None else float('nan'))

    X = np.array([row], dtype=float)
    pipeline = model_cache['pipeline']
    label = int(pipeline.predict(X)[0])
    proba = pipeline.predict_proba(X)[0]

    # predict_proba [P(class=0), P(class=1)]
    return {
        'label': label,
        'probability_rain': float(proba[1]),
        'probability_no_rain': float(proba[0]),
    }

import joblib
import xgboost as xgb
import importlib.resources


def load_data(filename):
    with importlib.resources.path('iimi.data', filename) as path:
        return joblib.load(path)


# Load nucleotide information
nucleotide_info = load_data('nucleotide_info.pkl')

# Load unreliable regions
unreliable_regions = load_data('unreliable_regions.pkl')

# Load trained models
trained_rf = load_data('trained_rf.pkl')

# Load trained XGBoost model
trained_xgb = xgb.Booster()
with importlib.resources.path('iimi.data', 'trained_xgb.model') as path:
    trained_xgb.load_model(path)

# Load trained ElasticNet model
trained_en = load_data('trained_en.pkl')

# Example plant diagnostics result
example_diag = load_data('example_diag.pkl')

# Coverage profiles of plant samples
example_cov = load_data('example_cov.pkl')

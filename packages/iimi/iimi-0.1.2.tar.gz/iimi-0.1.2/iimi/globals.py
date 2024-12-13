import joblib
import xgboost as xgb

# load nucleotide information
nucleotide_info_path = "../data/nucleotide_info.pkl"
nucleotide_info = joblib.load(nucleotide_info_path)

# load unreliable regions
unreliable_regions_path = "../data/unreliable_regions.pkl"
unreliable_regions = joblib.load(unreliable_regions_path)

# load trained models
trained_rf_path = "../data/trained_rf.pkl"
trained_rf = joblib.load(trained_rf_path)

trained_xgb_path = "../data/trained_xgb.model"
trained_xgb = xgb.Booster()
trained_xgb.load_model(trained_xgb_path)

trained_en_path = "../data/trained_en.pkl"
trained_en = joblib.load(trained_en_path)

# example plant diagnostics result
example_diag_path = "../data/example_diag.pkl"
example_diag = joblib.load(example_diag_path)

# coverage profiles of plant samples
example_cov_path = "../data/example_cov.pkl"
example_cov = joblib.load(example_cov_path)

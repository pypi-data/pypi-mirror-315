"""Analysis package for predicting gut microbiome alpha-diversity.

From blood metabolomics data.
"""

from gutmetrics.preprocessing.cleaning import (
    standardize_index,
    remove_outliers,
    validate_metabolomics_data,
    validate_microbiome_data,
    clean_metadata,
)
from gutmetrics.preprocessing.scaling import (
    scale_metabolomics,
    scale_proteomics,
    scale_clinical_labs,
    scale_and_combine_omics,
    get_scaled_feature_names,
)

__version__ = "0.1.3"

__all__ = [
    "standardize_index",
    "remove_outliers", 
    "validate_metabolomics_data",
    "validate_microbiome_data",
    "clean_metadata",
    "scale_metabolomics",
    "scale_proteomics", 
    "scale_clinical_labs",
    "scale_and_combine_omics",
    "get_scaled_feature_names",
]

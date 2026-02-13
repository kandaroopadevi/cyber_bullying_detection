"""
Cyberbullying Detection - src package

Exports handy functions for loading data, preprocessing, building features,
training, evaluating, and predicting.
"""

_version_ = "1.0.0"

from .data_utils import (
    load_json_dataset,
    simple_clean_text,
    lemmatize_text_spacy,
    preprocess_series,
)

from .features import (
    build_vectorizer,
    save_vectorizer,
    load_vectorizer,
)

# Optional convenience re-exports for training/eval helpers
# (prevents circular imports when used as scripts)
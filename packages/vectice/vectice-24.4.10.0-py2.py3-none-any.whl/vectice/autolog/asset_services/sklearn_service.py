from __future__ import annotations

from typing import Any

from vectice.autolog.asset_services.metric_service import MetricService
from vectice.autolog.asset_services.property_service import PropertyService
from vectice.autolog.asset_services.technique_service import TechniqueService
from vectice.autolog.model_library import ModelLibrary


def identify_estimator(asset: Any):
    """Temporary fix for sklearn 1.6.0 and xgboost sklearn integration."""
    is_model_regressor, is_model_classifier = False, False
    try:
        from sklearn.base import is_classifier, is_regressor

        # sklearn < 1.6.0
        is_model_regressor = is_regressor(asset)
        is_model_classifier = is_classifier(asset)
    except AttributeError:
        pass
    try:
        # sklearn 1.6.0, xgboost does not support this yet
        is_model_regressor = asset.__sklearn_tags__().estimator_type == "regressor"
        is_model_classifier = asset.__sklearn_tags__().estimator_type == "classifier"
    except Exception:
        pass

    try:
        # xgboost temp fallback. Current sklearn integration is behind
        is_model_regressor = asset._estimator_type == "regressor"
        is_model_classifier = asset._estimator_type == "classifier"
    except Exception:
        pass

    return is_model_regressor, is_model_classifier


class AutologSklearnService(MetricService, PropertyService, TechniqueService):
    def __init__(self, key: str, asset: Any, data: dict, custom_metrics_data: set[str | None]):
        self._asset = asset
        self._key = key

        super().__init__(cell_data=data, custom_metrics=custom_metrics_data)

    def get_asset(self):
        # xgboost relies on BaseEstimator
        # lightgbm has Booster and sklearn API which uses BaseEstimator
        try:
            from sklearn.pipeline import Pipeline

            is_regressor, is_classifier = identify_estimator(self._asset)

            if is_regressor or is_classifier or isinstance(self._asset, Pipeline):
                library = ModelLibrary.SKLEARN

                if isinstance(self._asset, Pipeline):
                    library = ModelLibrary.SKLEARN_PIPELINE
                elif str(self._asset.__class__.__module__) == "sklearn.model_selection._search":
                    library = ModelLibrary.SKLEARN_PIPELINE
                try:
                    # TODO fix regex picking up classes
                    # Ignore Initialized variables e.g LogisticRegression Class
                    self._asset.get_params()  # pyright: ignore[reportGeneralTypeIssues]
                    _, params = self._get_sklearn_or_xgboost_or_lgbm_info(self._asset)
                    return {
                        "variable": self._key,
                        "model": self._asset,
                        "library": library,
                        "metrics": self._get_model_metrics(self._cell_data),
                        "technique": self._get_model_technique(self._asset, library),
                        "properties": params,
                    }
                except Exception:
                    pass
        except ImportError:
            pass

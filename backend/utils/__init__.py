"""
Paquete de utilidades para el sistema de predicción de rendimiento académico.
Contiene módulos para preprocesamiento y predicción.
"""

from .preprocessing import preprocess_input, validate_input
from .predictor import predict_performance, identify_key_factors, get_recommendations

__all__ = [
    'preprocess_input',
    'validate_input',
    'predict_performance',
    'identify_key_factors',
    'get_recommendations'
]

__version__ = '1.0.0'
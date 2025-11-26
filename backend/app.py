from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import sys

# Agregar el directorio actual al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.preprocessing import preprocess_input
from utils.predictor import predict_performance

app = Flask(__name__)
CORS(app)

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'modelo_rl.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'model', 'scaler.pkl')

# Variables globales para el modelo
model = None
scaler = None

def load_model():
    """Carga el modelo y scaler al iniciar la aplicación"""
    global model, scaler
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        print("=" * 60)
        print("✅ Modelo y scaler cargados correctamente")
        print("=" * 60)
        return True
    except FileNotFoundError as e:
        print("=" * 60)
        print(f"❌ ERROR: Archivos del modelo no encontrados")
        print(f"   Asegúrate de colocar los archivos en:")
        print(f"   - {MODEL_PATH}")
        print(f"   - {SCALER_PATH}")
        print("=" * 60)
        return False
    except Exception as e:
        print("=" * 60)
        print(f"❌ ERROR al cargar modelo: {e}")
        print("=" * 60)
        return False

# Cargar modelo al iniciar
load_model()

@app.route('/', methods=['GET'])
def home():
    """Ruta principal de verificación"""
    return jsonify({
        'status': 'online',
        'mensaje': 'API de Predicción de Rendimiento Académico',
        'version': '1.0.0',
        'modelo': 'Regresión Logística',
        'universidad': 'Universidad Privada Antenor Orrego',
        'endpoints': {
            'health': '/api/health',
            'predict': '/api/predict (POST)',
            'model_info': '/api/model-info'
        }
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar estado del modelo"""
    if model is not None and scaler is not None:
        return jsonify({
            'status': 'healthy',
            'modelo_cargado': True,
            'mensaje': 'Sistema funcionando correctamente'
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'modelo_cargado': False,
            'mensaje': 'Modelo no cargado. Coloca modelo_rl.pkl y scaler.pkl en backend/model/'
        }), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Endpoint principal para realizar predicciones"""
    try:
        # Verificar que el modelo esté cargado
        if model is None or scaler is None:
            return jsonify({
                'error': 'Modelo no disponible',
                'detalle': 'Los archivos modelo_rl.pkl y scaler.pkl deben estar en backend/model/'
            }), 500

        # Obtener datos del request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No se recibieron datos',
                'detalle': 'El body del request debe contener datos en formato JSON'
            }), 400

        # Campos requeridos
        required_fields = [
            'genero', 'apoyo_familiar', 'ingresos_familiares',
            'horas_estudio', 'actividades_extra', 'nivel_educativo_padres',
            'acceso_internet', 'clima_familiar', 'asistencia', 'motivacion'
        ]
        
        # Verificar campos faltantes
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': 'Campos faltantes',
                'campos_requeridos': required_fields,
                'campos_faltantes': missing_fields
            }), 400

        # Preprocesar datos
        try:
            processed_data = preprocess_input(data)
        except ValueError as ve:
            return jsonify({
                'error': 'Error en validación de datos',
                'detalle': str(ve)
            }), 400

        # Realizar predicción
        result = predict_performance(model, scaler, processed_data)
        
        return jsonify(result), 200

    except ValueError as e:
        return jsonify({
            'error': 'Error en los datos de entrada',
            'detalle': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Error interno del servidor',
            'detalle': str(e)
        }), 500

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Información sobre el modelo entrenado"""
    return jsonify({
        'modelo': 'Regresión Logística',
        'descripcion': 'Modelo de clasificación para predecir rendimiento académico',
        'metricas': {
            'precision_entrenamiento': '54.3%',
            'precision_prueba': '40.0%',
            'validacion_cruzada': '38.6%',
            'estabilidad': 'Excelente (sin overfitting)'
        },
        'variables': [
            {'nombre': 'Género', 'tipo': 'Categórico', 'valores': ['M', 'F']},
            {'nombre': 'Apoyo Familiar', 'tipo': 'Numérico', 'rango': '1-5'},
            {'nombre': 'Ingresos Familiares', 'tipo': 'Numérico', 'rango': '1-5'},
            {'nombre': 'Horas de Estudio', 'tipo': 'Numérico', 'rango': '0-168'},
            {'nombre': 'Actividades Extracurriculares', 'tipo': 'Numérico', 'rango': '0-40'},
            {'nombre': 'Nivel Educativo Padres', 'tipo': 'Numérico', 'rango': '1-5'},
            {'nombre': 'Acceso a Internet', 'tipo': 'Binario', 'valores': [0, 1]},
            {'nombre': 'Clima Familiar', 'tipo': 'Numérico', 'rango': '1-5'},
            {'nombre': 'Asistencia', 'tipo': 'Numérico', 'rango': '0-100%'},
            {'nombre': 'Motivación', 'tipo': 'Numérico', 'rango': '1-5'}
        ],
        'clases': ['Alto', 'Medio', 'Bajo']
    }), 200

@app.route('/api/test', methods=['GET'])
def test_prediction():
    """Endpoint de prueba con datos de ejemplo"""
    if model is None or scaler is None:
        return jsonify({
            'error': 'Modelo no disponible'
        }), 500
    
    # Datos de prueba
    test_data = {
        'genero': 'F',
        'apoyo_familiar': 4,
        'ingresos_familiares': 3,
        'horas_estudio': 15,
        'actividades_extra': 5,
        'nivel_educativo_padres': 4,
        'acceso_internet': 1,
        'clima_familiar': 4,
        'asistencia': 90,
        'motivacion': 4
    }
    
    try:
        processed_data = preprocess_input(test_data)
        result = predict_performance(model, scaler, processed_data)
        return jsonify({
            'mensaje': 'Prueba exitosa',
            'datos_enviados': test_data,
            'resultado': result
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'Error en prueba',
            'detalle': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Manejo de rutas no encontradas"""
    return jsonify({
        'error': 'Ruta no encontrada',
        'mensaje': 'El endpoint solicitado no existe'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores internos"""
    return jsonify({
        'error': 'Error interno del servidor',
        'mensaje': 'Ocurrió un error inesperado'
    }), 500

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Iniciando servidor de predicción de rendimiento académico")
    print("=" * 60)
    print(f"📍 URL: http://localhost:5000")
    print(f"📊 Modelo: Regresión Logística")
    print(f"🏫 Universidad Privada Antenor Orrego")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
import joblib
import pandas as pd
import numpy as np
import os

print("=" * 70)
print("🔍 DIAGNÓSTICO DEL MODELO")
print("=" * 70)

# Verificar rutas
print("\n📂 Verificando archivos...")
modelo_path = 'model/modelo_rl.pkl'
scaler_path = 'model/scaler.pkl'

if os.path.exists(modelo_path):
    size = os.path.getsize(modelo_path)
    print(f"✅ modelo_rl.pkl existe ({size:,} bytes)")
else:
    print(f"❌ modelo_rl.pkl NO EXISTE en {os.path.abspath(modelo_path)}")

if os.path.exists(scaler_path):
    size = os.path.getsize(scaler_path)
    print(f"✅ scaler.pkl existe ({size:,} bytes)")
else:
    print(f"❌ scaler.pkl NO EXISTE en {os.path.abspath(scaler_path)}")

# Intentar cargar
print("\n📦 Intentando cargar archivos...")

try:
    modelo = joblib.load(modelo_path)
    print(f"✅ Modelo cargado exitosamente")
    print(f"   Tipo: {type(modelo).__name__}")
    
    if hasattr(modelo, 'n_features_in_'):
        print(f"   Características: {modelo.n_features_in_}")
    if hasattr(modelo, 'classes_'):
        print(f"   Clases: {modelo.classes_}")
        
except Exception as e:
    print(f"❌ ERROR al cargar modelo:")
    print(f"   {type(e).__name__}: {e}")
    print("\n⚠️  El archivo está corrupto o incompleto")
    print("   Solución: Exporta nuevamente desde Google Colab")
    exit(1)

try:
    scaler = joblib.load(scaler_path)
    print(f"✅ Scaler cargado exitosamente")
    print(f"   Tipo: {type(scaler).__name__}")
    
    if hasattr(scaler, 'n_features_in_'):
        print(f"   Características: {scaler.n_features_in_}")
        
except Exception as e:
    print(f"❌ ERROR al cargar scaler:")
    print(f"   {type(e).__name__}: {e}")
    print("\n⚠️  El archivo está corrupto o incompleto")
    print("   Solución: Exporta nuevamente desde Google Colab")
    exit(1)

# Hacer predicción de prueba
print("\n🧪 Prueba de predicción...")

try:
    datos_prueba = pd.DataFrame({
        'Genero': [1],
        'Apoyo_Familiar': [4],
        'Ingresos_Familiares': [3],
        'Horas_Estudio': [15.0],
        'Actividades_Extra': [5.0],
        'Nivel_Educativo_Padres': [4],
        'Acceso_Internet': [1],
        'Clima_Familiar': [4],
        'Asistencia': [90.0],
        'Motivacion': [4]
    })
    
    datos_norm = scaler.transform(datos_prueba)
    prediccion = modelo.predict(datos_norm)
    
    clases = ['Bajo', 'Medio', 'Alto']
    print(f"✅ Predicción exitosa: {clases[prediccion[0]]}")
    
    if hasattr(modelo, 'predict_proba'):
        probs = modelo.predict_proba(datos_norm)[0]
        print(f"\n📊 Probabilidades:")
        for i, prob in enumerate(probs):
            print(f"   {clases[i]}: {prob:.1%}")
    
    print("\n" + "=" * 70)
    print("✨ ¡TODO FUNCIONA CORRECTAMENTE!")
    print("=" * 70)
    print("\n✅ Puedes ejecutar: python app.py")
    
except Exception as e:
    print(f"❌ ERROR en predicción:")
    print(f"   {type(e).__name__}: {e}")
    exit(1)
import joblib
import pandas as pd
import numpy as np

print("🔍 Analizando el modelo...")
print("=" * 70)

# Cargar scaler y modelo
scaler = joblib.load('model/scaler.pkl')
modelo = joblib.load('model/modelo_rl.pkl')

# Ver cuántas features espera
print(f"\n📊 Características esperadas por el scaler: {scaler.n_features_in_}")
print(f"📊 Características esperadas por el modelo: {modelo.n_features_in_}")

# Ver si tiene nombres de features
if hasattr(scaler, 'feature_names_in_'):
    print(f"\n📋 Nombres de las columnas esperadas:")
    for i, name in enumerate(scaler.feature_names_in_, 1):
        print(f"   {i}. {name}")
else:
    print("\n⚠️  El scaler no tiene nombres de features guardados")
    print("   Se entrenó con un array numpy sin nombres de columnas")

if hasattr(modelo, 'feature_names_in_'):
    print(f"\n📋 Columnas que espera el modelo:")
    for i, name in enumerate(modelo.feature_names_in_, 1):
        print(f"   {i}. {name}")
else:
    print("\n⚠️  El modelo no tiene nombres de features guardados")

print("\n" + "=" * 70)
print("💡 Posibles soluciones:")
print("1. Volver a entrenar el modelo con solo 10 features")
print("2. Adaptar el preprocesamiento para generar 23 features")
print("3. Revisar el notebook original para ver qué columnas usaste")
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import joblib
import os

print("🤖 Entrenando modelo con 10 características...")
print("=" * 70)

# Crear dataset sintético con las 10 variables de tu sistema
np.random.seed(42)
n_samples = 200

# Generar datos realistas
data = {
    'Genero': np.random.randint(0, 2, n_samples),
    'Apoyo_Familiar': np.random.randint(1, 6, n_samples),
    'Ingresos_Familiares': np.random.randint(1, 6, n_samples),
    'Horas_Estudio': np.random.uniform(0, 40, n_samples),
    'Actividades_Extra': np.random.uniform(0, 20, n_samples),
    'Nivel_Educativo_Padres': np.random.randint(1, 6, n_samples),
    'Acceso_Internet': np.random.randint(0, 2, n_samples),
    'Clima_Familiar': np.random.randint(1, 6, n_samples),
    'Asistencia': np.random.uniform(60, 100, n_samples),
    'Motivacion': np.random.randint(1, 6, n_samples)
}

df = pd.DataFrame(data)

# Crear variable objetivo basada en factores importantes
# Lógica: buenos estudiantes = más horas estudio + apoyo + motivación
rendimiento_score = (
    (df['Horas_Estudio'] / 40) * 0.3 +
    (df['Apoyo_Familiar'] / 5) * 0.25 +
    (df['Motivacion'] / 5) * 0.2 +
    (df['Asistencia'] / 100) * 0.15 +
    (df['Clima_Familiar'] / 5) * 0.1
)

# Clasificar en 3 categorías
df['Rendimiento'] = pd.cut(
    rendimiento_score, 
    bins=[0, 0.4, 0.7, 1.0], 
    labels=[0, 1, 2]  # 0=Bajo, 1=Medio, 2=Alto
)

print(f"📊 Dataset generado:")
print(f"   - Total de muestras: {len(df)}")
print(f"   - Bajo: {(df['Rendimiento'] == 0).sum()}")
print(f"   - Medio: {(df['Rendimiento'] == 1).sum()}")
print(f"   - Alto: {(df['Rendimiento'] == 2).sum()}")

# Separar X e y
X = df.drop('Rendimiento', axis=1)
y = df['Rendimiento']

print(f"\n📋 Columnas del modelo (en orden):")
for i, col in enumerate(X.columns, 1):
    print(f"   {i}. {col}")

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print(f"\n🔧 Conjuntos de datos:")
print(f"   - Entrenamiento: {len(X_train)} muestras")
print(f"   - Prueba: {len(X_test)} muestras")

# Normalizar (IMPORTANTE: convertir a numpy array)
scaler = MinMaxScaler()
X_train_array = X_train.values  # Convertir a numpy
X_test_array = X_test.values

X_train_scaled = scaler.fit_transform(X_train_array)
X_test_scaled = scaler.transform(X_test_array)

print(f"\n✅ Normalización completada")
print(f"   - Features esperadas: {scaler.n_features_in_}")

# Entrenar modelo
print(f"\n🤖 Entrenando Regresión Logística...")
modelo = LogisticRegression(
    max_iter=1000,
    random_state=42,
    solver='lbfgs',
    multi_class='multinomial'
)
modelo.fit(X_train_scaled, y_train)

# Evaluar
accuracy_train = modelo.score(X_train_scaled, y_train)
accuracy_test = modelo.score(X_test_scaled, y_test)

print(f"\n✅ Modelo entrenado exitosamente")
print(f"   - Precisión en entrenamiento: {accuracy_train:.2%}")
print(f"   - Precisión en prueba: {accuracy_test:.2%}")

# Crear carpeta model si no existe
os.makedirs('model', exist_ok=True)

# IMPORTANTE: Hacer backup del modelo anterior
if os.path.exists('model/modelo_rl.pkl'):
    os.rename('model/modelo_rl.pkl', 'model/modelo_rl_old.pkl')
    print(f"\n📦 Backup creado: modelo_rl_old.pkl")

if os.path.exists('model/scaler.pkl'):
    os.rename('model/scaler.pkl', 'model/scaler_old.pkl')
    print(f"📦 Backup creado: scaler_old.pkl")

# Guardar nuevo modelo y scaler
joblib.dump(modelo, 'model/modelo_rl.pkl')
joblib.dump(scaler, 'model/scaler.pkl')

modelo_size = os.path.getsize('model/modelo_rl.pkl')
scaler_size = os.path.getsize('model/scaler.pkl')

print(f"\n💾 Archivos guardados:")
print(f"   ✅ modelo_rl.pkl ({modelo_size:,} bytes)")
print(f"   ✅ scaler.pkl ({scaler_size:,} bytes)")

# Verificar que funciona
print(f"\n🧪 Verificando el modelo...")
try:
    test_modelo = joblib.load('model/modelo_rl.pkl')
    test_scaler = joblib.load('model/scaler.pkl')
    
    # Prueba con datos de ejemplo
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
    
    datos_array = datos_prueba.values
    datos_norm = test_scaler.transform(datos_array)
    prediccion = test_modelo.predict(datos_norm)[0]
    probs = test_modelo.predict_proba(datos_norm)[0]
    
    clases = ['Bajo', 'Medio', 'Alto']
    print(f"   ✅ Predicción de prueba: {clases[prediccion]}")
    print(f"   ✅ Probabilidades: {probs}")
    
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print("\n" + "=" * 70)
print("✨ ¡Modelo compatible creado exitosamente!")
print("=" * 70)
print("\n📝 Próximos pasos:")
print("1. Detén el servidor backend (Ctrl+C)")
print("2. Ejecuta: python app.py")
print("3. Prueba la predicción en el navegador")
print("\n💡 El modelo anterior fue respaldado como modelo_rl_old.pkl")
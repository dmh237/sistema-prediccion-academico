# Sistema de Predicción de Rendimiento Académico

Sistema web profesional que utiliza Machine Learning (Regresión Logística) para predecir el rendimiento académico de estudiantes basándose en 10 variables clave.

## Universidad
**Universidad Privada Antenor Orrego (UPAO)**  
Facultad de Ingeniería  
Programa de Ingeniería de Computación y Sistemas


## Características

 **Predicción en tiempo real** del rendimiento académico (Alto/Medio/Bajo)  
 **Análisis de variables** familiares, socioeconómicas y personales  
 **Recomendaciones personalizadas** según el perfil del estudiante  
 **Interfaz web moderna** y responsive  
 **API REST** completa con Flask  
 **Modelo de Machine Learning** (Regresión Logística)

## Tecnologías Utilizadas

### Backend
- Python 3.8+
- Flask (API REST)
- scikit-learn (Machine Learning)
- pandas & numpy (Procesamiento de datos)
- joblib (Serialización del modelo)

### Frontend
- HTML5, CSS3, JavaScript
- Diseño responsive
- Animaciones CSS
- Fetch API

### Machine Learning
- Regresión Logística
- MinMaxScaler (Normalización)
- Validación cruzada (10-fold)

## Variables del Modelo

1. **Género** (M/F)
2. **Apoyo Familiar** (1-5)
3. **Ingresos Familiares** (1-5)
4. **Horas de Estudio** (0-168)
5. **Actividades Extracurriculares** (0-40)
6. **Nivel Educativo de los Padres** (1-5)
7. **Acceso a Internet** (Sí/No)
8. **Clima Familiar** (1-5)
9. **Asistencia** (0-100%)
10. **Motivación** (1-5)

## Instalación y Ejecución

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/sistema-prediccion-academico.git
cd sistema-prediccion-academico
```

### 2. Configurar el Backend
```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python app.py
```

El backend estará disponible en: `http://localhost:5000`

### 3. Configurar el Frontend
```bash
cd frontend

# Opción 1: Python HTTP Server
python -m http.server 8000

# Opción 2: Abrir index.html directamente en el navegador
```

El frontend estará disponible en: `http://localhost:8000`

## Métricas del Modelo

- **Modelo:** Regresión Logística
- **Precisión en entrenamiento:** 54.3%
- **Precisión en prueba:** 40.0%
- **Validación cruzada:** 38.6%
- **Clases:** Alto, Medio, Bajo


## Contribuciones

Este es un proyecto académico. Si deseas contribuir o reportar problemas, por favor abre un issue.

## Licencia

Proyecto Académico - Universidad Privada Antenor Orrego © 2025


**Desarrollado con por estudiantes de 5° ciclo de la carrera de Ingeniería de Computación y Sistemas - UPAO**

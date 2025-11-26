import numpy as np
import pandas as pd

def predict_performance(model, scaler, data):
    """
    Realiza la predicción del rendimiento académico
    
    Args:
        model: Modelo de ML cargado (Regresión Logística)
        scaler: Scaler para normalización
        data (pd.DataFrame): Datos preprocesados del estudiante
    
    Returns:
        dict: Resultado con predicción, probabilidades y factores clave
    """
    try:
        # IMPORTANTE: Convertir a numpy array para evitar warning de feature names
        data_array = data.values
        
        # Normalizar datos usando el scaler entrenado
        data_scaled = scaler.transform(data_array)
        
        # Realizar predicción
        prediction = model.predict(data_scaled)[0]
        
        # Obtener probabilidades para cada clase
        probabilities = model.predict_proba(data_scaled)[0]
        
        # Mapear índices a nombres de clases
        class_names = ['Bajo', 'Medio', 'Alto']
        
        # Crear diccionario de probabilidades
        prob_dict = {
            class_names[i]: float(probabilities[i])
            for i in range(len(class_names))
        }
        
        # Determinar predicción final
        predicted_class = class_names[prediction]
        
        # Identificar factores clave basados en los valores de entrada
        key_factors = identify_key_factors(data)
        
        # Obtener recomendaciones personalizadas
        recommendations = get_recommendations(predicted_class, data)
        
        # Construir respuesta
        result = {
            'prediccion': predicted_class,
            'probabilidades': prob_dict,
            'factores_clave': key_factors,
            'recomendaciones': recommendations,
            'confianza': float(max(probabilities))
        }
        
        print(f"✅ Predicción exitosa: {predicted_class}")
        print(f"   Probabilidades: {prob_dict}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error en predicción: {type(e).__name__}: {e}")
        raise Exception(f'Error en la predicción: {str(e)}')

def identify_key_factors(data):
    """
    Identifica los factores más relevantes basándose en los valores de entrada
    
    Args:
        data (pd.DataFrame): Datos del estudiante
    
    Returns:
        list: Lista de factores clave identificados
    """
    factors = []
    
    # Extraer valores
    apoyo_familiar = data['Apoyo_Familiar'].values[0]
    ingresos = data['Ingresos_Familiares'].values[0]
    horas_estudio = data['Horas_Estudio'].values[0]
    nivel_educativo = data['Nivel_Educativo_Padres'].values[0]
    clima_familiar = data['Clima_Familiar'].values[0]
    motivacion = data['Motivacion'].values[0]
    asistencia = data['Asistencia'].values[0]
    
    # Identificar factores positivos y negativos
    if apoyo_familiar >= 4:
        factors.append('Alto Apoyo Familiar')
    elif apoyo_familiar <= 2:
        factors.append('Bajo Apoyo Familiar (⚠️)')
    
    if horas_estudio >= 15:
        factors.append('Buenos Hábitos de Estudio')
    elif horas_estudio < 5:
        factors.append('Pocas Horas de Estudio (⚠️)')
    
    if motivacion >= 4:
        factors.append('Alta Motivación')
    elif motivacion <= 2:
        factors.append('Baja Motivación (⚠️)')
    
    if asistencia >= 90:
        factors.append('Excelente Asistencia')
    elif asistencia < 70:
        factors.append('Baja Asistencia (⚠️)')
    
    if clima_familiar >= 4:
        factors.append('Buen Clima Familiar')
    
    if nivel_educativo >= 4:
        factors.append('Alto Nivel Educativo de los Padres')
    
    if ingresos >= 4:
        factors.append('Buenos Recursos Económicos')
    elif ingresos <= 2:
        factors.append('Recursos Económicos Limitados (⚠️)')
    
    # Si no se identificaron factores específicos, agregar los 3 más importantes
    if len(factors) == 0:
        factors = ['Apoyo Familiar', 'Horas de Estudio', 'Motivación']
    
    return factors[:5]  # Retornar máximo 5 factores

def get_recommendations(prediction, data):
    """
    Genera recomendaciones personalizadas basadas en la predicción
    
    Args:
        prediction (str): Clase predicha ('Alto', 'Medio', 'Bajo')
        data (pd.DataFrame): Datos del estudiante
    
    Returns:
        list: Lista de recomendaciones
    """
    recommendations = []
    
    horas_estudio = data['Horas_Estudio'].values[0]
    apoyo_familiar = data['Apoyo_Familiar'].values[0]
    motivacion = data['Motivacion'].values[0]
    asistencia = data['Asistencia'].values[0]
    
    if prediction == 'Bajo':
        recommendations.append('Incrementar las horas de estudio semanales')
        recommendations.append('Buscar apoyo tutorial o asesoría académica')
        recommendations.append('Mejorar la asistencia a clases')
        recommendations.append('Establecer un plan de estudio estructurado')
        recommendations.append('Fomentar la comunicación con la familia sobre el progreso académico')
    
    elif prediction == 'Medio':
        if horas_estudio < 10:
            recommendations.append('Aumentar gradualmente las horas de estudio')
        if motivacion <= 3:
            recommendations.append('Participar en actividades que refuercen el interés académico')
        if asistencia < 85:
            recommendations.append('Mejorar la asistencia regular a clases')
        recommendations.append('Establecer metas académicas claras a corto plazo')
        recommendations.append('Mantener comunicación constante con docentes')
    
    else:  # Alto
        recommendations.append('Mantener los buenos hábitos de estudio')
        recommendations.append('Participar en actividades de liderazgo académico')
        recommendations.append('Considerar programas de tutoría para apoyar a otros estudiantes')
        recommendations.append('Explorar oportunidades de investigación o proyectos avanzados')
    
    return recommendations
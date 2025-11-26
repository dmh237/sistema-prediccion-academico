import pandas as pd
import numpy as np

def preprocess_input(data):
    """
    Preprocesa los datos de entrada del formulario
    
    Args:
        data (dict): Diccionario con los datos del estudiante
    
    Returns:
        pd.DataFrame: DataFrame con datos procesados listos para el modelo
    """
    try:
        # Mapeo de género
        genero_map = {'M': 0, 'F': 1}
        genero_numeric = genero_map.get(str(data['genero']).upper(), 0)
        
        # Convertir acceso a internet
        acceso_internet = int(data['acceso_internet'])
        
        # Crear DataFrame con el orden correcto de columnas
        processed_data = pd.DataFrame({
            'Genero': [genero_numeric],
            'Apoyo_Familiar': [int(data['apoyo_familiar'])],
            'Ingresos_Familiares': [int(data['ingresos_familiares'])],
            'Horas_Estudio': [float(data['horas_estudio'])],
            'Actividades_Extra': [float(data['actividades_extra'])],
            'Nivel_Educativo_Padres': [int(data['nivel_educativo_padres'])],
            'Acceso_Internet': [acceso_internet],
            'Clima_Familiar': [int(data['clima_familiar'])],
            'Asistencia': [float(data['asistencia'])],
            'Motivacion': [int(data['motivacion'])]
        })
        
        # Validaciones de rango
        validations = {
            'Apoyo_Familiar': (1, 5),
            'Ingresos_Familiares': (1, 5),
            'Horas_Estudio': (0, 168),
            'Actividades_Extra': (0, 40),
            'Nivel_Educativo_Padres': (1, 5),
            'Acceso_Internet': (0, 1),
            'Clima_Familiar': (1, 5),
            'Asistencia': (0, 100),
            'Motivacion': (1, 5)
        }
        
        for col, (min_val, max_val) in validations.items():
            value = processed_data[col].values[0]
            if not (min_val <= value <= max_val):
                raise ValueError(f'{col} debe estar entre {min_val} y {max_val}. Valor recibido: {value}')
        
        return processed_data
        
    except KeyError as e:
        raise ValueError(f'Campo faltante: {e}')
    except (ValueError, TypeError) as e:
        raise ValueError(f'Error en conversión de datos: {e}')

def validate_input(data):
    """
    Valida que los datos de entrada sean correctos
    
    Args:
        data (dict): Datos a validar
    
    Returns:
        tuple: (bool, str) - (es_valido, mensaje_error)
    """
    required_fields = [
        'genero', 'apoyo_familiar', 'ingresos_familiares',
        'horas_estudio', 'actividades_extra', 'nivel_educativo_padres',
        'acceso_internet', 'clima_familiar', 'asistencia', 'motivacion'
    ]
    
    # Verificar campos requeridos
    for field in required_fields:
        if field not in data:
            return False, f'Campo requerido faltante: {field}'
    
    # Validar género
    if str(data['genero']).upper() not in ['M', 'F']:
        return False, 'Género debe ser M o F'
    
    try:
        # Validaciones numéricas
        apoyo = int(data['apoyo_familiar'])
        if not (1 <= apoyo <= 5):
            return False, 'Apoyo familiar debe estar entre 1 y 5'
        
        ingresos = int(data['ingresos_familiares'])
        if not (1 <= ingresos <= 5):
            return False, 'Ingresos familiares debe estar entre 1 y 5'
        
        horas = float(data['horas_estudio'])
        if not (0 <= horas <= 168):
            return False, 'Horas de estudio debe estar entre 0 y 168'
        
        actividades = float(data['actividades_extra'])
        if not (0 <= actividades <= 40):
            return False, 'Actividades extra debe estar entre 0 y 40'
        
        nivel_edu = int(data['nivel_educativo_padres'])
        if not (1 <= nivel_edu <= 5):
            return False, 'Nivel educativo padres debe estar entre 1 y 5'
        
        internet = int(data['acceso_internet'])
        if internet not in [0, 1]:
            return False, 'Acceso a internet debe ser 0 o 1'
        
        clima = int(data['clima_familiar'])
        if not (1 <= clima <= 5):
            return False, 'Clima familiar debe estar entre 1 y 5'
        
        asistencia = float(data['asistencia'])
        if not (0 <= asistencia <= 100):
            return False, 'Asistencia debe estar entre 0 y 100'
        
        motivacion = int(data['motivacion'])
        if not (1 <= motivacion <= 5):
            return False, 'Motivación debe estar entre 1 y 5'
            
    except (ValueError, TypeError) as e:
        return False, f'Error en formato de datos: {str(e)}'
    
    return True, 'Datos válidos'
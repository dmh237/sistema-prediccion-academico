const API_URL = 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', function() {
    const predictBtn = document.getElementById('predict-btn');
    const clearBtn = document.getElementById('clear-btn');
    
    // Event listeners
    predictBtn.addEventListener('click', handlePredict);
    clearBtn.addEventListener('click', clearForm);
    
    // Sincronizar sliders con inputs numéricos
    setupRangeInputs();
    
    // Agregar validación en tiempo real
    setupRealtimeValidation();
    
    // Animación de entrada
    animateFormFields();
});

// ===== SINCRONIZAR SLIDERS CON INPUTS =====
function setupRangeInputs() {
    const ranges = [
        { slider: 'apoyo_familiar_range', input: 'apoyo_familiar' },
        { slider: 'ingresos_familiares_range', input: 'ingresos_familiares' },
        { slider: 'nivel_educativo_padres_range', input: 'nivel_educativo_padres' },
        { slider: 'clima_familiar_range', input: 'clima_familiar' },
        { slider: 'motivacion_range', input: 'motivacion' }
    ];
    
    ranges.forEach(({ slider, input }) => {
        const sliderEl = document.getElementById(slider);
        const inputEl = document.getElementById(input);
        
        if (sliderEl && inputEl) {
            // Sincronizar slider -> input
            sliderEl.addEventListener('input', (e) => {
                inputEl.value = e.target.value;
                updateSliderBackground(sliderEl);
            });
            
            // Sincronizar input -> slider
            inputEl.addEventListener('input', (e) => {
                const value = Math.min(Math.max(parseInt(e.target.value) || 1, 1), 5);
                sliderEl.value = value;
                inputEl.value = value;
                updateSliderBackground(sliderEl);
            });
            
            // Inicializar color
            updateSliderBackground(sliderEl);
        }
    });
}

function updateSliderBackground(slider) {
    const min = slider.min || 1;
    const max = slider.max || 5;
    const value = slider.value;
    const percentage = ((value - min) / (max - min)) * 100;
    
    slider.style.background = `linear-gradient(to right, #667eea 0%, #764ba2 ${percentage}%, #e5e7eb ${percentage}%, #e5e7eb 100%)`;
}

// ===== VALIDACIÓN EN TIEMPO REAL =====
function setupRealtimeValidation() {
    const inputs = document.querySelectorAll('input[type="number"]:not([id$="_range"])');
    
    inputs.forEach(input => {
        input.addEventListener('input', (e) => {
            validateInput(e.target);
        });
        
        input.addEventListener('blur', (e) => {
            validateInput(e.target);
        });
    });
}

function validateInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);
    
    // Remover estados previos
    input.classList.remove('input-valid', 'input-invalid');
    
    if (input.value === '') {
        return;
    }
    
    if (value < min || value > max || isNaN(value)) {
        input.classList.add('input-invalid');
        input.style.borderColor = '#ef4444';
    } else {
        input.classList.add('input-valid');
        input.style.borderColor = '#10b981';
    }
}

// ===== ANIMACIÓN DE ENTRADA =====
function animateFormFields() {
    const fields = document.querySelectorAll('.form-group');
    fields.forEach((field, index) => {
        field.style.animationDelay = `${index * 0.05}s`;
    });
}

// ===== MANEJAR PREDICCIÓN =====
async function handlePredict() {
    const predictBtn = document.getElementById('predict-btn');
    const resultContent = document.getElementById('result-content');
    
    // Recolectar datos del formulario
    const formData = {
        genero: document.getElementById('genero').value,
        apoyo_familiar: document.getElementById('apoyo_familiar').value,
        ingresos_familiares: document.getElementById('ingresos_familiares').value,
        horas_estudio: document.getElementById('horas_estudio').value,
        actividades_extra: document.getElementById('actividades_extra').value,
        nivel_educativo_padres: document.getElementById('nivel_educativo_padres').value,
        acceso_internet: document.getElementById('acceso_internet').value,
        clima_familiar: document.getElementById('clima_familiar').value,
        asistencia: document.getElementById('asistencia').value,
        motivacion: document.getElementById('motivacion').value
    };
    
    // Validar campos completos
    for (let key in formData) {
        if (!formData[key]) {
            showError('Por favor complete todos los campos del formulario');
            highlightEmptyFields();
            return;
        }
    }
    
    // Validar rangos
    if (!validateRanges(formData)) {
        return;
    }
    
    // Mostrar loading
    predictBtn.disabled = true;
    predictBtn.innerHTML = '<span class="loading"></span> Analizando datos...';
    
    // Mostrar loading en el panel de resultados
    showLoadingState();
    
    try {
        const response = await fetch(`${API_URL}/api/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error en la predicción');
        }
        
        const result = await response.json();
        
        // Pequeño delay para efecto visual
        setTimeout(() => {
            displayResult(result);
        }, 500);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Error de conexión con el servidor. Verifique que el backend esté ejecutándose en http://localhost:5000');
    } finally {
        predictBtn.disabled = false;
        predictBtn.innerHTML = '<span class="btn-icon">🚀</span> Realizar Predicción';
    }
}

function showLoadingState() {
    const resultContent = document.getElementById('result-content');
    resultContent.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">
                <div class="loading" style="width: 48px; height: 48px; border-width: 4px;"></div>
            </div>
            <p class="empty-text">Procesando datos...</p>
            <p class="empty-subtext">El modelo está analizando la información del estudiante</p>
        </div>
    `;
}

function highlightEmptyFields() {
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        if (!input.value) {
            input.style.borderColor = '#ef4444';
            input.style.animation = 'shake 0.3s ease-in-out';
            setTimeout(() => {
                input.style.animation = '';
            }, 300);
        }
    });
}

function validateRanges(data) {
    const validations = [
        { field: 'apoyo_familiar', min: 1, max: 5, name: 'Apoyo Familiar' },
        { field: 'ingresos_familiares', min: 1, max: 5, name: 'Ingresos Familiares' },
        { field: 'horas_estudio', min: 0, max: 168, name: 'Horas de Estudio' },
        { field: 'actividades_extra', min: 0, max: 40, name: 'Actividades Extra' },
        { field: 'nivel_educativo_padres', min: 1, max: 5, name: 'Nivel Educativo Padres' },
        { field: 'clima_familiar', min: 1, max: 5, name: 'Clima Familiar' },
        { field: 'asistencia', min: 0, max: 100, name: 'Asistencia' },
        { field: 'motivacion', min: 1, max: 5, name: 'Motivación' }
    ];
    
    for (let validation of validations) {
        const value = parseFloat(data[validation.field]);
        if (value < validation.min || value > validation.max) {
            showError(`${validation.name} debe estar entre ${validation.min} y ${validation.max}`);
            
            // Highlight el campo con error
            const input = document.getElementById(validation.field);
            if (input) {
                input.style.borderColor = '#ef4444';
                input.focus();
            }
            return false;
        }
    }
    
    return true;
}

// ===== MOSTRAR RESULTADO =====
function displayResult(result) {
    const resultContent = document.getElementById('result-content');
    const prediccion = result.prediccion;
    const probabilidades = result.probabilidades;
    const recomendaciones = result.recomendaciones || [
        'Mantener comunicación constante con la familia',
        'Establecer horarios de estudio regulares',
        'Participar en actividades de apoyo académico',
        'Consultar con tutores ante dificultades'
    ];
    
    const prediccionClass = prediccion.toLowerCase();
    
    // Emojis según la predicción
    const emojiMap = {
        'alto': '🎉',
        'medio': '📈',
        'bajo': '⚠️'
    };
    
    const emoji = emojiMap[prediccionClass];
    
    resultContent.innerHTML = `
        <div class="prediction-result">
            <div class="prediction-box ${prediccionClass}">
                <p class="prediction-label">${emoji} Resultado de la Predicción</p>
                <p class="prediction-value ${prediccionClass}">Rendimiento ${prediccion}</p>
                <p style="margin-top: 12px; color: var(--gray-600); font-size: 14px;">
                    Confianza: ${(result.confianza * 100).toFixed(1)}%
                </p>
            </div>
            
            <div class="probabilities">
                <h3>📊 Distribución de Probabilidades</h3>
                ${Object.entries(probabilidades).map(([clase, prob]) => `
                    <div class="prob-item">
                        <div class="prob-label">
                            <span>${clase}</span>
                            <span style="color: var(--primary); font-weight: 700;">${(prob * 100).toFixed(1)}%</span>
                        </div>
                        <div class="prob-bar">
                            <div class="prob-fill ${clase.toLowerCase()}" style="width: 0%" data-width="${prob * 100}"></div>
                        </div>
                    </div>
                `).join('')}
            </div>
            
            <div class="recommendations-box">
                <h3>💡 Recomendaciones Personalizadas</h3>
                <ul class="recommendations-list">
                    ${recomendaciones.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
        </div>
    `;
    
    // Animar las barras de probabilidad
    setTimeout(() => {
        document.querySelectorAll('.prob-fill').forEach(bar => {
            const width = bar.getAttribute('data-width');
            bar.style.width = width + '%';
        });
    }, 100);
    
    // Scroll suave al resultado (en móviles)
    if (window.innerWidth < 1024) {
        resultContent.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    // Confetti si el resultado es Alto
    if (prediccionClass === 'alto') {
        launchConfetti();
    }
}

// ===== CONFETTI EFFECT =====
function launchConfetti() {
    const colors = ['#667eea', '#764ba2', '#10b981', '#f59e0b', '#ef4444'];
    const confettiCount = 50;
    
    for (let i = 0; i < confettiCount; i++) {
        setTimeout(() => {
            createConfettiPiece(colors[Math.floor(Math.random() * colors.length)]);
        }, i * 30);
    }
}

function createConfettiPiece(color) {
    const confetti = document.createElement('div');
    confetti.style.cssText = `
        position: fixed;
        width: 10px;
        height: 10px;
        background: ${color};
        top: -10px;
        left: ${Math.random() * 100}%;
        opacity: 1;
        transform: rotate(${Math.random() * 360}deg);
        pointer-events: none;
        z-index: 9999;
        border-radius: 2px;
    `;
    
    document.body.appendChild(confetti);
    
    const duration = 2000 + Math.random() * 1000;
    const startTime = Date.now();
    
    function animate() {
        const elapsed = Date.now() - startTime;
        const progress = elapsed / duration;
        
        if (progress < 1) {
            const y = progress * window.innerHeight;
            const x = Math.sin(progress * 10) * 100;
            const rotation = progress * 720;
            const opacity = 1 - progress;
            
            confetti.style.transform = `translate(${x}px, ${y}px) rotate(${rotation}deg)`;
            confetti.style.opacity = opacity;
            
            requestAnimationFrame(animate);
        } else {
            confetti.remove();
        }
    }
    
    animate();
}

// ===== MOSTRAR ERROR =====
function showError(message) {
    const resultContent = document.getElementById('result-content');
    resultContent.innerHTML = `
        <div class="error-message">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <div>
                <strong style="display: block; margin-bottom: 4px;">Error</strong>
                <span>${message}</span>
            </div>
        </div>
    `;
    
    if (window.innerWidth < 1024) {
        resultContent.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// ===== LIMPIAR FORMULARIO =====
function clearForm() {
    // Limpiar inputs
    document.querySelectorAll('input[type="number"]').forEach(input => {
        if (input.id.includes('_range')) {
            input.value = 3;
            updateSliderBackground(input);
        } else {
            input.value = '';
        }
        input.style.borderColor = '';
        input.classList.remove('input-valid', 'input-invalid');
    });
    
    // Limpiar selects
    document.querySelectorAll('select').forEach(select => {
        select.value = '';
        select.style.borderColor = '';
    });
    
    // Sincronizar valores de los rangos
    const ranges = [
        { slider: 'apoyo_familiar_range', input: 'apoyo_familiar' },
        { slider: 'ingresos_familiares_range', input: 'ingresos_familiares' },
        { slider: 'nivel_educativo_padres_range', input: 'nivel_educativo_padres' },
        { slider: 'clima_familiar_range', input: 'clima_familiar' },
        { slider: 'motivacion_range', input: 'motivacion' }
    ];
    
    ranges.forEach(({ slider, input }) => {
        const sliderEl = document.getElementById(slider);
        const inputEl = document.getElementById(input);
        if (sliderEl && inputEl) {
            sliderEl.value = 3;
            inputEl.value = 3;
            updateSliderBackground(sliderEl);
        }
    });
    
    // Resetear vista de resultados
    const resultContent = document.getElementById('result-content');
    resultContent.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
            </div>
            <p class="empty-text">Complete el formulario para obtener la predicción</p>
            <p class="empty-subtext">El sistema analizará los datos del estudiante</p>
        </div>
    `;
    
    const formContainer = document.querySelector('.form-container');
    formContainer.style.animation = 'fadeIn 0.3s ease';
    setTimeout(() => {
        formContainer.style.animation = '';
    }, 300);
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== AGREGAR ESTILOS DINÁMICOS =====
const style = document.createElement('style');
style.textContent = `
    .input-valid {
        border-color: #10b981 !important;
        background: #f0fdf4;
    }
    
    .input-invalid {
        border-color: #ef4444 !important;
        background: #fef2f2;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
`;
document.head.appendChild(style);

console.log('%c🎓 Sistema de Predicción de Rendimiento Académico', 'color: #667eea; font-size: 20px; font-weight: bold;');
console.log('%cUniversidad Privada Antenor Orrego', 'color: #764ba2; font-size: 14px;');
console.log('%cDesarrollado con Machine Learning 🤖', 'color: #10b981; font-size: 12px;');
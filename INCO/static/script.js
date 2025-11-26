// Complete Form JavaScript
class CompleteForm {
    constructor() {
        this.form = document.getElementById('loginForm');
        this.submitBtn = this.form.querySelector('.login-btn');
        this.successMessage = document.getElementById('successMessage');
        this.isSubmitting = false;
        
        this.validators = {
            nombre: this.validateNombre,
            email: FormUtils.validateEmail,
            telefono: this.validateTelefono,
            edad: this.validateEdad,
            nivel: this.validateSelect,
            area: this.validateSelect,
            modalidad: this.validateRadio,
            horario: this.validateRadio,
            terminos: this.validateTerminos
        };
        
        this.init();
    }
    
    init() {
        this.addEventListeners();
        this.setupFloatingLabels();
        this.setupRangeSlider();
        this.setupCheckboxes();
        this.setupRadioButtons();
        this.addBackgroundEffects();
        this.addEntranceAnimations();
        FormUtils.addSharedAnimations();
    }
    
    addEventListeners() {
        // Form submission
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Real-time validation for text inputs
        ['nombre', 'email', 'telefono', 'edad'].forEach(fieldName => {
            const field = document.getElementById(fieldName);
            if (field) {
                field.addEventListener('blur', () => this.validateField(fieldName));
                field.addEventListener('input', () => this.clearError(fieldName));
            }
        });
        
        // Select validation
        ['nivel', 'area'].forEach(fieldName => {
            const field = document.getElementById(fieldName);
            if (field) {
                field.addEventListener('change', () => this.validateField(fieldName));
            }
        });
        
        // Radio buttons validation
        document.querySelectorAll('input[type="radio"]').forEach(radio => {
            radio.addEventListener('change', () => {
                this.validateField(radio.name);
                this.animateRadioSelection(radio);
            });
        });
        
        // Términos checkbox
        const terminos = document.getElementById('terminos');
        if (terminos) {
            terminos.addEventListener('change', () => {
                this.validateField('terminos');
                this.animateCheckbox(terminos);
            });
        }
        
        // Enhanced focus effects
        const inputs = this.form.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"], input[type="number"], textarea');
        inputs.forEach(input => {
            input.addEventListener('focus', (e) => this.handleFocus(e));
            input.addEventListener('blur', (e) => this.handleBlur(e));
        });
        
        // Keyboard shortcuts
        this.setupKeyboardShortcuts();
    }
    
    setupFloatingLabels() {
        const inputs = this.form.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"], input[type="number"], textarea');
        inputs.forEach(input => {
            if (input.value.trim() !== '') {
                input.classList.add('has-value');
            }
            
            input.addEventListener('input', () => {
                if (input.value.trim() !== '') {
                    input.classList.add('has-value');
                } else {
                    input.classList.remove('has-value');
                }
            });
        });
    }
    
    setupRangeSlider() {
        const rangeInput = document.getElementById('presupuesto');
        const rangeValue = document.getElementById('presupuestoValue');
        
        if (rangeInput && rangeValue) {
            rangeInput.addEventListener('input', (e) => {
                rangeValue.textContent = `$${e.target.value}`;
                
                // Add glow effect
                rangeInput.style.boxShadow = '0 0 15px rgba(0, 255, 136, 0.3)';
                setTimeout(() => {
                    rangeInput.style.boxShadow = '';
                }, 200);
            });
        }
    }
    
    setupCheckboxes() {
        const checkboxes = this.form.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                this.animateCheckbox(checkbox);
            });
        });
    }
    
    setupRadioButtons() {
        const radioButtons = this.form.querySelectorAll('input[type="radio"]');
        radioButtons.forEach(radio => {
            radio.addEventListener('change', () => {
                this.animateRadioSelection(radio);
            });
        });
    }
    
    animateCheckbox(checkbox) {
        const customCheckbox = checkbox.nextElementSibling;
        if (customCheckbox) {
            customCheckbox.style.transform = 'scale(0.8)';
            customCheckbox.style.boxShadow = '0 0 15px rgba(0, 255, 136, 0.5)';
            setTimeout(() => {
                customCheckbox.style.transform = 'scale(1)';
                setTimeout(() => {
                    customCheckbox.style.boxShadow = '';
                }, 200);
            }, 150);
        }
    }
    
    animateRadioSelection(radio) {
        const label = radio.closest('.radio-label');
        if (label) {
            label.style.transform = 'scale(0.98)';
            label.style.boxShadow = '0 0 20px rgba(0, 255, 136, 0.3)';
            setTimeout(() => {
                label.style.transform = 'scale(1)';
                setTimeout(() => {
                    label.style.boxShadow = '';
                }, 200);
            }, 150);
        }
    }
    
    addBackgroundEffects() {
        document.addEventListener('mousemove', (e) => {
            const orbs = document.querySelectorAll('.glow-orb');
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;
            
            orbs.forEach((orb, index) => {
                const speed = (index + 1) * 0.5;
                const moveX = (x - 0.5) * speed * 20;
                const moveY = (y - 0.5) * speed * 20;
                orb.style.transform = `translate(${moveX}px, ${moveY}px)`;
            });
        });
    }
    
    addEntranceAnimations() {
        const sections = this.form.querySelectorAll('.section-title, .form-group');
        sections.forEach((section, index) => {
            section.style.opacity = '0';
            section.style.transform = 'translateY(20px)';
            setTimeout(() => {
                section.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
                section.style.opacity = '1';
                section.style.transform = 'translateY(0)';
            }, index * 50);
        });
    }
    
    handleFocus(e) {
        const wrapper = e.target.closest('.input-wrapper, .textarea-wrapper');
        if (wrapper) {
            wrapper.classList.add('focused');
            const input = wrapper.querySelector('input, textarea');
            input.style.boxShadow = '0 0 20px rgba(0, 255, 136, 0.1)';
        }
    }
    
    handleBlur(e) {
        const wrapper = e.target.closest('.input-wrapper, .textarea-wrapper');
        if (wrapper) {
            wrapper.classList.remove('focused');
            const input = wrapper.querySelector('input, textarea');
            input.style.boxShadow = '';
        }
    }
    
    // Validation methods
    validateNombre(value) {
        if (!value) {
            return { isValid: false, message: 'El nombre es requerido' };
        }
        if (value.length < 3) {
            return { isValid: false, message: 'El nombre debe tener al menos 3 caracteres' };
        }
        return { isValid: true };
    }
    
    validateTelefono(value) {
        if (!value) {
            return { isValid: false, message: 'El teléfono es requerido' };
        }
        const phoneRegex = /^[0-9]{8,15}$/;
        if (!phoneRegex.test(value.replace(/[\s\-\(\)]/g, ''))) {
            return { isValid: false, message: 'Ingresa un teléfono válido' };
        }
        return { isValid: true };
    }
    
    validateEdad(value) {
        if (!value) {
            return { isValid: false, message: 'La edad es requerida' };
        }
        const edad = parseInt(value);
        if (edad < 16 || edad > 100) {
            return { isValid: false, message: 'La edad debe estar entre 16 y 100 años' };
        }
        return { isValid: true };
    }
    
    validateSelect(value) {
        if (!value) {
            return { isValid: false, message: 'Por favor selecciona una opción' };
        }
        return { isValid: true };
    }
    
    validateRadio(value, field) {
        const radioName = field?.name || value;
        const radios = this.form.querySelectorAll(`input[name="${radioName}"]`);
        const isChecked = Array.from(radios).some(radio => radio.checked);
        
        if (!isChecked) {
            return { isValid: false, message: 'Por favor selecciona una opción' };
        }
        return { isValid: true };
    }
    
    validateTerminos(value, field) {
        const checkbox = field || document.getElementById('terminos');
        if (!checkbox.checked) {
            return { isValid: false, message: 'Debes aceptar los términos y condiciones' };
        }
        return { isValid: true };
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        if (this.isSubmitting) return;
        
        const isValid = this.validateForm();
        
        if (isValid) {
            await this.submitForm();
        } else {
            this.shakeForm();
        }
    }
    
    validateForm() {
        let isValid = true;
        
        Object.keys(this.validators).forEach(fieldName => {
            if (!this.validateField(fieldName)) {
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    validateField(fieldName) {
        const field = document.getElementById(fieldName) || this.form.querySelector(`input[name="${fieldName}"]`);
        const validator = this.validators[fieldName];
        
        if (!validator) return true;
        
        let value;
        if (field && field.type === 'radio') {
            const checkedRadio = this.form.querySelector(`input[name="${fieldName}"]:checked`);
            value = checkedRadio ? checkedRadio.value : '';
        } else if (field) {
            value = field.value?.trim() || '';
        }
        
        const result = validator.call(this, value, field);
        
        if (result.isValid) {
            this.clearError(fieldName);
            this.showSuccess(fieldName);
        } else {
            this.showError(fieldName, result.message);
        }
        
        return result.isValid;
    }
    
    showError(fieldName, message) {
        const field = document.getElementById(fieldName) || this.form.querySelector(`input[name="${fieldName}"]`);
        if (!field) return;
        
        const formGroup = field.closest('.form-group');
        const errorElement = document.getElementById(fieldName + 'Error');
        
        if (formGroup && errorElement) {
            formGroup.classList.add('error');
            errorElement.textContent = message;
            errorElement.classList.add('show');
            
            // Add shake animation
            formGroup.style.animation = 'shake 0.5s ease-in-out';
            setTimeout(() => {
                formGroup.style.animation = '';
            }, 500);
        }
    }
    
    clearError(fieldName) {
        const field = document.getElementById(fieldName) || this.form.querySelector(`input[name="${fieldName}"]`);
        if (!field) return;
        
        const formGroup = field.closest('.form-group');
        const errorElement = document.getElementById(fieldName + 'Error');
        
        if (formGroup && errorElement) {
            formGroup.classList.remove('error');
            errorElement.classList.remove('show');
            setTimeout(() => {
                errorElement.textContent = '';
            }, 300);
        }
    }
    
    showSuccess(fieldName) {
        const field = document.getElementById(fieldName);
        if (!field) return;
        
        const wrapper = field.closest('.input-wrapper, .select-wrapper');
        if (wrapper) {
            wrapper.style.borderColor = 'var(--neon-primary)';
            field.style.boxShadow = '0 0 10px rgba(0, 255, 136, 0.3)';
            setTimeout(() => {
                wrapper.style.borderColor = '';
                field.style.boxShadow = '';
            }, 2000);
        }
    }
    
    shakeForm() {
        const card = document.querySelector('.login-card');
        card.style.animation = 'shake 0.5s ease-in-out';
        card.style.boxShadow = '0 0 30px rgba(255, 0, 128, 0.3)';
        setTimeout(() => {
            card.style.animation = '';
            card.style.boxShadow = '';
        }, 500);
    }
    
    async submitForm() {
        this.isSubmitting = true;
        this.submitBtn.classList.add('loading');
        this.submitBtn.style.boxShadow = '0 0 30px rgba(0, 255, 136, 0.6)';
        
        try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Get form data
            const formData = this.getFormData();
            console.log('Form Data:', formData);
            
            // Show success state
            this.showSuccessMessage();
            
        } catch (error) {
            console.error('Submit error:', error);
            FormUtils.showNotification('Error al enviar el formulario. Intenta nuevamente.', 'error', this.form);
        } finally {
            this.isSubmitting = false;
            this.submitBtn.classList.remove('loading');
            this.submitBtn.style.boxShadow = '';
        }
    }
    
    showSuccessMessage() {
        // Hide form with animation
        this.form.style.opacity = '0';
        this.form.style.transform = 'translateY(-20px) scale(0.95)';
        
        const card = document.querySelector('.login-card');
        card.style.boxShadow = '0 0 50px rgba(0, 255, 136, 0.4)';
        
        setTimeout(() => {
            this.form.style.display = 'none';
            this.successMessage.classList.add('show');
            
            // Simulate redirect
            setTimeout(() => {
                this.resetForm();
            }, 5000);
        }, 300);
    }
    
    resetForm() {
        this.successMessage.classList.remove('show');
        
        setTimeout(() => {
            this.form.style.display = 'block';
            this.form.reset();
            
            // Clear validation states
            Object.keys(this.validators).forEach(fieldName => {
                this.clearError(fieldName);
            });
            
            // Reset form appearance
            this.form.style.opacity = '1';
            this.form.style.transform = 'translateY(0) scale(1)';
            
            const card = document.querySelector('.login-card');
            card.style.boxShadow = '';
            
            // Reset floating labels
            const inputs = this.form.querySelectorAll('input, textarea');
            inputs.forEach(input => {
                input.classList.remove('has-value');
            });
            
            // Reset range value
            const rangeValue = document.getElementById('presupuestoValue');
            if (rangeValue) rangeValue.textContent = '$500';
        }, 300);
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
                if (e.target.closest('#loginForm')) {
                    e.preventDefault();
                    this.handleSubmit(e);
                }
            }
            
            if (e.key === 'Escape') {
                Object.keys(this.validators).forEach(fieldName => {
                    this.clearError(fieldName);
                });
            }
        });
    }
    
    getFormData() {
        const formData = new FormData(this.form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            if (data[key]) {
                if (Array.isArray(data[key])) {
                    data[key].push(value);
                } else {
                    data[key] = [data[key], value];
                }
            } else {
                data[key] = value;
            }
        }
        
        // Add checkboxes that aren't checked
        const checkboxes = this.form.querySelectorAll('input[type="checkbox"]:not(:checked)');
        checkboxes.forEach(cb => {
            if (cb.name && !data[cb.name]) {
                data[cb.name] = false;
            }
        });
        
        return data;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const loginCard = document.querySelector('.login-card');
    if (loginCard) {
        loginCard.style.opacity = '0';
        loginCard.style.transform = 'translateY(30px) scale(0.95)';
        
        setTimeout(() => {
            loginCard.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
            loginCard.style.opacity = '1';
            loginCard.style.transform = 'translateY(0) scale(1)';
        }, 200);
    }
    
    new CompleteForm();
});

// Handle page visibility
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
        const activeElement = document.activeElement;
        if (activeElement && activeElement.tagName !== 'INPUT' && activeElement.tagName !== 'TEXTAREA') {
            const firstInput = document.querySelector('#nombre');
            if (firstInput && !firstInput.value) {
                setTimeout(() => firstInput.focus(), 100);
            }
        }
    }
});
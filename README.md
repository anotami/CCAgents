# VMO Call Center OS 🏢

Este es un ecosistema integral de gestión para **Vendor Management Offices (VMO)** y operaciones de Call Center. El sistema permite gestionar el ciclo de vida completo de una operación BPO, desde la ingesta de datos crudos hasta la toma de decisiones estratégicas.

La aplicación está construida con **Python** y **Streamlit**, diseñada para ser modular, escalable y fácil de usar.

---

## 🚀 Cómo empezar

Cualquiera puede usar este sistema de dos formas:

1. **Datos de Ejemplo:** Dentro del módulo **CORTEX**, puedes generar datos ficticios para probar todos los flujos del sistema de inmediato.
2. **Tus Datos:** Puedes cargar tus propios archivos `.csv` respetando las columnas requeridas en cada sección.

---

## 🔄 El Ciclo de Gestión (9 Fases)

El sistema se divide en 9 agentes que se alimentan entre sí:

1. **CORTEX (Datos):** Ingesta, documentación y validación de fuentes (ACD, QA, CX).
2. **NEXUS (Capacidad):** Cálculo de carga de trabajo, TMO y staffing necesario.
3. **FORGE (Ejecución):** Gestión Intraday (GTR), adherencia y alertas de desvío.
4. **SENTINEL (Calidad):** Monitoreo de KPIs de calidad y detección de errores críticos (RAC).
5. **PULSE (Experiencia):** Análisis de sentimiento y satisfacción del cliente (CSAT).
6. **BLUEPRINT (Procesos):** Diseño y control de cambios en los PCRCs operativos.
7. **LEDGER (Financiero):** Cálculo de facturación, bonos por desempeño y penalidades.
8. **ATLAS (Estrategia):** Consolidación ejecutiva para comités WBR y MBR.
9. **RUICA (Mejora):** Registro de acciones correctivas y actualización de la base de conocimiento.

---

## 🛠️ Instalación Local

Si prefieres correrlo en tu máquina:

1. Clona el repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/vmo-callcenter-os.git](https://github.com/tu-usuario/vmo-callcenter-os.git)

vmo-callcenter-os/                # Raíz de tu repositorio
│
├── app.py                        # Punto de entrada (Menú principal y Home)
├── requirements.txt              # Librerías necesarias (streamlit, pandas, duckdb, etc.)
├── README.md                     # Instrucciones para que otros lo instalen
│
├── .streamlit/                   # Configuración visual de Streamlit
│   └── config.toml               # (Para colores corporativos, ocultar menús, etc.)
│
├── data/                         # La "Memoria Central"
│   ├── mock_data/                # Archivos CSV de prueba para quien lo descargue
│   └── vmo_database.db           # Tu base de datos local (SQLite o DuckDB)
│
├── pages/                        # FRONT-END: El estándar de Streamlit para Multi-Páginas
│   ├── 1_🧠_CORTEX_Ingesta.py
│   ├── 2_⚙️_NEXUS_Capacidad.py
│   ├── 3_🔥_FORGE_Ejecucion.py
│   ├── 4_🛡️_SENTINEL_Calidad.py
│   └── ... (las 9 fases)
│
└── agentes/                      # BACK-END: El "Cerebro" de cada módulo
    ├── __init__.py
    ├── cortex_validador.py       # Lógica de limpieza y guardado en DB
    ├── nexus_forecasting.py      # Fórmulas de Erlang C, cruces de capacidad
    ├── sentinel_qa.py            # Lógica de detección de errores RAC
    └── utils.py                  # Funciones comunes (ej. conexión a la DB, control de "Datos de Ejemplo")

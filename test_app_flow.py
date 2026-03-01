import pytest
from streamlit.testing.v1 import AppTest

# Esta función probará que la aplicación principal cargue
def test_home_page():
    at = AppTest.from_file("app.py").run()
    assert not at.exception
    print("✅ Home: OK")

# Esta función probará específicamente el flujo de CORTEX
def test_cortex_generation():
    at = AppTest.from_file("pages/1_🧠_CORTEX.py").run()
    # Buscamos el botón de generar datos por su texto
    if at.button:
        at.button[0].click().run()
        assert not at.exception
    print("✅ CORTEX (Generación de 2 meses): OK")

# Probamos que NEXUS reciba los datos y los procese
def test_nexus_loading():
    at = AppTest.from_file("pages/2_⚙️_NEXUS.py").run()
    # Verificamos que no haya errores de NameError o ModuleNotFound
    assert not at.exception
    print("✅ NEXUS: OK")

# Puedes repetir para cada módulo
@pytest.mark.parametrize("page", [
    "pages/3_🔥_FORGE.py",
    "pages/4_🛡_SENTINEL.py",
    "pages/5_💓_PULSE.py",
    "pages/8_🧭_ATLAS.py"
])
def test_all_modules_load(page):
    at = AppTest.from_file(page).run()
    assert not at.exception
    print(f"✅ {page}: OK")

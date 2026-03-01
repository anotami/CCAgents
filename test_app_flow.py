import pytest
from streamlit.testing.v1 import AppTest

# Esta función probará que la aplicación principal (INICIO) cargue
def test_home_page():
    at = AppTest.from_file("app.py").run()
    assert not at.exception
    print("Test Home: OK")

# Esta función probará el flujo de CORTEX sin emojis
def test_cortex_generation():
    at = AppTest.from_file("pages/1_CORTEX.py").run()
    # Buscamos el botón de generar datos por su texto o índice
    if at.button:
        at.button[0].click().run()
        assert not at.exception
    print("Test CORTEX (Generacion 2 meses): OK")

# Probamos que NEXUS cargue correctamente
def test_nexus_loading():
    at = AppTest.from_file("pages/2_NEXUS.py").run()
    assert not at.exception
    print("Test NEXUS: OK")

# Prueba masiva para el resto de los módulos
@pytest.mark.parametrize("page", [
    "pages/3_FORGE.py",
    "pages/4_SENTINEL.py",
    "pages/5_PULSE.py",
    "pages/6_BLUEPRINT.py",
    "pages/7_LEDGER.py",
    "pages/8_ATLAS.py",
    "pages/9_RUICA.py"
])
def test_all_modules_load(page):
    at = AppTest.from_file(page).run()
    assert not at.exception
    print(f"Test {page}: OK")

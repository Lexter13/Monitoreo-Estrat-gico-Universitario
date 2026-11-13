@echo off
TITLE Observatorio de Educacion Superior (OES)
COLOR 1F

echo ====================================================================
echo   OBSERVATORIO DE EDUCACION SUPERIOR (OES) - VERSION 2.0
echo   Practica Guiada N. 08 - Ingenieria de Sistemas
echo ====================================================================
echo.

echo [1/3] Verificando interprete Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] No se encontro Python en el PATH del sistema.
    echo Por favor instale Python 3.11 o superior y marque "Add Python to PATH".
    pause
    exit /b 1
)

echo [2/3] Inicializando base de datos SQLite y verificando integridad...
python preparar_datos.py

echo.
echo [3/3] Iniciando aplicacion web en Streamlit...
echo La interfaz se abrira en su navegador en: http://localhost:8501
echo Para detener el observatorio, presione Ctrl + C en esta consola.
echo.

python -m streamlit run app.py

pause


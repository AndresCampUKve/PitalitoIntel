@echo off
echo ===================================================
echo   INSTALADOR QUIRÚRGICO - PITALITO INTEL SCRAPER
echo ===================================================
echo.
echo Este script programará tu computadora para que ejecute 
echo "scraper.py" todos los días a las 6:00 AM en segundo plano.
echo Nunca más tendrás que actualizar los datos a mano.
echo.

:: Obteniendo la ruta absoluta de scraper.py
set SCRAPER_PATH="%~dp0scraper.py"

:: Creando un archivo vbs temporal para ejecutar python de forma invisible (sin consola negra)
echo Set WshShell = CreateObject("WScript.Shell") > "%~dp0run_hidden.vbs"
echo WshShell.Run "python """ ^& %SCRAPER_PATH% ^& """", 0, False >> "%~dp0run_hidden.vbs"

set VBS_PATH="%~dp0run_hidden.vbs"

echo Creando tarea en Windows Task Scheduler (Requiere permisos de Administrador si Windows lo pide)...
schtasks /create /tn "PitalitoIntel_AutoScraper" /tr "wscript.exe %VBS_PATH%" /sc daily /st 06:00 /f

echo.
echo Tarea creada exitosamente. 
echo Tu base de datos en Supabase se actualizará sola cada mañana.
echo Puedes presionar cualquier tecla para salir.
pause >nul

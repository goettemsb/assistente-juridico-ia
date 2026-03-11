@echo off
title Assistente Juridico IA
echo.
echo  ========================================
echo    ASSISTENTE JURIDICO IA - Iniciando...
echo  ========================================
echo.
echo  NAO FECHE ESTA JANELA!
echo.
cd /d "%~dp0"
taskkill /F /IM streamlit.exe >nul 2>&1
timeout /t 2 >nul
start http://localhost:8502
streamlit run app.py --server.port 8502 --server.headless true
pause
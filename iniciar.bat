@echo off
setlocal
pushd "%~dp0"
if errorlevel 1 (
    echo Nao foi possivel acessar a pasta do projeto.
    pause
    exit /b 1
)
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" gerador.py %*
) else (
    python gerador.py %*
)
set "gerador_resultado=%errorlevel%"
echo.
if not "%gerador_resultado%"=="0" echo Falha na execucao. Consulte a mensagem acima e a instalacao no README.
pause
popd
exit /b %gerador_resultado%

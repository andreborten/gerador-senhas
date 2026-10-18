@echo off
setlocal
pushd "%~dp0"
if errorlevel 1 (
    echo Nao foi possivel acessar a pasta do projeto.
    pause
    exit /b 1
)
set "gerador_entrada=interface.py"
if not "%~1"=="" set "gerador_entrada=gerador.py"
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" %gerador_entrada% %*
) else (
    python %gerador_entrada% %*
)
set "gerador_resultado=%errorlevel%"
echo.
if not "%gerador_resultado%"=="0" echo Falha na execucao. Consulte a mensagem acima e a instalacao no README.
pause
popd
exit /b %gerador_resultado%

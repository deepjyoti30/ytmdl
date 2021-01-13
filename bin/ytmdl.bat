@echo off

setlocal
if exist "%~dp0\python.exe" (
    "%~dp0\python" "%~dp0ytmdl" %*
) else (
    "%~dp0..\python" "%~dp0ytmdl" %*
)
endlocal
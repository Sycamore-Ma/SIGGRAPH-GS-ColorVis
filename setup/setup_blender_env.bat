@echo off

set "BLENDER_PATH=D:\Blender Foundation\Blender 4.1"
set "PYTHON_BIN=%BLENDER_PATH%\4.1\python\bin\python.exe"
set "SCRIPT_DIR=%~dp0"

cd /d "%SCRIPT_DIR%\.."

echo Current directory: %cd%
echo Blender Python: %PYTHON_BIN%

call "%PYTHON_BIN%" --version
call "%PYTHON_BIN%" -m pip --version
call "%PYTHON_BIN%" -m ensurepip
call "%PYTHON_BIN%" -m pip install --upgrade pip
call "%PYTHON_BIN%" -m pip install -r setup\requirements_blender.txt

echo.
echo Done.

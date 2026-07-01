@echo off
setlocal enabledelayedexpansion

:: 他证通 Windows 打包 — 参考 pc-upload-software/build_windows.bat
set APP_NAME=TazhengTong
set SCRIPT_DIR=%~dp0..
set BUILD_DIR=%SCRIPT_DIR%\build
set DIST_DIR=%SCRIPT_DIR%\dist
set VENV_DIR=%BUILD_DIR%\venv
set PIP_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple
set PIP_HOST=pypi.tuna.tsinghua.edu.cn
if defined PIP_INDEX_URL set PIP_INDEX=%PIP_INDEX_URL%
if defined PIP_TRUSTED_HOST set PIP_HOST=%PIP_TRUSTED_HOST%

echo ==^> 创建虚拟环境
python -m venv "%VENV_DIR%"
call "%VENV_DIR%\Scripts\activate.bat"

echo ==^> pip 镜像: %PIP_INDEX%
echo ==^> 安装依赖（PySide6 较大，可能需要数分钟）
pip install --upgrade pip -q --retries 10 --timeout 180 -i %PIP_INDEX% --trusted-host %PIP_HOST%
if errorlevel 1 goto pip_failed
pip install pyinstaller -q --retries 10 --timeout 180 -i %PIP_INDEX% --trusted-host %PIP_HOST%
if errorlevel 1 goto pip_failed
pip install -r "%SCRIPT_DIR%\requirements.txt" -q --retries 10 --timeout 180 -i %PIP_INDEX% --trusted-host %PIP_HOST%
if errorlevel 1 goto pip_failed
goto pip_ok
:pip_failed
echo ERROR: pip 安装失败，请检查网络或设置镜像：
echo   set PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
echo   set PIP_TRUSTED_HOST=mirrors.aliyun.com
exit /b 1
:pip_ok

cd /d "%SCRIPT_DIR%"
for /f "delims=" %%V in ('python -c "from cert_extract.version import APP_VERSION; print(APP_VERSION)"') do set VERSION=%%V

echo ==^> PyInstaller 构建 %APP_NAME% v%VERSION%
pyinstaller ^
    --name "%APP_NAME%" ^
    --windowed ^
    --onedir ^
    --noconfirm ^
    --clean ^
    --log-level WARN ^
    --collect-all PySide6 ^
    --collect-all shiboken6 ^
    --hidden-import PySide6.QtCore ^
    --hidden-import PySide6.QtGui ^
    --hidden-import PySide6.QtWidgets ^
    --hidden-import pypdf ^
    --hidden-import openpyxl ^
    --add-data "%SCRIPT_DIR%\version;." ^
    app.py

if exist "dist\%APP_NAME%\%APP_NAME%.exe" (
    powershell -Command "Compress-Archive -Path 'dist\%APP_NAME%' -DestinationPath 'dist\%APP_NAME%_windows_v%VERSION%.zip' -Force"
    echo ==^> 完成: dist\%APP_NAME%\%APP_NAME%.exe
    echo ==^> 压缩包: dist\%APP_NAME%_windows_v%VERSION%.zip
) else (
    echo ERROR: 构建失败
    exit /b 1
)

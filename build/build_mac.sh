#!/usr/bin/env bash
# 他证通 macOS 打包 — 参考 pc-upload-software/build_mac.sh
set -euo pipefail

APP_NAME="TazhengTong"
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$SCRIPT_DIR/build"
DIST_DIR="$SCRIPT_DIR/dist"
VENV_DIR="$BUILD_DIR/venv"

# 默认清华镜像（PySide6 体积大，官方 PyPI 易断线）；可 export PIP_INDEX_URL= 改用官方源
PIP_INDEX="${PIP_INDEX_URL:-https://pypi.tuna.tsinghua.edu.cn/simple}"
PIP_HOST="${PIP_TRUSTED_HOST:-pypi.tuna.tsinghua.edu.cn}"
PIP_OPTS=(--retries 10 --timeout 180 -i "$PIP_INDEX" --trusted-host "$PIP_HOST" -q)

pip_install_retry() {
    local max_attempts=5
    local attempt=1
    while [ "$attempt" -le "$max_attempts" ]; do
        if pip install "$@"; then
            return 0
        fi
        echo "WARN: pip 下载中断，${attempt}/${max_attempts} 次重试..."
        attempt=$((attempt + 1))
        sleep "$((attempt * 2))"
    done
    echo "ERROR: pip 安装失败，请检查网络或更换镜像："
    echo "  export PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/"
    echo "  export PIP_TRUSTED_HOST=mirrors.aliyun.com"
    return 1
}

PYTHON_BIN=""
for py in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$py" &>/dev/null; then
        PYTHON_BIN="$py"
        break
    fi
done
if [ -z "$PYTHON_BIN" ]; then
    echo "ERROR: 需要 Python 3.10+"
    exit 1
fi

echo "==> Python: $($PYTHON_BIN --version)"
echo "==> pip 镜像: $PIP_INDEX"
if [ ! -d "$VENV_DIR" ]; then
    echo "==> 创建虚拟环境 $VENV_DIR"
    "$PYTHON_BIN" -m venv "$VENV_DIR"
else
    echo "==> 复用虚拟环境 $VENV_DIR"
fi
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "==> 升级 pip..."
pip_install_retry --upgrade pip "${PIP_OPTS[@]}"
echo "==> 安装 PyInstaller..."
pip_install_retry pyinstaller "${PIP_OPTS[@]}"
echo "==> 安装项目依赖（PySide6 较大，可能需要数分钟）..."
pip_install_retry -r "$SCRIPT_DIR/requirements.txt" "${PIP_OPTS[@]}"

VERSION=$(python -c "from cert_extract.version import APP_VERSION; print(APP_VERSION)")
cd "$SCRIPT_DIR"

echo "==> PyInstaller 构建 $APP_NAME v$VERSION"
pyinstaller \
    --name "$APP_NAME" \
    --windowed \
    --onedir \
    --noconfirm \
    --clean \
    --log-level WARN \
    --collect-all PySide6 \
    --collect-all shiboken6 \
    --hidden-import PySide6.QtCore \
    --hidden-import PySide6.QtGui \
    --hidden-import PySide6.QtWidgets \
    --hidden-import pypdf \
    --hidden-import openpyxl \
    --add-data "$SCRIPT_DIR/version:." \
    app.py

if [ -d "dist/${APP_NAME}.app" ]; then
    codesign --force --deep -s - "dist/${APP_NAME}.app" 2>/dev/null || true
    ZIP="dist/${APP_NAME}_mac_v${VERSION}.zip"
    ditto -c -k --keepParent "dist/${APP_NAME}.app" "$ZIP"
    echo "==> 完成: dist/${APP_NAME}.app"
    echo "==> 压缩包: $ZIP"
else
    echo "ERROR: 未找到 dist/${APP_NAME}.app"
    exit 1
fi

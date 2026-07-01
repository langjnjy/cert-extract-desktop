"""应用元数据 — 版本号从项目根目录 version 文件读取。"""

from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

APP_NAME = "TazhengTong"
APP_ID = "com.tazhengtong.cert-extract"
COPYRIGHT_HOLDER = "他证通"


def project_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def version_file_path() -> Path:
    return project_root() / "version"


@lru_cache(maxsize=1)
def read_app_version() -> str:
    """读取根目录 version 文件首行；打包后需通过 --add-data 一并打入。"""
    candidates = [
        version_file_path(),
        project_root() / "_internal" / "version",
        Path(__file__).resolve().parent.parent / "version",
    ]
    if getattr(sys, "frozen", False):
        exe = Path(sys.executable).resolve()
        candidates.extend(
            [
                exe.parent.parent / "Resources" / "version",
                exe.parent / "version",
            ]
        )
    seen: set[Path] = set()
    for path in candidates:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            text = line.strip()
            if text and not text.startswith("#"):
                return text
    return "0.0.0"


APP_VERSION = read_app_version()

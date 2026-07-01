"""应用名称 — macOS 菜单栏 / 关于对话框等显示名。"""

from __future__ import annotations

import os
import sys

from PySide6.QtWidgets import QApplication

from cert_extract.version import APP_NAME, APP_VERSION
from ui import i18n


def configure_before_qapplication() -> None:
    """须在 QApplication() 之前调用（开发模式下避免菜单栏显示 Python）。"""
    if sys.platform != "darwin" or getattr(sys, "frozen", False):
        return
    os.environ["QT_MAC_APPLICATION_NAME"] = i18n.t("app_title")


def apply_to(app: QApplication) -> None:
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    refresh_display_name(app)


def refresh_display_name(app: QApplication | None = None) -> None:
    title = i18n.t("app_title")
    target = app or QApplication.instance()
    if target is None:
        return
    target.setApplicationDisplayName(title)
    if sys.platform == "darwin" and not getattr(sys, "frozen", False):
        os.environ["QT_MAC_APPLICATION_NAME"] = title

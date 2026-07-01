"""主窗口 — 应用壳 + 多页面切换。"""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from ui import i18n, theme
from ui.app_identity import refresh_display_name
from ui.app_menu import AppMenu
from ui.nav_bar import NavBar
from ui.pages.cert_extract_page import CertExtractPage
from ui.pages.cert_rename_page import CertRenamePage


def _project_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._root = _project_root()
        self._pages: dict[str, QWidget] = {}
        self._app_menu: AppMenu | None = None
        self._build_ui()
        self.refresh_lang()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self.nav = NavBar()
        self.nav.changed.connect(self._on_nav_changed)
        self.nav.feature_changed.connect(self._on_feature_changed)
        outer.addWidget(self.nav)

        self.stack = QStackedWidget()
        self.stack.setObjectName("contentStack")
        outer.addWidget(self.stack, 1)

        self.page_cert = CertExtractPage(self._root)
        self.page_rename = CertRenamePage(self._root)
        self._pages = {"cert": self.page_cert, "rename": self.page_rename}

        self.stack.addWidget(self.page_cert)
        self.stack.addWidget(self.page_rename)

        self._app_menu = AppMenu(self)

    def refresh_lang(self) -> None:
        self.setWindowTitle(f"{i18n.t('app_title')} — {i18n.t('app_subtitle')}")
        refresh_display_name()
        if self._app_menu:
            self._app_menu.refresh()
        self.nav.refresh()
        self.page_cert.refresh_lang()
        self.page_rename.refresh_lang()

    @Slot()
    def _on_nav_changed(self) -> None:
        QApplication.instance().setStyleSheet(theme.build_stylesheet())
        self.nav.refresh()
        self.refresh_lang()

    @Slot(str)
    def _on_feature_changed(self, key: str) -> None:
        if key == "rename":
            self.page_rename.reset_to_input()
        page = self._pages.get(key)
        if page:
            self.stack.setCurrentWidget(page)

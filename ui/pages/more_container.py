"""更多功能容器 — hub + 子功能页。"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget

from ui.pages.cert_rename_page import CertRenamePage
from ui.pages.more_hub_page import MoreHubPage


class MoreContainer(QWidget):
    def __init__(self, project_root: Path, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._stack = QStackedWidget()
        self.hub = MoreHubPage()
        self.rename_page = CertRenamePage(project_root)
        self._stack.addWidget(self.hub)
        self._stack.addWidget(self.rename_page)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._stack)

        self.hub.feature_opened.connect(self._open_feature)
        self.rename_page.back_requested.connect(self._show_hub)

    def _open_feature(self, key: str) -> None:
        if key == "rename":
            self._stack.setCurrentWidget(self.rename_page)

    def _show_hub(self) -> None:
        self._stack.setCurrentWidget(self.hub)

    def refresh_lang(self) -> None:
        self.hub.refresh_lang()
        self.rename_page.refresh_lang()

    def reset_to_hub(self) -> None:
        self._show_hub()

"""占位页 — 后续功能扩展。"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from ui import i18n


class PlaceholderPage(QWidget):
    def __init__(self, page_key: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.page_key = page_key
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("placeholderCard")
        card.setMaximumWidth(420)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(40, 36, 40, 36)
        cl.setSpacing(12)
        cl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_icon = QLabel("✦")
        self.lbl_icon.setObjectName("placeholderIcon")
        self.lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_title = QLabel()
        self.lbl_title.setObjectName("placeholderTitle")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_desc = QLabel()
        self.lbl_desc.setObjectName("placeholderDesc")
        self.lbl_desc.setWordWrap(True)
        self.lbl_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cl.addWidget(self.lbl_icon)
        cl.addWidget(self.lbl_title)
        cl.addWidget(self.lbl_desc)
        layout.addWidget(card, 0, Qt.AlignmentFlag.AlignCenter)

    def refresh_lang(self) -> None:
        self.lbl_title.setText(i18n.t(f"page_{self.page_key}_title"))
        self.lbl_desc.setText(i18n.t(f"page_{self.page_key}_desc"))

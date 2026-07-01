"""更多功能 — 功能入口 hub。"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ui import i18n


class MoreHubPage(QWidget):
    feature_opened = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 16)
        layout.setSpacing(14)

        self.lbl_hub = QLabel()
        self.lbl_hub.setObjectName("sectionTitle")
        layout.addWidget(self.lbl_hub)

        self.card_rename = self._feature_card("rename")
        layout.addWidget(self.card_rename)
        layout.addStretch()

    def _feature_card(self, feature_key: str) -> QFrame:
        card = QFrame()
        card.setObjectName("featureCard")
        row = QHBoxLayout(card)
        row.setContentsMargins(18, 16, 18, 16)
        row.setSpacing(14)

        text_col = QVBoxLayout()
        text_col.setSpacing(4)
        lbl_title = QLabel()
        lbl_title.setObjectName("featureTitle")
        lbl_desc = QLabel()
        lbl_desc.setObjectName("hintLabel")
        lbl_desc.setWordWrap(True)
        text_col.addWidget(lbl_title)
        text_col.addWidget(lbl_desc)

        btn_open = QPushButton()
        btn_open.setObjectName("actionBtn")
        btn_open.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_open.clicked.connect(lambda: self.feature_opened.emit(feature_key))

        row.addLayout(text_col, 1)
        row.addWidget(btn_open, 0, Qt.AlignmentFlag.AlignVCenter)

        if feature_key == "rename":
            self._rename_title = lbl_title
            self._rename_desc = lbl_desc
            self._rename_btn = btn_open
        return card

    def refresh_lang(self) -> None:
        self.lbl_hub.setText(i18n.t("more_hub_title"))
        self._rename_title.setText(i18n.t("feature_rename_title"))
        self._rename_desc.setText(i18n.t("feature_rename_desc"))
        self._rename_btn.setText(i18n.t("feature_open"))

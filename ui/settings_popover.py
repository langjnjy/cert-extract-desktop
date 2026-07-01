"""设置弹层 — 主题 / 明暗 / 语言。"""

from __future__ import annotations

from typing import Dict

from PySide6.QtCore import QPoint, Qt, Signal, QSize
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui import i18n, theme

_GEAR_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="3"/>
  <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1Z"/>
</svg>"""


def gear_icon(size: int, color: str) -> QIcon:
    svg = _GEAR_SVG.format(color=color)
    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)
    renderer = QSvgRenderer(svg.encode("utf-8"))
    painter = QPainter(pm)
    renderer.render(painter)
    painter.end()
    return QIcon(pm)


class _ChipButton(QPushButton):
    def __init__(self, label: str, parent: QWidget | None = None) -> None:
        super().__init__(label, parent)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("chipBtn", True)


class SettingsPopover(QFrame):
    applied = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setObjectName("settingsPopover")
        self.setMinimumWidth(300)
        self._theme_btns: Dict[str, QPushButton] = {}
        self._mode_btns: Dict[str, QPushButton] = {}
        self._lang_btns: Dict[str, QPushButton] = {}
        self._build()
        self.refresh_text()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(14)

        self.lbl_title = QLabel()
        self.lbl_title.setObjectName("settingsTitle")
        layout.addWidget(self.lbl_title)

        self.lbl_theme = QLabel()
        self.lbl_theme.setObjectName("settingsSection")
        layout.addWidget(self.lbl_theme)

        theme_grid = QGridLayout()
        theme_grid.setSpacing(8)
        for idx, key in enumerate(theme.accent_choices()):
            btn = _ChipButton(i18n.accent_label(key))
            btn.clicked.connect(lambda _=False, k=key: self._pick_theme(k))
            self._theme_btns[key] = btn
            theme_grid.addWidget(btn, idx // 6, idx % 6)
        layout.addLayout(theme_grid)

        self.lbl_appearance = QLabel()
        self.lbl_appearance.setObjectName("settingsSection")
        layout.addWidget(self.lbl_appearance)

        mode_row = QHBoxLayout()
        mode_row.setSpacing(8)
        for key in ("dark", "light"):
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setObjectName("segBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _=False, k=key: self._pick_mode(k))
            self._mode_btns[key] = btn
            mode_row.addWidget(btn)
        layout.addLayout(mode_row)

        self.lbl_language = QLabel()
        self.lbl_language.setObjectName("settingsSection")
        layout.addWidget(self.lbl_language)

        lang_row = QHBoxLayout()
        lang_row.setSpacing(8)
        for key in ("zh", "en"):
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setObjectName("segBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _=False, k=key: self._pick_lang(k))
            self._lang_btns[key] = btn
            lang_row.addWidget(btn)
        layout.addLayout(lang_row)

    def refresh_text(self) -> None:
        self.lbl_title.setText(i18n.t("settings_title"))
        self.lbl_theme.setText(i18n.t("settings_theme"))
        self.lbl_appearance.setText(i18n.t("settings_appearance"))
        self.lbl_language.setText(i18n.t("settings_language"))
        self._mode_btns["dark"].setText(i18n.t("theme_dark"))
        self._mode_btns["light"].setText(i18n.t("theme_light"))
        self._lang_btns["zh"].setText(i18n.t("lang_zh"))
        self._lang_btns["en"].setText(i18n.t("lang_en"))
        for key, btn in self._theme_btns.items():
            btn.setText(i18n.accent_label(key))
        self._sync_checks()

    def _sync_checks(self) -> None:
        cur = theme.current_accent()
        for key, btn in self._theme_btns.items():
            btn.setChecked(key == cur)
        mode = theme.current_mode()
        for key, btn in self._mode_btns.items():
            btn.setChecked(key == mode)
        lang = i18n.current_lang()
        for key, btn in self._lang_btns.items():
            btn.setChecked(key == lang)

    def _pick_theme(self, key: str) -> None:
        theme.set_accent(key)
        self._sync_checks()
        self.applied.emit()

    def _pick_mode(self, key: str) -> None:
        theme.set_mode(key)
        self._sync_checks()
        self.applied.emit()

    def _pick_lang(self, key: str) -> None:
        i18n.set_lang(key)
        self.refresh_text()
        self.applied.emit()

    def popup_at(self, anchor: QWidget) -> None:
        self.refresh_text()
        self.adjustSize()
        btn_bottom = anchor.mapToGlobal(QPoint(0, anchor.height()))
        x = btn_bottom.x() + anchor.width() - self.width()
        y = btn_bottom.y() + 8
        self.move(x, y)
        self.show()


class SettingsButton(QPushButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("settingsBtn")
        self.setFixedSize(38, 38)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_icon()

    def _update_icon(self) -> None:
        color = theme.C.get("FG_SUB", "#94a3b8")
        self.setIcon(gear_icon(20, color))
        self.setIconSize(QSize(20, 20))

    def refresh(self) -> None:
        self._update_icon()
        self.setToolTip(i18n.t("settings_title"))

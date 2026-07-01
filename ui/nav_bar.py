"""顶部导航栏 — 主功能 Tab + 更多功能下拉 / 主题 / 明暗 / 语言。"""

from __future__ import annotations

from typing import Dict, List, Tuple

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui import i18n, theme

DEFAULT_FEATURE = "cert"
# 出现在「更多功能」下拉中的功能（后续在此追加）
MORE_MENU_FEATURES: List[str] = ["rename"]


class NavBar(QFrame):
    changed = Signal()
    feature_changed = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("navBar")
        self._current_feature = DEFAULT_FEATURE
        self._theme_btns: Dict[str, QPushButton] = {}
        self._group_labels: Dict[str, QLabel] = {}
        self._more_menu = QMenu(self)
        self._build()

    def _build(self) -> None:
        root = QHBoxLayout(self)
        root.setContentsMargins(20, 8, 20, 8)
        root.setSpacing(16)

        brand = QVBoxLayout()
        brand.setSpacing(2)
        self.lbl_brand = QLabel()
        self.lbl_brand.setObjectName("navBrand")
        self.lbl_tagline = QLabel()
        self.lbl_tagline.setObjectName("navTagline")
        brand.addWidget(self.lbl_brand)
        brand.addWidget(self.lbl_tagline)
        root.addLayout(brand)

        root.addWidget(self._vline())

        feat_wrap = QWidget()
        feat_lay = QHBoxLayout(feat_wrap)
        feat_lay.setContentsMargins(0, 0, 0, 0)
        feat_lay.setSpacing(6)

        self._primary_btn = QPushButton()
        self._primary_btn.setCheckable(True)
        self._primary_btn.setChecked(True)
        self._primary_btn.setObjectName("navFeatureBtn")
        self._primary_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._primary_btn.clicked.connect(self._on_primary_clicked)
        feat_lay.addWidget(self._primary_btn)

        self._more_btn = QPushButton()
        self._more_btn.setObjectName("navMoreBtn")
        self._more_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._more_btn.clicked.connect(self._show_more_menu)
        feat_lay.addWidget(self._more_btn)

        root.addWidget(feat_wrap)
        root.addStretch(1)

        root.addWidget(self._nav_group("navThemeLabel", self._theme_row()))
        root.addWidget(self._vline())
        root.addWidget(self._nav_group("navModeLabel", self._mode_toggle_row()))
        root.addWidget(self._vline())
        root.addWidget(self._nav_group("navLangLabel", self._lang_toggle_row()))

    def _vline(self) -> QFrame:
        line = QFrame()
        line.setObjectName("navDivider")
        line.setFixedWidth(1)
        line.setFixedHeight(36)
        return line

    def _nav_group(self, label_key: str, row: QWidget) -> QWidget:
        wrap = QWidget()
        lay = QVBoxLayout(wrap)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)
        lbl = QLabel()
        lbl.setObjectName("navGroupLabel")
        self._group_labels[label_key] = lbl
        lay.addWidget(lbl)
        lay.addWidget(row)
        return wrap

    _THEME_DOT = 20

    def _theme_row(self) -> QWidget:
        wrap = QWidget()
        vlay = QVBoxLayout(wrap)
        vlay.setContentsMargins(0, 0, 0, 0)
        vlay.setSpacing(4)
        for row_keys in theme.accent_row_groups():
            row = QWidget()
            lay = QHBoxLayout(row)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.setSpacing(4)
            for key in row_keys:
                btn = QPushButton()
                btn.setCheckable(True)
                btn.setObjectName("navThemeBtn")
                btn.setFixedSize(self._THEME_DOT, self._THEME_DOT)
                btn.setToolTip(i18n.accent_label(key))
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.clicked.connect(lambda _=False, k=key: self._pick_theme(k))
                self._theme_btns[key] = btn
                lay.addWidget(btn)
            vlay.addWidget(row)
        return wrap

    def _mode_toggle_row(self) -> QWidget:
        row = QWidget()
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self._mode_btn = QPushButton()
        self._mode_btn.setObjectName("navToggleBtn")
        self._mode_btn.setFixedWidth(76)
        self._mode_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._mode_btn.clicked.connect(self._toggle_mode)
        lay.addWidget(self._mode_btn)
        return row

    def _lang_toggle_row(self) -> QWidget:
        row = QWidget()
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self._lang_btn = QPushButton()
        self._lang_btn.setObjectName("navToggleBtn")
        self._lang_btn.setFixedWidth(76)
        self._lang_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._lang_btn.clicked.connect(self._toggle_lang)
        lay.addWidget(self._lang_btn)
        return row

    def current_feature(self) -> str:
        return self._current_feature

    def _feature_label(self, key: str) -> str:
        if key == "cert":
            return i18n.t("nav_cert")
        if key == "rename":
            return i18n.t("feature_rename_title")
        return key

    def _more_menu_items(self) -> List[Tuple[str, str]]:
        items: List[Tuple[str, str]] = []
        if self._current_feature != "cert":
            items.append(("cert", i18n.t("nav_cert")))
        for key in MORE_MENU_FEATURES:
            if key != self._current_feature:
                items.append((key, self._feature_label(key)))
        return items

    def _rebuild_more_menu(self) -> None:
        self._more_menu.clear()
        for key, label in self._more_menu_items():
            action = self._more_menu.addAction(label)
            action.triggered.connect(lambda _checked=False, k=key: self._pick_feature(k))

    def _show_more_menu(self) -> None:
        self._rebuild_more_menu()
        if self._more_menu.isEmpty():
            return
        pos = self._more_btn.mapToGlobal(self._more_btn.rect().bottomLeft())
        self._more_menu.popup(pos)

    def _on_primary_clicked(self) -> None:
        self._pick_feature(self._current_feature)

    def _mode_btn_label(self) -> str:
        return i18n.t(
            "theme_toggle_light" if theme.current_mode() == "dark" else "theme_toggle_dark"
        )

    def refresh(self) -> None:
        self.lbl_brand.setText(i18n.t("app_title"))
        self.lbl_tagline.setText(i18n.t("app_subtitle"))
        self._group_labels["navThemeLabel"].setText(i18n.t("settings_theme"))
        self._group_labels["navModeLabel"].setText(i18n.t("settings_appearance"))
        self._group_labels["navLangLabel"].setText(i18n.t("settings_language"))
        self._primary_btn.setText(self._feature_label(self._current_feature))
        self._more_btn.setText(f"{i18n.t('nav_more')}  ▾")
        self._mode_btn.setText(self._mode_btn_label())
        self._lang_btn.setText(i18n.t("lang_toggle"))
        for key, btn in self._theme_btns.items():
            btn.setToolTip(i18n.accent_label(key))
        self._sync_checks()
        self._restyle_theme_dots()

    def _restyle_theme_dots(self) -> None:
        fg = theme.C["FG_PRIMARY"]
        dot = self._THEME_DOT
        radius = dot // 2
        for key, btn in self._theme_btns.items():
            color = theme.theme_preview_color(key)
            checked = theme.current_accent() == key
            border = fg if checked else "transparent"
            btn.setStyleSheet(
                f"QPushButton#navThemeBtn {{ background-color: {color}; border-radius: {radius}px;"
                f" border: 1.5px solid {border}; min-width:{dot}px; max-width:{dot}px;"
                f" min-height:{dot}px; max-height:{dot}px; }}"
                f"QPushButton#navThemeBtn:hover {{ border: 1.5px solid {fg}; }}"
            )
            btn.setChecked(checked)

    def _sync_checks(self) -> None:
        self._primary_btn.setChecked(True)
        for key, btn in self._theme_btns.items():
            btn.setChecked(key == theme.current_accent())

    def _pick_feature(self, key: str) -> None:
        if key == self._current_feature:
            return
        self._current_feature = key
        self._primary_btn.setText(self._feature_label(key))
        self._sync_checks()
        self.feature_changed.emit(key)

    def _pick_theme(self, key: str) -> None:
        theme.set_accent(key)
        self._sync_checks()
        self._restyle_theme_dots()
        self.changed.emit()

    def _toggle_mode(self) -> None:
        theme.set_mode("light" if theme.current_mode() == "dark" else "dark")
        self.refresh()
        self.changed.emit()

    def _toggle_lang(self) -> None:
        i18n.toggle_lang()
        self.refresh()
        self.changed.emit()

    def set_feature(self, key: str) -> None:
        """外部同步当前功能（不重复 emit）。"""
        if key != self._current_feature:
            self._current_feature = key
            self._primary_btn.setText(self._feature_label(key))
            self._sync_checks()

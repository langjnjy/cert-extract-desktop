"""系统菜单栏 — 原生 QMenuBar（macOS 显示在屏幕顶部，暂不承接 NavBar 功能）。"""

from __future__ import annotations

import sys

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QMessageBox

from cert_extract.version import read_app_version
from ui.dialogs.about_dialog import show_about_dialog
from ui import i18n


class AppMenu:
    """为 QMainWindow 挂载测试用菜单栏。"""

    def __init__(self, window: QMainWindow) -> None:
        self._window = window
        self._menus: dict[str, object] = {}
        self._actions: dict[str, QAction] = {}
        self._build()

    def _build(self) -> None:
        bar = self._window.menuBar()
        bar.clear()
        bar.setNativeMenuBar(True)

        file_menu = bar.addMenu("")
        self._menus["file"] = file_menu
        self._add_action(
            "file_test",
            file_menu,
            lambda: self._show_test("file"),
            QKeySequence(),
        )
        file_menu.addSeparator()
        quit_action = self._add_action(
            "quit",
            file_menu,
            self._window.close,
            QKeySequence.StandardKey.Quit,
        )
        quit_action.setMenuRole(QAction.MenuRole.QuitRole)

        edit_menu = bar.addMenu("")
        self._menus["edit"] = edit_menu
        self._add_action(
            "edit_test",
            edit_menu,
            lambda: self._show_test("edit"),
        )

        view_menu = bar.addMenu("")
        self._menus["view"] = view_menu
        self._add_action(
            "view_test",
            view_menu,
            lambda: self._show_test("view"),
        )

        if sys.platform == "darwin":
            window_menu = bar.addMenu("")
            self._menus["window"] = window_menu
            min_action = self._add_action(
                "window_minimize",
                window_menu,
                self._window.showMinimized,
                QKeySequence("Ctrl+M"),
            )
            min_action.setMenuRole(QAction.MenuRole.NoRole)
            zoom_action = self._add_action(
                "window_zoom",
                window_menu,
                self._toggle_zoom,
            )
            zoom_action.setMenuRole(QAction.MenuRole.NoRole)

        help_menu = bar.addMenu("")
        self._menus["help"] = help_menu
        about_action = self._add_action(
            "about",
            help_menu,
            self._show_about,
        )
        about_action.setMenuRole(QAction.MenuRole.AboutRole)

        self.refresh()

    def _add_action(
        self,
        key: str,
        menu,
        slot,
        shortcut: QKeySequence | QKeySequence.StandardKey | None = None,
    ) -> QAction:
        action = QAction("", self._window)
        action.triggered.connect(slot)
        if shortcut is not None:
            action.setShortcut(shortcut)
        menu.addAction(action)
        self._actions[key] = action
        return action

    def refresh(self) -> None:
        self._menus["file"].setTitle(i18n.t("menu_file"))
        self._actions["file_test"].setText(i18n.t("menu_file_test"))
        self._actions["quit"].setText(i18n.t("menu_quit"))

        self._menus["edit"].setTitle(i18n.t("menu_edit"))
        self._actions["edit_test"].setText(i18n.t("menu_edit_test"))

        self._menus["view"].setTitle(i18n.t("menu_view"))
        self._actions["view_test"].setText(i18n.t("menu_view_test"))

        if "window" in self._menus:
            self._menus["window"].setTitle(i18n.t("menu_window"))
            self._actions["window_minimize"].setText(i18n.t("menu_window_minimize"))
            self._actions["window_zoom"].setText(i18n.t("menu_window_zoom"))

        self._menus["help"].setTitle(i18n.t("menu_help"))
        self._actions["about"].setText(i18n.t("menu_about"))

    def _show_test(self, section: str) -> None:
        QMessageBox.information(
            self._window,
            i18n.t("menu_test_title"),
            i18n.t("menu_test_body", section=i18n.t(f"menu_{section}")),
        )

    def _show_about(self) -> None:
        show_about_dialog(self._window)

    def _toggle_zoom(self) -> None:
        if self._window.isMaximized():
            self._window.showNormal()
        else:
            self._window.showMaximized()

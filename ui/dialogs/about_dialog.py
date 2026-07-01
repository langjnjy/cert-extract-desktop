"""关于对话框 — 参考 WPS 关于页布局。"""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from cert_extract.version import APP_NAME, COPYRIGHT_HOLDER, read_app_version
from ui import i18n, theme


class AboutDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("aboutDialog")
        self.setModal(True)
        self.setFixedSize(500, 360)
        self._build_ui()
        self.refresh_text()
        self._apply_style()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 20)
        root.setSpacing(0)

        header = QHBoxLayout()
        header.setSpacing(16)

        self.logo = QLabel()
        self.logo.setObjectName("aboutLogo")
        self.logo.setFixedSize(56, 56)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_col = QVBoxLayout()
        title_col.setSpacing(4)
        self.lbl_app = QLabel()
        self.lbl_app.setObjectName("aboutAppName")
        self.lbl_tagline = QLabel()
        self.lbl_tagline.setObjectName("aboutTagline")
        self.lbl_tagline.setWordWrap(True)
        title_col.addWidget(self.lbl_app)
        title_col.addWidget(self.lbl_tagline)
        header.addWidget(self.logo, 0, Qt.AlignmentFlag.AlignTop)
        header.addLayout(title_col, 1)
        root.addLayout(header)

        root.addSpacing(22)

        version_row = QHBoxLayout()
        version_row.setSpacing(8)
        self.lbl_version = QLabel()
        self.lbl_version.setObjectName("aboutVersion")
        self.btn_check_update = QPushButton()
        self.btn_check_update.setObjectName("aboutLinkBtn")
        self.btn_check_update.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_check_update.setFlat(True)
        self.btn_check_update.clicked.connect(self._on_check_update)
        version_row.addWidget(self.lbl_version)
        version_row.addStretch(1)
        version_row.addWidget(self.btn_check_update)
        root.addLayout(version_row)

        root.addSpacing(14)

        self.lbl_desc = QLabel()
        self.lbl_desc.setObjectName("aboutDesc")
        self.lbl_desc.setWordWrap(True)
        root.addWidget(self.lbl_desc)

        root.addStretch(1)

        sep = QFrame()
        sep.setObjectName("aboutSep")
        sep.setFixedHeight(1)
        root.addWidget(sep)
        root.addSpacing(12)

        self.lbl_copyright = QLabel()
        self.lbl_copyright.setObjectName("aboutCopyright")
        self.lbl_copyright.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.lbl_copyright)

        root.addSpacing(10)

        links = QHBoxLayout()
        links.setSpacing(18)
        links.addStretch(1)
        self.btn_license = self._link_button(self._on_license)
        self.btn_opensource = self._link_button(self._on_opensource)
        links.addWidget(self.btn_license)
        links.addWidget(self.btn_opensource)
        links.addStretch(1)
        root.addLayout(links)

    def _link_button(self, slot) -> QPushButton:
        btn = QPushButton()
        btn.setObjectName("aboutLinkBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFlat(True)
        btn.clicked.connect(slot)
        return btn

    def refresh_text(self) -> None:
        app_title = i18n.t("app_title")
        self.setWindowTitle(i18n.t("menu_about"))
        self.logo.setText(app_title[:1])
        self.lbl_app.setText(app_title)
        self.lbl_tagline.setText(i18n.t("app_subtitle"))
        version = read_app_version()
        self.lbl_version.setText(i18n.t("about_version", version=version))
        self.btn_check_update.setText(i18n.t("about_check_update"))
        self.lbl_desc.setText(i18n.t("about_desc"))
        year = datetime.now().year
        self.lbl_copyright.setText(
            i18n.t(
                "about_copyright",
                year=year,
                holder=COPYRIGHT_HOLDER,
                name=APP_NAME,
            )
        )
        self.btn_license.setText(i18n.t("about_license"))
        self.btn_opensource.setText(i18n.t("about_opensource"))

    def _apply_style(self) -> None:
        c = theme.C
        self.setStyleSheet(
            f"""
            QDialog#aboutDialog {{
                background-color: {c['BG_PANEL']};
            }}
            QLabel#aboutLogo {{
                background-color: {c['ACCENT']};
                color: white;
                border-radius: 14px;
                font-size: 28px;
                font-weight: 700;
            }}
            QLabel#aboutAppName {{
                font-size: 22px;
                font-weight: 700;
                color: {c['FG_PRIMARY']};
                background: transparent;
            }}
            QLabel#aboutTagline {{
                font-size: 12px;
                color: {c['FG_MUTED']};
                background: transparent;
            }}
            QLabel#aboutVersion {{
                font-size: 12px;
                color: {c['FG_SUB']};
                background: transparent;
            }}
            QLabel#aboutDesc {{
                font-size: 11px;
                line-height: 1.5;
                color: {c['FG_MUTED']};
                background: transparent;
            }}
            QFrame#aboutSep {{
                background-color: {c['BORDER']};
                border: none;
            }}
            QLabel#aboutCopyright {{
                font-size: 10px;
                color: {c['FG_MUTED']};
                background: transparent;
            }}
            QPushButton#aboutLinkBtn {{
                color: {c['ACCENT']};
                background: transparent;
                border: none;
                font-size: 11px;
                padding: 0 2px;
                text-decoration: underline;
            }}
            QPushButton#aboutLinkBtn:hover {{
                color: {c['ACCENT_HOVER']};
            }}
            """
        )

    def _on_check_update(self) -> None:
        QMessageBox.information(
            self,
            i18n.t("about_check_update"),
            i18n.t("about_update_latest", version=read_app_version()),
        )

    def _on_license(self) -> None:
        QMessageBox.information(self, i18n.t("about_license"), i18n.t("about_license_body"))

    def _on_opensource(self) -> None:
        QMessageBox.information(self, i18n.t("about_opensource"), i18n.t("about_opensource_body"))


def show_about_dialog(parent: QWidget | None = None) -> None:
    AboutDialog(parent).exec()

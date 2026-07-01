"""批量查找替换对话框。"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)

from ui import i18n


class BulkReplaceDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("bulkReplaceDialog")
        self.setWindowTitle(i18n.t("replace_title"))
        self.setMinimumWidth(380)

        self.lbl_desc = QLabel(i18n.t("replace_desc"))
        self.lbl_desc.setObjectName("hintLabel")
        self.lbl_desc.setWordWrap(True)

        form = QFormLayout()
        self.edit_find = QLineEdit()
        self.edit_replace = QLineEdit()
        form.addRow(i18n.t("replace_find"), self.edit_find)
        form.addRow(i18n.t("replace_with"), self.edit_replace)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText(i18n.t("replace_apply"))
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(i18n.t("replace_cancel"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(self.lbl_desc)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def find_text(self) -> str:
        return self.edit_find.text()

    def replace_text(self) -> str:
        return self.edit_replace.text()

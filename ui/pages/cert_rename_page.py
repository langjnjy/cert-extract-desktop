"""他证 PDF 按坐落重命名页面。"""

from __future__ import annotations

from pathlib import Path
from typing import List, Literal

from PySide6.QtCore import QSize, Qt, QTimer, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from cert_extract.core import pdf_reader
from cert_extract.core.models import RenameItem, RenamePreviewResult
from cert_extract.services.rename_service import apply_renames
from ui import i18n
from ui.dialogs.bulk_replace_dialog import BulkReplaceDialog
from ui.workers import RenamePreviewThread

SourceKind = Literal["none", "folder", "files"]
NEW_NAME_COL = 1


class CertRenamePage(QWidget):
    def __init__(self, project_root: Path, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._root = project_root
        self._thread: RenamePreviewThread | None = None
        self._source_kind: SourceKind = "none"
        self._source_paths: List[Path] = []
        self._preview_items: List[RenameItem] = []
        self._last_elapsed = 0.0
        self._build_ui()
        self._wire_defaults()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(0)

        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_input_page())
        self.stack.addWidget(self._build_preview_page())
        layout.addWidget(self.stack, 1)

    def _build_input_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        source_card = QFrame()
        source_card.setObjectName("sourceCard")
        sl = QVBoxLayout(source_card)
        sl.setContentsMargins(20, 18, 20, 18)
        sl.setSpacing(12)
        self.lbl_source = QLabel()
        self.lbl_source.setObjectName("sectionTitle")
        self.edit_source = QLineEdit()
        self.edit_source.setReadOnly(True)
        self.edit_source.setObjectName("sourceInput")
        pick_row = QHBoxLayout()
        pick_row.setSpacing(12)
        self.btn_pick_folder = QPushButton()
        self.btn_pick_folder.setObjectName("pickBtn")
        self.btn_pick_folder.clicked.connect(self._pick_folder)
        self.btn_pick_file = QPushButton()
        self.btn_pick_file.setObjectName("pickBtn")
        self.btn_pick_file.clicked.connect(self._pick_files)
        pick_row.addWidget(self.btn_pick_folder)
        pick_row.addWidget(self.btn_pick_file)
        pick_row.addStretch()
        self.btn_start = QPushButton()
        self.btn_start.setObjectName("actionBtn")
        self.btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_start.clicked.connect(self._start_preview)
        pick_row.addWidget(self.btn_start)
        sl.addWidget(self.lbl_source)
        sl.addWidget(self.edit_source)
        sl.addLayout(pick_row)

        self.status_card = QFrame()
        self.status_card.setObjectName("statusCard")
        st = QVBoxLayout(self.status_card)
        st.setContentsMargins(0, 4, 0, 0)
        st.setSpacing(6)
        self.lbl_progress = QLabel()
        self.lbl_progress.setObjectName("fieldLabel")
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(8)
        st.addWidget(self.lbl_progress)
        st.addWidget(self.progress)
        sl.addWidget(self.status_card)
        self._set_progress_visible(False)
        layout.addWidget(source_card)
        layout.addStretch()
        return page

    def _build_preview_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        top = QHBoxLayout()
        self.lbl_preview_stats = QLabel()
        self.lbl_preview_stats.setObjectName("previewStats")
        top.addWidget(self.lbl_preview_stats, 1)
        self.btn_reselect = QPushButton()
        self.btn_reselect.setObjectName("ghostBtn")
        self.btn_reselect.clicked.connect(self._back_to_input)
        top.addWidget(self.btn_reselect, 0, Qt.AlignmentFlag.AlignVCenter)
        layout.addLayout(top)

        table_card = QFrame()
        table_card.setObjectName("previewCard")
        tl = QVBoxLayout(table_card)
        tl.setContentsMargins(12, 12, 12, 12)
        self.table = QTableWidget()
        self.table.setObjectName("previewTable")
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked
            | QAbstractItemView.EditTrigger.EditKeyPressed
            | QAbstractItemView.EditTrigger.AnyKeyPressed
        )
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setWordWrap(False)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.table.verticalHeader().setVisible(False)
        header.sectionResized.connect(self._update_new_name_header_pos)
        header.geometriesChanged.connect(self._update_new_name_header_pos)
        header.sectionMoved.connect(self._update_new_name_header_pos)
        self.table.horizontalScrollBar().valueChanged.connect(self._update_new_name_header_pos)
        self.table.verticalScrollBar().valueChanged.connect(self._update_new_name_header_pos)

        self._new_name_header = QWidget(header.viewport())
        self._new_name_header.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self._new_name_header.setObjectName("newNameHeader")
        header_lay = QHBoxLayout(self._new_name_header)
        header_lay.setContentsMargins(10, 0, 8, 0)
        header_lay.setSpacing(6)
        self._lbl_new_name_col = QLabel()
        self._lbl_new_name_col.setObjectName("tableColHeaderLabel")
        self._replace_btn = QToolButton()
        self._replace_btn.setObjectName("replaceIconBtn")
        self._replace_btn.setToolTip(i18n.t("replace_tooltip"))
        self._replace_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._replace_btn.setFixedSize(22, 22)
        self._replace_btn.setAutoRaise(False)
        icon = QIcon.fromTheme("edit-find-replace")
        if not icon.isNull():
            self._replace_btn.setIcon(icon)
            self._replace_btn.setIconSize(QSize(14, 14))
            self._replace_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        else:
            self._replace_btn.setText("A→a")
            self._replace_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self._replace_btn.clicked.connect(self._open_replace_dialog)
        header_lay.addWidget(self._lbl_new_name_col)
        header_lay.addWidget(self._replace_btn)
        header_lay.addStretch()
        self._new_name_header.hide()
        tl.addWidget(self.table)
        layout.addWidget(table_card, 1)

        actions = QHBoxLayout()
        actions.addStretch()
        self.btn_apply = QPushButton()
        self.btn_apply.setObjectName("actionBtn")
        self.btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_apply.clicked.connect(self._apply_rename)
        actions.addWidget(self.btn_apply)
        layout.addLayout(actions)
        self._preview_page = page
        return page

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if self.stack.currentIndex() == 1:
            self._update_new_name_header_pos()

    def _wire_defaults(self) -> None:
        self._clear_source()
        self.stack.setCurrentIndex(0)

    def reset_to_input(self) -> None:
        self.stack.setCurrentIndex(0)
        self._new_name_header.hide()
        self.progress.setValue(0)
        self.lbl_progress.clear()
        self._set_progress_visible(False)

    def _set_progress_visible(self, visible: bool) -> None:
        self.status_card.setVisible(visible)

    def _clear_source(self) -> None:
        self._source_kind = "none"
        self._source_paths = []
        self.edit_source.clear()

    def refresh_lang(self) -> None:
        self.lbl_source.setText(i18n.t("rename_input_source"))
        self.edit_source.setPlaceholderText(i18n.t("input_placeholder"))
        self.btn_pick_folder.setText(i18n.t("pick_folder"))
        self.btn_pick_file.setText(i18n.t("pick_pdf"))
        self.btn_start.setText(i18n.t("rename_preview"))
        self.btn_reselect.setText(i18n.t("back_to_input"))
        self.btn_apply.setText(i18n.t("rename_apply"))
        self._lbl_new_name_col.setText(i18n.t("rename_col_new"))
        self._replace_btn.setToolTip(i18n.t("replace_tooltip"))
        self._refresh_source_display()
        self._refresh_preview_headers()
        if self._preview_items and self.stack.currentIndex() == 1:
            self._refresh_preview_stats(self._last_elapsed)

    def _refresh_preview_headers(self) -> None:
        headers = i18n.rename_preview_headers()
        if self.table.columnCount() != len(headers):
            return
        for col, label in enumerate(headers):
            if col == NEW_NAME_COL:
                self.table.setHorizontalHeaderItem(col, QTableWidgetItem(""))
            else:
                self.table.setHorizontalHeaderItem(col, QTableWidgetItem(label))
        self._lbl_new_name_col.setText(i18n.t("rename_col_new"))

    def _refresh_source_display(self) -> None:
        if self._source_kind == "none" or not self._source_paths:
            self.edit_source.clear()
            return
        if self._source_kind == "folder":
            self.edit_source.setText(str(self._source_paths[0]))
        elif len(self._source_paths) == 1:
            self.edit_source.setText(str(self._source_paths[0]))
        else:
            self.edit_source.setText(i18n.t("files_selected", count=len(self._source_paths)))

    def _pick_folder(self) -> None:
        from PySide6.QtWidgets import QFileDialog

        start = str(self._source_paths[0].parent) if self._source_paths else str(self._root)
        path = QFileDialog.getExistingDirectory(self, i18n.t("pick_folder"), start)
        if path:
            self._source_kind = "folder"
            self._source_paths = [Path(path)]
            self._refresh_source_display()

    def _pick_files(self) -> None:
        from PySide6.QtWidgets import QFileDialog

        start = str(self._source_paths[0].parent) if self._source_paths else str(self._root)
        paths, _ = QFileDialog.getOpenFileNames(self, i18n.t("pick_pdf"), start, "PDF (*.pdf)")
        if paths:
            self._source_kind = "files"
            self._source_paths = [Path(p) for p in paths]
            self._refresh_source_display()

    @staticmethod
    def _readonly_cell(text: str) -> QTableWidgetItem:
        item = QTableWidgetItem(text)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        return item

    @staticmethod
    def _editable_cell(text: str) -> QTableWidgetItem:
        return QTableWidgetItem(text)

    def _status_text(self, item: RenameItem) -> str:
        if item.error == "no_text_layer":
            return i18n.t("rename_err_no_text")
        if item.error == "no_location" or item.error == "no_building_unit":
            return i18n.t("rename_err_no_location")
        if item.error:
            return item.error
        if item.applied and item.message == "unchanged":
            return i18n.t("rename_status_unchanged")
        if item.applied:
            return i18n.t("rename_status_ok")
        return i18n.t("rename_status_ready")

    @staticmethod
    def _display_new_filename(stem: str) -> str:
        name = stem.strip()
        if not name:
            return ""
        return name if name.lower().endswith(".pdf") else f"{name}.pdf"

    @staticmethod
    def _stem_from_display(text: str) -> str:
        stem = text.strip()
        if stem.lower().endswith(".pdf"):
            return stem[:-4]
        return stem

    def _fit_columns_for_scroll(self) -> None:
        """按内容设列宽一次，保留横向滚动、单行显示。"""
        fm = self.table.fontMetrics()
        padding = 28
        header = self.table.horizontalHeader()
        for col in range(self.table.columnCount()):
            max_w = 80
            if col == NEW_NAME_COL:
                label_w = fm.horizontalAdvance(self._lbl_new_name_col.text()) + 40
                max_w = max(max_w, label_w)
            else:
                header_item = self.table.horizontalHeaderItem(col)
                if header_item and header_item.text():
                    max_w = max(max_w, fm.horizontalAdvance(header_item.text()) + padding)
            for row in range(self.table.rowCount()):
                item = self.table.item(row, col)
                if item:
                    max_w = max(max_w, fm.horizontalAdvance(item.text()) + padding)
            self.table.setColumnWidth(col, max_w)

    def _update_new_name_header_pos(self) -> None:
        if not self._new_name_header.isVisible():
            return
        header = self.table.horizontalHeader()
        if header.count() <= NEW_NAME_COL:
            return
        viewport = header.viewport()
        if viewport is None:
            return
        x = header.sectionViewportPosition(NEW_NAME_COL)
        w = header.sectionSize(NEW_NAME_COL)
        h = viewport.height()
        self._new_name_header.setGeometry(x, 0, w, max(h, 1))
        self._new_name_header.raise_()

    def _open_replace_dialog(self) -> None:
        dialog = BulkReplaceDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        find_text = dialog.find_text()
        if not find_text:
            QMessageBox.warning(self, i18n.t("replace_title"), i18n.t("replace_empty_find"))
            return
        rows = self._bulk_replace_new_names(find_text, dialog.replace_text())
        QMessageBox.information(
            self, i18n.t("replace_title"), i18n.t("replace_done", rows=rows)
        )

    def _bulk_replace_new_names(self, find_text: str, replace_text: str) -> int:
        """一次性替换「新文件名」列所有单元格中的匹配文字。"""
        rows_changed = 0
        for row in range(self.table.rowCount()):
            item = self.table.item(row, NEW_NAME_COL)
            if not item:
                continue
            text = item.text()
            if find_text not in text:
                continue
            item.setText(text.replace(find_text, replace_text))
            rows_changed += 1
        return rows_changed

    def _refresh_preview_stats(self, elapsed: float) -> None:
        ok = sum(1 for i in self._preview_items if i.new_stem.strip())
        fail = len(self._preview_items) - ok
        self.lbl_preview_stats.setText(
            i18n.t("rename_preview_stats", total=len(self._preview_items), ok=ok, fail=fail, seconds=elapsed)
        )

    def _show_preview(self, result: RenamePreviewResult) -> None:
        self._preview_items = list(result.items)
        self._last_elapsed = result.elapsed_seconds
        headers = i18n.rename_preview_headers()
        self.table.clear()
        self.table.setColumnCount(len(headers))
        for col, label in enumerate(headers):
            if col == NEW_NAME_COL:
                self.table.setHorizontalHeaderItem(col, QTableWidgetItem(""))
            else:
                self.table.setHorizontalHeaderItem(col, QTableWidgetItem(label))
        self._lbl_new_name_col.setText(i18n.t("rename_col_new"))
        self.table.setRowCount(len(self._preview_items))

        for row, item in enumerate(self._preview_items):
            self.table.setItem(row, 0, self._readonly_cell(item.source_path.name))
            self.table.setItem(row, 1, self._editable_cell(self._display_new_filename(item.new_stem)))
            self.table.setItem(row, 2, self._readonly_cell(item.location or "—"))
            self.table.setItem(row, 3, self._readonly_cell(self._status_text(item)))

        self._fit_columns_for_scroll()
        self._refresh_preview_stats(result.elapsed_seconds)
        self.btn_apply.setEnabled(any(i.new_stem.strip() for i in self._preview_items))
        self._new_name_header.show()
        self._update_new_name_header_pos()
        QTimer.singleShot(0, self._update_new_name_header_pos)
        self.stack.setCurrentIndex(1)

    def _sync_items_from_table(self) -> None:
        for row, item in enumerate(self._preview_items):
            cell = self.table.item(row, 1)
            item.new_stem = self._stem_from_display(cell.text() if cell else "")
            if item.new_stem:
                item.error = ""
                if item.source in ("", "no_match"):
                    item.source = "manual"
            self.table.setItem(row, 3, self._readonly_cell(self._status_text(item)))

    @Slot()
    def _back_to_input(self) -> None:
        self._new_name_header.hide()
        self.stack.setCurrentIndex(0)
        self.progress.setValue(0)
        self.lbl_progress.clear()
        self._set_progress_visible(False)

    @Slot()
    def _start_preview(self) -> None:
        if not pdf_reader.available():
            QMessageBox.critical(self, i18n.t("error_title"), i18n.t("missing_pdf_lib"))
            return
        if not self._source_paths:
            QMessageBox.warning(self, i18n.t("error_title"), i18n.t("no_source"))
            return

        self.btn_start.setEnabled(False)
        self.btn_start.setText(i18n.t("running"))
        self.progress.setValue(0)
        self.lbl_progress.setText(i18n.t("running"))
        self._set_progress_visible(True)

        thread = RenamePreviewThread(sources=self._source_paths)
        thread.progress.connect(self._on_progress)
        thread.finished.connect(self._on_preview_finished)
        thread.failed.connect(self._on_failed)
        thread.finished.connect(thread.deleteLater)
        self._thread = thread
        thread.start()

    @Slot(int, int, str)
    def _on_progress(self, current: int, total: int, name: str) -> None:
        pct = int(current / total * 100) if total else 0
        self.progress.setValue(pct)
        if name:
            self.lbl_progress.setText(i18n.t("progress_fmt", current=current, total=total, dir=name))
        elif total:
            self.lbl_progress.setText(i18n.t("progress_starting", total=total))
        else:
            self.lbl_progress.setText(i18n.t("running"))

    @Slot(object)
    def _on_preview_finished(self, result: RenamePreviewResult) -> None:
        self.btn_start.setEnabled(True)
        self.btn_start.setText(i18n.t("rename_preview"))
        self._set_progress_visible(False)

        if not result.items:
            QMessageBox.warning(self, i18n.t("error_title"), i18n.t("no_records"))
            return

        self._show_preview(result)

    @Slot(str)
    def _on_failed(self, message: str) -> None:
        self.btn_start.setEnabled(True)
        self.btn_start.setText(i18n.t("rename_preview"))
        self._set_progress_visible(False)
        self.lbl_progress.clear()
        if message == "missing_pdf_library":
            message = i18n.t("missing_pdf_lib")
        QMessageBox.critical(self, i18n.t("error_title"), message)

    @Slot()
    def _apply_rename(self) -> None:
        self._sync_items_from_table()
        ok_items = [
            i for i in self._preview_items if i.new_stem.strip() and not i.applied
        ]
        if not ok_items:
            QMessageBox.information(self, i18n.t("rename_apply_title"), i18n.t("rename_nothing_to_apply"))
            return

        reply = QMessageBox.question(
            self,
            i18n.t("rename_apply_title"),
            i18n.t("rename_apply_confirm", count=len(ok_items)),
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        updated = apply_renames(self._preview_items)
        self._preview_items = updated
        renamed = sum(1 for i in updated if i.applied and i.message == "renamed")
        unchanged = sum(1 for i in updated if i.applied and i.message == "unchanged")
        failed = sum(1 for i in updated if i.error)

        for row, item in enumerate(self._preview_items):
            self.table.setItem(row, 0, self._readonly_cell(item.source_path.name))
            self.table.setItem(row, 1, self._editable_cell(self._display_new_filename(item.new_stem)))
            self.table.setItem(row, 3, self._readonly_cell(self._status_text(item)))

        self.btn_apply.setEnabled(False)
        QMessageBox.information(
            self,
            i18n.t("rename_apply_title"),
            i18n.t("rename_apply_done", renamed=renamed, unchanged=unchanged, failed=failed),
        )

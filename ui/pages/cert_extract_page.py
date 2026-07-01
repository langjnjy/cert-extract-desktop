"""他证 PDF 提取页面 — 选择来源 → 提取预览 → 导出 Excel。"""

from __future__ import annotations

from pathlib import Path
from typing import List, Literal

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
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
    QVBoxLayout,
    QWidget,
)

from cert_extract.core import pdf_reader
from cert_extract.core.excel_writer import write_excel
from cert_extract.core.models import ExtractRecord, ExtractResult
from ui import i18n
from ui.workers import ExtractThread

SourceKind = Literal["none", "folder", "files"]


class CertExtractPage(QWidget):
    """他证信息提取 — 当前已实现功能。"""

    def __init__(self, project_root: Path, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._root = project_root
        self._thread: ExtractThread | None = None
        self._source_kind: SourceKind = "none"
        self._source_paths: List[Path] = []
        self._preview_records: List[ExtractRecord] = []
        self._export_label = "extract"
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
        self.btn_start.clicked.connect(self._start)
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
        top.setSpacing(12)
        self.lbl_preview_stats = QLabel()
        self.lbl_preview_stats.setObjectName("previewStats")
        top.addWidget(self.lbl_preview_stats, 1)
        self.btn_back = QPushButton()
        self.btn_back.setObjectName("ghostBtn")
        self.btn_back.setMinimumWidth(96)
        self.btn_back.clicked.connect(self._back_to_input)
        top.addWidget(self.btn_back, 0, Qt.AlignmentFlag.AlignVCenter)
        layout.addLayout(top)

        table_card = QFrame()
        table_card.setObjectName("previewCard")
        tl = QVBoxLayout(table_card)
        tl.setContentsMargins(12, 12, 12, 12)
        tl.setSpacing(0)
        self.table = QTableWidget()
        self.table.setObjectName("previewTable")
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked
            | QAbstractItemView.EditTrigger.EditKeyPressed
            | QAbstractItemView.EditTrigger.AnyKeyPressed
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.verticalHeader().setVisible(False)
        tl.addWidget(self.table)
        layout.addWidget(table_card, 1)

        actions = QHBoxLayout()
        actions.setSpacing(12)
        actions.addStretch()
        self.btn_export = QPushButton()
        self.btn_export.setObjectName("actionBtn")
        self.btn_export.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_export.clicked.connect(self._export_excel)
        actions.addWidget(self.btn_export)
        layout.addLayout(actions)
        return page

    def _wire_defaults(self) -> None:
        self._clear_source()
        self.stack.setCurrentIndex(0)

    def _clear_source(self) -> None:
        self._source_kind = "none"
        self._source_paths = []
        self.edit_source.clear()

    def _set_progress_visible(self, visible: bool) -> None:
        self.status_card.setVisible(visible)

    def refresh_lang(self) -> None:
        self.lbl_source.setText(i18n.t("input_source"))
        self.edit_source.setPlaceholderText(i18n.t("input_placeholder"))
        self.btn_pick_folder.setText(i18n.t("pick_folder"))
        self.btn_pick_file.setText(i18n.t("pick_pdf"))
        self.btn_start.setText(i18n.t("start"))
        self.btn_back.setText(i18n.t("back_to_input"))
        self.btn_export.setText(i18n.t("export_excel"))
        if not self._thread or not self._thread.isRunning():
            if self.stack.currentIndex() == 0 and not self.status_card.isVisible():
                self.lbl_progress.clear()
        self._refresh_source_display()
        self._refresh_preview_headers()
        if self._preview_records and self.stack.currentIndex() == 1:
            self._refresh_preview_stats(self._last_elapsed)

    def _refresh_preview_headers(self) -> None:
        headers = i18n.excel_headers()
        if self.table.columnCount() == len(headers):
            self.table.setHorizontalHeaderLabels(headers)

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
        start = str(self._source_paths[0].parent) if self._source_paths else str(self._root)
        path = QFileDialog.getExistingDirectory(self, i18n.t("pick_folder"), start)
        if path:
            self._source_kind = "folder"
            self._source_paths = [Path(path)]
            self._refresh_source_display()

    def _pick_files(self) -> None:
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
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item

    @staticmethod
    def _editable_cell(text: str) -> QTableWidgetItem:
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item

    def _refresh_preview_stats(self, elapsed: float) -> None:
        ok = sum(1 for r in self._preview_records if r.ok)
        fail = len(self._preview_records) - ok
        self.lbl_preview_stats.setText(
            i18n.t(
                "preview_stats",
                total=len(self._preview_records),
                ok=ok,
                fail=fail,
                seconds=elapsed,
            )
        )

    def _show_preview(self, result: ExtractResult) -> None:
        self._preview_records = list(result.records)
        self._export_label = result.source_label or i18n.t("multi_file_excel")
        self._last_elapsed = result.elapsed_seconds
        headers = i18n.excel_headers()
        self.table.clear()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(self._preview_records))

        for row, record in enumerate(self._preview_records):
            self.table.setItem(row, 0, self._readonly_cell(str(row + 1)))
            self.table.setItem(row, 1, self._editable_cell(record.rights_holder))
            self.table.setItem(row, 2, self._editable_cell(record.location))
            self.table.setItem(row, 3, self._editable_cell(record.property_right_certificate_no))
            self.table.setItem(row, 4, self._editable_cell(record.original_property_certificate_no))
            self.table.setItem(row, 5, self._editable_cell(record.property_certificate_no))

        self.table.resizeColumnsToContents()
        self._refresh_preview_stats(result.elapsed_seconds)
        self.stack.setCurrentIndex(1)

    def _records_from_table(self) -> List[ExtractRecord]:
        records: List[ExtractRecord] = []
        for row in range(self.table.rowCount()):
            base = self._preview_records[row] if row < len(self._preview_records) else ExtractRecord(filename="")

            def cell(col: int) -> str:
                item = self.table.item(row, col)
                return item.text().strip() if item else ""

            records.append(
                ExtractRecord(
                    filename=base.filename,
                    rights_holder=cell(1),
                    location=cell(2),
                    property_right_certificate_no=cell(3),
                    original_property_certificate_no=cell(4),
                    property_certificate_no=cell(5),
                    error=base.error,
                )
            )
        return records

    @Slot()
    def _back_to_input(self) -> None:
        self.stack.setCurrentIndex(0)
        self.progress.setValue(0)
        self.lbl_progress.clear()
        self._set_progress_visible(False)

    @Slot()
    def _start(self) -> None:
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

        thread = ExtractThread(sources=self._source_paths)
        thread.progress.connect(self._on_progress)
        thread.finished.connect(self._on_finished)
        thread.failed.connect(self._on_failed)
        thread.finished.connect(thread.deleteLater)
        self._thread = thread
        thread.start()

    @Slot(int, int, str)
    def _on_progress(self, current: int, total: int, name: str) -> None:
        pct = int(current / total * 100) if total else 0
        self.progress.setValue(pct)
        if name:
            self.lbl_progress.setText(
                i18n.t("progress_fmt", current=current, total=total, dir=name)
            )
        elif total:
            self.lbl_progress.setText(i18n.t("progress_starting", total=total))
        else:
            self.lbl_progress.setText(i18n.t("running"))

    @Slot(object)
    def _on_finished(self, result: ExtractResult) -> None:
        self.btn_start.setEnabled(True)
        self.btn_start.setText(i18n.t("start"))
        self.progress.setValue(100)

        if not result.records:
            self._set_progress_visible(False)
            self.lbl_progress.clear()
            QMessageBox.warning(self, i18n.t("error_title"), i18n.t("no_records"))
            return

        self._set_progress_visible(False)
        self._show_preview(result)
        if result.failed_count:
            QMessageBox.information(self, i18n.t("preview_title"), i18n.t("scan_warning"))

    @Slot(str)
    def _on_failed(self, message: str) -> None:
        self.btn_start.setEnabled(True)
        self.btn_start.setText(i18n.t("start"))
        self._set_progress_visible(False)
        self.lbl_progress.clear()
        if message == "missing_pdf_library":
            message = i18n.t("missing_pdf_lib")
        QMessageBox.critical(self, i18n.t("error_title"), message)

    @Slot()
    def _export_excel(self) -> None:
        if self.table.rowCount() == 0:
            return

        default_name = f"{self._export_label}.xlsx"
        start_dir = str(self._root)
        path, _ = QFileDialog.getSaveFileName(
            self,
            i18n.t("save_excel_title"),
            str(Path(start_dir) / default_name),
            i18n.t("save_excel_filter"),
        )
        if not path:
            return
        if not path.lower().endswith(".xlsx"):
            path += ".xlsx"

        records = self._records_from_table()
        try:
            write_excel(records, Path(path), i18n.excel_headers())
        except Exception as exc:
            QMessageBox.critical(self, i18n.t("error_title"), str(exc))
            return

        QMessageBox.information(
            self,
            i18n.t("export_success_title"),
            i18n.t("export_success_body", path=path),
        )

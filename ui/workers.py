"""后台提取线程（仅解析，不写 Excel）。"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from PySide6.QtCore import QThread, Signal

from cert_extract.core.constants import DEFAULT_WORKERS
from cert_extract.core.models import ExtractResult, RenamePreviewResult
from cert_extract.services.batch_service import extract_sources
from cert_extract.services.rename_service import preview_renames


class ExtractThread(QThread):
    progress = Signal(int, int, str)
    finished = Signal(object)
    failed = Signal(str)

    def __init__(
        self,
        sources: Sequence[Path],
        max_workers: int = DEFAULT_WORKERS,
    ) -> None:
        super().__init__()
        self.sources = list(sources)
        self.max_workers = max_workers

    def run(self) -> None:
        try:
            result: ExtractResult = extract_sources(
                sources=self.sources,
                max_workers=self.max_workers,
                on_progress=lambda c, t, d: self.progress.emit(c, t, d),
            )
            self.finished.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))


class RenamePreviewThread(QThread):
    progress = Signal(int, int, str)
    finished = Signal(object)
    failed = Signal(str)

    def __init__(
        self,
        sources: Sequence[Path],
        max_workers: int = DEFAULT_WORKERS,
    ) -> None:
        super().__init__()
        self.sources = list(sources)
        self.max_workers = max_workers

    def run(self) -> None:
        try:
            result: RenamePreviewResult = preview_renames(
                sources=self.sources,
                max_workers=self.max_workers,
                on_progress=lambda c, t, d: self.progress.emit(c, t, d),
            )
            self.finished.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))

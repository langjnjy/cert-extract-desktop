from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class ExtractRecord:
    filename: str
    rights_holder: str = ""
    location: str = ""
    property_right_certificate_no: str = ""
    original_property_certificate_no: str = ""
    property_certificate_no: str = ""
    error: str = ""

    @property
    def ok(self) -> bool:
        return not self.error and bool(self.location or self.property_certificate_no)


@dataclass
class JobResult:
    directory_name: str
    excel_path: Optional[Path]
    pdf_count: int
    records: List[ExtractRecord] = field(default_factory=list)
    elapsed_seconds: float = 0.0

    @property
    def success_count(self) -> int:
        return sum(1 for r in self.records if r.ok)

    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.records if not r.ok)


@dataclass
class ExtractResult:
    """仅提取、不写 Excel（供 GUI 预览）。"""
    records: List[ExtractRecord] = field(default_factory=list)
    source_label: str = ""
    elapsed_seconds: float = 0.0

    @property
    def pdf_count(self) -> int:
        return len(self.records)

    @property
    def success_count(self) -> int:
        return sum(1 for r in self.records if r.ok)

    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.records if not r.ok)


@dataclass
class RenameItem:
    source_path: Path
    location: str = ""
    new_stem: str = ""
    source: str = ""
    error: str = ""
    applied: bool = False
    message: str = ""

    @property
    def ok(self) -> bool:
        return bool(self.new_stem.strip()) and not self.error

    @property
    def new_filename(self) -> str:
        return f"{self.new_stem}.pdf" if self.new_stem else ""


@dataclass
class RenamePreviewResult:
    items: List[RenameItem] = field(default_factory=list)
    elapsed_seconds: float = 0.0

    @property
    def success_count(self) -> int:
        return sum(1 for i in self.items if i.ok)

    @property
    def failed_count(self) -> int:
        return sum(1 for i in self.items if not i.ok)

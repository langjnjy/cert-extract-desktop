"""他证 PDF 重命名 — 多来源推断 + 预览确认。"""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Set

from cert_extract.core import pdf_reader
from cert_extract.core.constants import DEFAULT_WORKERS
from cert_extract.core.models import RenameItem, RenamePreviewResult
from cert_extract.core.parsers import derive_rename_stem
from cert_extract.services.batch_service import collect_all_pdfs

ProgressCallback = Callable[[int, int, str], None]


def collect_pdf_paths(sources: Sequence[Path]) -> List[Path]:
    pdfs: List[Path] = []
    for source in sources:
        resolved = source.resolve()
        if resolved.is_file() and resolved.suffix.lower() == ".pdf":
            pdfs.append(resolved)
            continue
        if not resolved.is_dir():
            continue
        current, subdirs = collect_all_pdfs(resolved)
        if subdirs:
            for name in sorted(subdirs):
                pdfs.extend(p.resolve() for p in subdirs[name])
        elif current:
            pdfs.extend(p.resolve() for p in current)
        else:
            pdfs.extend(p.resolve() for p in sorted(resolved.rglob("*.pdf")))
    return sorted({p for p in pdfs}, key=lambda p: p.name.lower())


def parse_rename_item(pdf_path: Path) -> RenameItem:
    try:
        new_stem, reference, source = derive_rename_stem(pdf_path)
        if new_stem:
            return RenameItem(
                source_path=pdf_path,
                location=reference,
                new_stem=new_stem,
                source=source,
            )

        text = pdf_reader.extract_text(pdf_path)
        if not text or not text.strip():
            return RenameItem(
                source_path=pdf_path,
                location=reference,
                source=source,
                error="no_text_layer",
            )

        new_stem, reference, source = derive_rename_stem(pdf_path, text)
        if new_stem:
            return RenameItem(
                source_path=pdf_path,
                location=reference,
                new_stem=new_stem,
                source=source,
            )

        return RenameItem(
            source_path=pdf_path,
            location=reference,
            source=source,
            error="no_location",
        )
    except Exception as exc:
        return RenameItem(source_path=pdf_path, error=str(exc))


def preview_renames(
    sources: Sequence[Path],
    max_workers: int = DEFAULT_WORKERS,
    on_progress: Optional[ProgressCallback] = None,
) -> RenamePreviewResult:
    if not pdf_reader.available():
        raise RuntimeError("missing_pdf_library")

    pdfs = collect_pdf_paths(sources)
    total = len(pdfs)
    items: List[RenameItem] = []
    t0 = time.time()

    if on_progress and total:
        on_progress(0, total, "")

    if not pdfs:
        return RenamePreviewResult(items=[], elapsed_seconds=0.0)

    if len(pdfs) <= 2:
        for idx, pdf_path in enumerate(pdfs, start=1):
            items.append(parse_rename_item(pdf_path))
            if on_progress:
                on_progress(idx, total, pdf_path.name)
    else:
        indexed: List[tuple[int, RenameItem]] = []
        done = 0
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {
                pool.submit(parse_rename_item, pdf_path): (idx, pdf_path)
                for idx, pdf_path in enumerate(pdfs)
            }
            for future in as_completed(futures):
                idx, pdf_path = futures[future]
                indexed.append((idx, future.result()))
                done += 1
                if on_progress:
                    on_progress(done, total, pdf_path.name)
        indexed.sort(key=lambda pair: pair[0])
        items = [item for _, item in indexed]

    return RenamePreviewResult(items=items, elapsed_seconds=time.time() - t0)


def _unique_target(path: Path, stem: str, taken: Set[Path]) -> Path:
    candidate = path.parent / f"{stem}.pdf"
    if candidate not in taken:
        return candidate
    suffix = 2
    while True:
        alt = path.parent / f"{stem}_{suffix}.pdf"
        if alt not in taken:
            return alt
        suffix += 1


def apply_renames(items: Sequence[RenameItem]) -> List[RenameItem]:
    taken: Set[Path] = set()
    results: List[RenameItem] = []

    for item in items:
        stem = item.new_stem.strip()
        if not stem:
            results.append(item)
            continue
        item.new_stem = stem

        source = item.source_path.resolve()
        target = source.parent / f"{stem}.pdf"
        if source.name == target.name:
            item.applied = True
            item.message = "unchanged"
            item.error = ""
            taken.add(source)
            results.append(item)
            continue

        if target.exists() and target.resolve() != source:
            target = _unique_target(source, stem, taken)

        if target in taken:
            target = _unique_target(source, stem, taken)

        try:
            source.rename(target)
            item.applied = True
            item.message = "renamed"
            item.error = ""
            item.source_path = target
            taken.add(target)
        except OSError as exc:
            item.error = str(exc)
            item.message = "failed"
        results.append(item)

    return results

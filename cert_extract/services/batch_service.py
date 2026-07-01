"""批量提取编排。"""

from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from cert_extract.core.constants import DEFAULT_WORKERS
from cert_extract.core.excel_writer import write_excel
from cert_extract.core.models import ExtractRecord, ExtractResult, JobResult
from cert_extract.core.parsers import (
    extract_location,
    extract_original_mortgage_cert,
    extract_property_certificate_no,
    extract_property_right_certificate_no,
    extract_rights_holder,
)
from cert_extract.core import pdf_reader

logger = logging.getLogger(__name__)

ProgressCallback = Callable[[int, int, str], None]
ItemDoneCallback = Callable[[Path], None]


def _empty_record(filename: str, error: str = "") -> ExtractRecord:
    return ExtractRecord(filename=filename, error=error)


def parse_pdf_text(text: str, filename: str) -> ExtractRecord:
    if not text or not text.strip():
        return _empty_record(filename, "no_text_layer")
    return ExtractRecord(
        filename=filename,
        rights_holder=extract_rights_holder(text),
        property_certificate_no=extract_property_certificate_no(text),
        original_property_certificate_no=extract_original_mortgage_cert(text),
        location=extract_location(text),
        property_right_certificate_no=extract_property_right_certificate_no(text),
    )


def process_pdf(pdf_path: Path) -> ExtractRecord:
    try:
        text = pdf_reader.extract_text(pdf_path)
        return parse_pdf_text(text, pdf_path.name)
    except Exception as exc:
        logger.exception("process_pdf failed: %s", pdf_path)
        return _empty_record(pdf_path.name, str(exc))


def process_pdf_list(
    pdf_files: Sequence[Path],
    max_workers: int = DEFAULT_WORKERS,
    on_item_done: Optional[ItemDoneCallback] = None,
) -> List[ExtractRecord]:
    files = sorted(pdf_files)
    if not files:
        return []

    results: List[ExtractRecord] = []
    if len(files) <= 2:
        for pdf_file in files:
            results.append(process_pdf(pdf_file))
            if on_item_done:
                on_item_done(pdf_file)
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(process_pdf, p): p for p in files}
            for future in as_completed(futures):
                pdf_path = futures[future]
                results.append(future.result())
                if on_item_done:
                    on_item_done(pdf_path)
    results.sort(key=lambda r: r.filename)
    return results


def collect_all_pdfs(dir_path: Path) -> Tuple[List[Path], Dict[str, List[Path]]]:
    current = sorted(dir_path.glob("*.pdf"))
    subdirs: Dict[str, List[Path]] = {}
    for sub in sorted(d for d in dir_path.iterdir() if d.is_dir()):
        pdfs = sorted(sub.glob("*.pdf"))
        if pdfs:
            subdirs[sub.name] = pdfs
    return current, subdirs


def process_folder(
    folder: Path,
    max_workers: int = DEFAULT_WORKERS,
    on_item_done: Optional[ItemDoneCallback] = None,
) -> List[ExtractRecord]:
    current, subdirs = collect_all_pdfs(folder)
    if subdirs:
        records: List[ExtractRecord] = []
        for name in sorted(subdirs):
            records.extend(process_pdf_list(subdirs[name], max_workers, on_item_done))
        return records
    if current:
        return process_pdf_list(current, max_workers, on_item_done)
    all_pdfs = sorted(folder.rglob("*.pdf"))
    return process_pdf_list(all_pdfs, max_workers, on_item_done)


def _count_pdfs_in_sources(sources: Sequence[Path]) -> int:
    total = 0
    for source in sources:
        if source.is_dir():
            _, sub = collect_all_pdfs(source)
            if sub:
                total += sum(len(v) for v in sub.values())
            else:
                cur, _ = collect_all_pdfs(source)
                total += len(cur) if cur else len(list(source.rglob("*.pdf")))
        elif source.suffix.lower() == ".pdf":
            total += 1
    return total


def _source_label(sources: Sequence[Path]) -> str:
    folders = [p for p in sources if p.is_dir()]
    files = [p for p in sources if p.is_file()]
    if len(folders) == 1 and not files:
        return folders[0].name
    if len(files) == 1 and not folders:
        return files[0].stem
    return "extract"


def extract_sources(
    sources: Sequence[Path],
    max_workers: int = DEFAULT_WORKERS,
    on_progress: Optional[ProgressCallback] = None,
) -> ExtractResult:
    """仅提取字段，不写入 Excel。"""
    if not pdf_reader.available():
        raise RuntimeError("missing_pdf_library")

    folders = [p.resolve() for p in sources if p.is_dir()]
    files = [p.resolve() for p in sources if p.is_file() and p.suffix.lower() == ".pdf"]
    total_pdfs = _count_pdfs_in_sources(sources)
    processed = 0
    all_records: List[ExtractRecord] = []
    t0 = time.time()

    if on_progress and total_pdfs:
        on_progress(0, total_pdfs, "")

    def _tick(pdf_path: Path) -> None:
        nonlocal processed
        processed += 1
        if on_progress:
            on_progress(processed, total_pdfs, pdf_path.name)

    for folder in folders:
        records = process_folder(folder, max_workers, on_item_done=_tick)
        all_records.extend(records)

    if files:
        records = process_pdf_list(files, max_workers, on_item_done=_tick)
        all_records.extend(records)

    return ExtractResult(
        records=all_records,
        source_label=_source_label(list(sources)),
        elapsed_seconds=time.time() - t0,
    )


def run_sources(
    sources: Sequence[Path],
    output_dir: Path,
    max_workers: int = DEFAULT_WORKERS,
    excel_headers: Optional[Sequence[str]] = None,
    on_progress: Optional[ProgressCallback] = None,
    multi_file_label: str = "提取结果",
) -> List[JobResult]:
    if not pdf_reader.available():
        raise RuntimeError("missing_pdf_library")

    output_dir = output_dir.resolve()
    excel_dir = output_dir / "excel"
    (output_dir / "logs").mkdir(parents=True, exist_ok=True)

    headers = list(excel_headers or [])
    if len(headers) != 6:
        headers = ["序号", "权利人", "房屋坐落", "不动产权证号", "原他项权证号", "他项权证号"]

    folders = [p.resolve() for p in sources if p.is_dir()]
    files = [p.resolve() for p in sources if p.is_file() and p.suffix.lower() == ".pdf"]

    total_pdfs = 0
    for folder in folders:
        _, sub = collect_all_pdfs(folder)
        if sub:
            total_pdfs += sum(len(v) for v in sub.values())
        else:
            cur, _ = collect_all_pdfs(folder)
            total_pdfs += len(cur) if cur else len(list(folder.rglob("*.pdf")))
    total_pdfs += len(files)

    processed = 0
    jobs: List[JobResult] = []

    for folder in folders:
        t0 = time.time()
        records = process_folder(folder, max_workers)
        processed += len(records)
        if on_progress:
            on_progress(processed, total_pdfs, folder.name)
        if records:
            excel_path = excel_dir / f"{folder.name}.xlsx"
            write_excel(records, excel_path, headers)
            jobs.append(
                JobResult(
                    directory_name=folder.name,
                    excel_path=excel_path,
                    pdf_count=len(records),
                    records=records,
                    elapsed_seconds=time.time() - t0,
                )
            )

    if files:
        t0 = time.time()
        records = process_pdf_list(files, max_workers)
        processed += len(records)
        if on_progress:
            on_progress(processed, total_pdfs, files[0].name)
        if records:
            if len(files) == 1:
                excel_name = f"{files[0].stem}.xlsx"
                job_name = files[0].stem
            else:
                excel_name = f"{multi_file_label}.xlsx"
                job_name = multi_file_label
            excel_path = excel_dir / excel_name
            write_excel(records, excel_path, headers)
            jobs.append(
                JobResult(
                    directory_name=job_name,
                    excel_path=excel_path,
                    pdf_count=len(records),
                    records=records,
                    elapsed_seconds=time.time() - t0,
                )
            )

    return jobs


# CLI 兼容
def list_job_directories(pdf_root: Path) -> List[Tuple[str, int]]:
    if not pdf_root.is_dir():
        return []
    items: List[Tuple[str, int]] = []
    for d in sorted(p for p in pdf_root.iterdir() if p.is_dir()):
        current, subdirs = collect_all_pdfs(d)
        count = len(current) + sum(len(v) for v in subdirs.values())
        if count:
            items.append((d.name, count))
    return items


def run_batch(
    pdf_root: Path,
    output_dir: Path,
    selected_dirs: Optional[Sequence[str]] = None,
    max_workers: int = DEFAULT_WORKERS,
    excel_headers: Optional[Sequence[str]] = None,
    on_progress: Optional[ProgressCallback] = None,
) -> List[JobResult]:
    pdf_root = pdf_root.resolve()
    if selected_dirs:
        sources = [pdf_root / name for name in selected_dirs if (pdf_root / name).is_dir()]
    else:
        sources = [d for d in pdf_root.iterdir() if d.is_dir()]
    return run_sources(
        sources=sources,
        output_dir=output_dir,
        max_workers=max_workers,
        excel_headers=excel_headers,
        on_progress=on_progress,
    )

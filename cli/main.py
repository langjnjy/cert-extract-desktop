#!/usr/bin/env python3
"""命令行入口（无 GUI）。"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from cert_extract.core import pdf_reader
from cert_extract.core.constants import DEFAULT_WORKERS
from cert_extract.services.batch_service import run_batch, run_sources
from ui import i18n


def main() -> int:
    parser = argparse.ArgumentParser(description="他证通 CLI")
    parser.add_argument("--pdf-dir", default="pdf", help="PDF 根目录（批量子目录模式）")
    parser.add_argument("--source", nargs="+", help="文件夹或 PDF 文件路径，可多选")
    parser.add_argument("--output-dir", default="output", help="输出目录")
    parser.add_argument("--dirs", nargs="+", help="pdf-dir 下子目录名（兼容旧用法）")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    args = parser.parse_args()

    if not pdf_reader.available():
        print("缺少 pypdf，请 pip install -r requirements.txt", file=sys.stderr)
        return 1

    i18n.set_lang(args.lang)
    output = Path(args.output_dir)
    t0 = time.time()

    if args.source:
        sources = [Path(p) for p in args.source]
        jobs = run_sources(
            sources=sources,
            output_dir=output,
            max_workers=DEFAULT_WORKERS,
            excel_headers=i18n.excel_headers(),
            on_progress=lambda c, t, d: print(f"\r  {c}/{t} {d}", end="", flush=True),
            multi_file_label=i18n.t("multi_file_excel"),
        )
    else:
        root = Path(args.pdf_dir)
        if not root.is_dir():
            print(f"目录不存在: {root}", file=sys.stderr)
            return 1
        jobs = run_batch(
            pdf_root=root,
            output_dir=output,
            selected_dirs=args.dirs,
            max_workers=DEFAULT_WORKERS,
            excel_headers=i18n.excel_headers(),
            on_progress=lambda c, t, d: print(f"\r  {c}/{t} {d}", end="", flush=True),
        )

    print()
    for job in jobs:
        print(f"  {job.excel_path} ({job.pdf_count} PDFs)")
    print(f"完成，耗时 {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

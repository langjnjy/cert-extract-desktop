"""PDF 文本层读取。"""

from __future__ import annotations

from pathlib import Path

EXTRACT_METHOD: str | None = None

try:
    import pypdf

    EXTRACT_METHOD = "pypdf"
except ImportError:
    try:
        import PyPDF2  # noqa: F401

        EXTRACT_METHOD = "PyPDF2"
    except ImportError:
        try:
            import pdfplumber  # noqa: F401

            EXTRACT_METHOD = "pdfplumber"
        except ImportError:
            EXTRACT_METHOD = None


def available() -> bool:
    return EXTRACT_METHOD is not None


def extract_text(pdf_path: Path, max_pages: int = 3) -> str:
    if not EXTRACT_METHOD:
        return ""

    text_parts: list[str] = []
    try:
        if EXTRACT_METHOD == "pypdf":
            import pypdf as _pypdf

            with open(pdf_path, "rb") as f:
                reader = _pypdf.PdfReader(f)
                for i in range(min(max_pages, len(reader.pages))):
                    page_text = reader.pages[i].extract_text()
                    if page_text:
                        text_parts.append(page_text)
        elif EXTRACT_METHOD == "PyPDF2":
            import PyPDF2 as _PyPDF2

            with open(pdf_path, "rb") as f:
                reader = _PyPDF2.PdfReader(f)
                for i in range(min(max_pages, len(reader.pages))):
                    page_text = reader.pages[i].extract_text()
                    if page_text:
                        text_parts.append(page_text)
        elif EXTRACT_METHOD == "pdfplumber":
            import pdfplumber as _pdfplumber

            with _pdfplumber.open(pdf_path) as pdf:
                for i in range(min(max_pages, len(pdf.pages))):
                    page_text = pdf.pages[i].extract_text()
                    if page_text:
                        text_parts.append(page_text)
    except Exception:
        return ""
    return "\n".join(text_parts)

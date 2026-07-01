"""从 PDF 文本解析各字段。"""

from __future__ import annotations

import re


def _compact_line(text: str) -> str:
    return re.sub(r"\s+", "", text)


def _is_location_line(text: str) -> bool:
    """判断一行是否为坐落地址（含街道型与小区幢室型）。"""
    compact = _compact_line(text)
    if re.search(r"[区县市].*[镇街道].*[路街].*号", compact):
        return True
    # 如「浦江县湖畔居28幢1001室」：有县/区/市 + 幢，但无镇/路/号
    if re.search(r"[区县市].*?\d+幢", compact):
        return True
    return False


def extract_rights_holder(text: str) -> str:
    """义务人 → 权利人列"""
    cleaned = [line.strip() for line in text.split("\n") if line.strip()]
    for i, line in enumerate(cleaned):
        if line == "抵押权":
            parts: list[str] = []
            j = i + 2
            while j < len(cleaned):
                candidate = cleaned[j]
                compact = _compact_line(candidate)
                if _is_location_line(candidate):
                    break
                if re.match(r"^33\d+", compact):
                    break
                if candidate.startswith(("不动产权证号", "不动产权证书号")):
                    break
                parts.append(compact)
                j += 1
            return "".join(parts)
    return ""


def extract_original_mortgage_cert(text: str) -> str:
    match = re.search(r"原抵押权证明号[：:]\s*([^\n]+(?:\n[^\n]*)?)", text, re.MULTILINE)
    if not match:
        return ""
    cert_no = re.sub(r"\s+", "", match.group(1))
    if "权第" not in cert_no and "权" in cert_no and "不动产证明" in cert_no:
        cert_no = cert_no.replace("权", "权第", 1)
    return cert_no


def normalize_cert_display(cert_no: str) -> str:
    if not cert_no:
        return ""
    return cert_no.replace("(", "（").replace(")", "）")


def format_current_certificate_display(cert_no: str) -> str:
    if not cert_no:
        return ""
    match = re.search(
        r"浙\s*[\(（]\s*(\d{4})\s*[\)）]\s*([^不]+?)不动产证明第\s*(\d+)\s*号?",
        cert_no,
    )
    if match:
        year, city, number = match.groups()
        return f"浙（{year}）{city.strip()}不动产证明第{number}号"
    return re.sub(r"\s+", "", normalize_cert_display(cert_no))


def extract_property_certificate_no(text: str) -> str:
    """他项权证号：取证明右上角/页眉证号，排除「原抵押权证明号」。"""
    pattern_full = re.compile(
        r"浙\s*[\(（]\s*(\d{4})\s*[\)）]\s*([^\s]+)\s*不动产证明第\s*(\d+)", re.MULTILINE
    )
    pattern_short = re.compile(
        r"浙\s*[\(（]\s*(\d{4})\s*[\)）]\s*([^\s\d]+?)\s+(\d{7})\b"
    )

    def _format(year: str, city: str, number: str) -> str:
        return f"浙({year}){city.strip()}不动产证明第{number}号"

    def _is_original_mortgage_context(start: int) -> bool:
        snippet = text[max(0, start - 40) : start + 20]
        return "原抵押权证明号" in snippet or "原抵押" in snippet

    # 页眉证号在 PDF 文本中常出现在文末（如「浙( 2026 ) 浦江县 0000988」），自后向前匹配
    for line in reversed(text.split("\n")):
        stripped = line.strip()
        if not stripped or "原抵押权证明号" in stripped:
            continue
        match = pattern_short.search(stripped)
        if match:
            return _format(*match.groups())

    for match in pattern_full.finditer(text):
        if _is_original_mortgage_context(match.start()):
            continue
        return _format(*match.groups())

    return ""


def extract_location(text: str) -> str:
    pattern_situated = re.compile(r"坐\s*落", re.MULTILINE)
    pattern_start = re.compile(r"^[金东西南北中婺]", re.MULTILINE)
    pattern_continue = re.compile(r"[幢室号]", re.MULTILINE)
    pattern_exclude = re.compile(r"[坐落单元号]", re.MULTILINE)
    whitespace = re.compile(r"\s+")

    lines = text.split("\n")
    for i, line in enumerate(lines):
        if pattern_situated.search(line):
            for j in range(i + 1, min(i + 5, len(lines))):
                candidate = lines[j].strip()
                if candidate and _is_location_line(candidate):
                    address = candidate
                    if j > i + 1:
                        prev = lines[j - 1].strip()
                        if prev and pattern_start.search(prev) and not pattern_exclude.search(prev):
                            address = prev + address
                    if j + 1 < len(lines):
                        nxt = lines[j + 1].strip()
                        if nxt and pattern_continue.search(nxt) and "单元号" not in nxt:
                            address += nxt
                    return whitespace.sub("", address)
    for i, line in enumerate(lines):
        if _is_location_line(line):
            address = line.strip()
            if i > 0:
                prev = lines[i - 1].strip()
                if prev and prev.startswith("金") and not pattern_exclude.search(prev):
                    address = prev + address
            if i + 1 < len(lines):
                nxt = lines[i + 1].strip()
                if nxt and pattern_continue.search(nxt) and "单元号" not in nxt:
                    address += nxt
            return whitespace.sub("", address)
    return ""


# 从任意文本中提取「幢-室」短名（保留供其他场景使用）
_BUILDING_UNIT_PATTERNS = (
    re.compile(r"(\d+)幢([\d\-]+?)(?:商)?室"),
    re.compile(r"(\d+)幢([\d\-]+?)(?:商)?$"),
    re.compile(r"(\d+)号楼([\d\-]+?)(?:商)?室"),
    re.compile(r"(\d+)号([\d\-]+?)(?:商)?室"),
)


def rename_suffix_from_text(text: str) -> str:
    if not text:
        return ""
    compact = re.sub(r"\s+", "", text)
    for pattern in _BUILDING_UNIT_PATTERNS:
        matches = pattern.findall(compact)
        if matches:
            building, unit = matches[-1]
            return f"{building}-{unit}"
    return ""


def rename_suffix_from_location(location: str) -> str:
    return rename_suffix_from_text(location)


_FILENAME_PAREN_RE = re.compile(r"[（(]([^）)]+)[）)]")
_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|\n\r\t]')


def sanitize_filename_stem(name: str) -> str:
    """坐落 → 安全文件名（去空白、替换非法字符）。"""
    if not name:
        return ""
    cleaned = re.sub(r"\s+", "", name.strip())
    return _INVALID_FILENAME_CHARS.sub("_", cleaned)


def address_from_filename(stem: str) -> str:
    match = _FILENAME_PAREN_RE.search(stem)
    return match.group(1).strip() if match else ""


def derive_rename_stem(pdf_path: Path, pdf_text: str | None = None) -> tuple[str, str, str]:
    """以完整坐落作为新文件名，返回 (stem, 坐落, 来源)。"""
    current_stem = pdf_path.stem

    filename_addr = address_from_filename(current_stem)
    if filename_addr:
        location = re.sub(r"\s+", "", filename_addr)
        new_stem = sanitize_filename_stem(location)
        if new_stem:
            if new_stem == sanitize_filename_stem(current_stem):
                return new_stem, location, "already_named"
            return new_stem, location, "filename"

    location = ""
    if pdf_text:
        location = extract_location(pdf_text)
        if location:
            new_stem = sanitize_filename_stem(location)
            if new_stem:
                if new_stem == sanitize_filename_stem(current_stem):
                    return new_stem, location, "already_named"
                return new_stem, location, "location"

    return "", location or filename_addr, "no_match"


def extract_property_right_certificate_no(text: str) -> str:
    pattern = re.compile(
        r"不动产权(?:证|证书)号[：:]\s*([^\n]+(?:\n[^\n]*)?)", re.MULTILINE
    )
    whitespace = re.compile(r"\s+")
    match = pattern.search(text)
    if not match:
        return ""
    cert_no = whitespace.sub("", match.group(1))
    if "权第" not in cert_no and "权" in cert_no:
        cert_no = cert_no.replace("权", "权第", 1)
    return cert_no

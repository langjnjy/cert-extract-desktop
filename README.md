# TazhengTong Desktop

Desktop app for **Chinese real-estate registration certificate PDFs** (不动产登记证明).

Extract key fields to Excel, rename PDFs by property location, and work in Chinese or English—with 12 themes and light/dark mode.

**Current version:** see [Releases](https://github.com/langjnjy/cert-extract-desktop/releases) or the `version` file in this repo.

---

## What it does

| Feature | Summary |
|---------|---------|
| **Extract** | Select PDFs → preview & edit results → export to Excel |
| **Rename** | Select PDFs → preview new filenames → rename in batch |
| **CLI** | Batch extract without opening the GUI (for scripts) |

**Fields extracted:** rights holder, property location, mortgage certificate no., original mortgage certificate no., property title certificate no., and filename.

> **PDF requirement:** electronic PDFs with a selectable text layer only. Scanned images are not supported yet.

---

## Download

Pre-built packages for **Windows**, **macOS**, and **Linux** are published on the [Releases](https://github.com/langjnjy/cert-extract-desktop/releases) page.

| Platform | What you get |
|----------|--------------|
| Windows | Unzip and run `TazhengTong.exe` inside the folder |
| macOS | Unzip and open `TazhengTong.app` (if blocked: right-click → **Open**) |
| Linux | Unzip and run the `TazhengTong` executable inside the folder |

Always use the full folder from the zip—not a single `.exe` or binary alone.

---

## Run from source

Requires **Python 3.10+**.

```bash
git clone https://github.com/langjnjy/cert-extract-desktop.git
cd cert-extract-desktop
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

---

## Notes

- Excel column headers follow the UI language (中文 / English).
- Renaming may fail if a PDF is open in another program—close it and try again.
- Questions and issues: use [GitHub Issues](https://github.com/langjnjy/cert-extract-desktop/issues).

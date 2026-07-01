#!/usr/bin/env python3
"""他证通 / CertExtract — 桌面入口。"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from ui import i18n, theme
from ui.app_identity import apply_to, configure_before_qapplication
from ui.main_window import MainWindow


def _setup_logging() -> None:
    root = Path(__file__).resolve().parent
    log_dir = root / "output" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_dir / "app.log", encoding="utf-8")],
    )


def main() -> int:
    _setup_logging()
    configure_before_qapplication()
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    apply_to(app)
    app.setStyleSheet(theme.build_stylesheet())

    window = MainWindow()
    window.resize(800, 620)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

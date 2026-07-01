"""Qt 全局主题 — 整套界面配色（背景/卡片/边框/按钮），非仅强调色。"""

from __future__ import annotations

from typing import Dict, List

# 每套主题含 dark / light 完整色板（窗口背景、面板、输入框、日志区等全部跟随）
_THEMES: Dict[str, Dict[str, Dict[str, str]]] = {
    "indigo": {
        "dark": {
            "BG_PRIMARY": "#0f1419",
            "BG_PANEL": "#1a2332",
            "BG_CARD": "#222d3d",
            "BG_INPUT": "#151c28",
            "FG_PRIMARY": "#f1f5f9",
            "FG_MUTED": "#94a3b8",
            "FG_SUB": "#cbd5e1",
            "ACCENT": "#6366f1",
            "ACCENT_HOVER": "#818cf8",
            "ACCENT_SOFT": "#312e81",
            "BORDER": "#334155",
            "BTN_SECONDARY": "#273449",
            "BTN_SECONDARY_HOVER": "#334155",
            "PROGRESS_TRACK": "#1e293b",
            "LOG_BG": "#0b1020",
        },
        "light": {
            "BG_PRIMARY": "#eef2ff",
            "BG_PANEL": "#ffffff",
            "BG_CARD": "#f5f7ff",
            "BG_INPUT": "#ffffff",
            "FG_PRIMARY": "#1e1b4b",
            "FG_MUTED": "#64748b",
            "FG_SUB": "#475569",
            "ACCENT": "#4f46e5",
            "ACCENT_HOVER": "#4338ca",
            "ACCENT_SOFT": "#e0e7ff",
            "BORDER": "#c7d2fe",
            "BTN_SECONDARY": "#eef2ff",
            "BTN_SECONDARY_HOVER": "#e0e7ff",
            "PROGRESS_TRACK": "#e0e7ff",
            "LOG_BG": "#f8fafc",
        },
    },
    "ocean": {
        "dark": {
            "BG_PRIMARY": "#081018",
            "BG_PANEL": "#0f1f2e",
            "BG_CARD": "#152838",
            "BG_INPUT": "#0c1824",
            "FG_PRIMARY": "#e0f2fe",
            "FG_MUTED": "#7dd3fc",
            "FG_SUB": "#bae6fd",
            "ACCENT": "#0ea5e9",
            "ACCENT_HOVER": "#38bdf8",
            "ACCENT_SOFT": "#0c4a6e",
            "BORDER": "#1e4a66",
            "BTN_SECONDARY": "#123044",
            "BTN_SECONDARY_HOVER": "#1a4060",
            "PROGRESS_TRACK": "#0f2535",
            "LOG_BG": "#060d14",
        },
        "light": {
            "BG_PRIMARY": "#e0f2fe",
            "BG_PANEL": "#ffffff",
            "BG_CARD": "#f0f9ff",
            "BG_INPUT": "#ffffff",
            "FG_PRIMARY": "#0c4a6e",
            "FG_MUTED": "#0369a1",
            "FG_SUB": "#075985",
            "ACCENT": "#0284c7",
            "ACCENT_HOVER": "#0369a1",
            "ACCENT_SOFT": "#bae6fd",
            "BORDER": "#7dd3fc",
            "BTN_SECONDARY": "#e0f2fe",
            "BTN_SECONDARY_HOVER": "#bae6fd",
            "PROGRESS_TRACK": "#bae6fd",
            "LOG_BG": "#f0f9ff",
        },
    },
    "forest": {
        "dark": {
            "BG_PRIMARY": "#081210",
            "BG_PANEL": "#0f221c",
            "BG_CARD": "#152e26",
            "BG_INPUT": "#0c1a16",
            "FG_PRIMARY": "#ecfdf5",
            "FG_MUTED": "#6ee7b7",
            "FG_SUB": "#a7f3d0",
            "ACCENT": "#10b981",
            "ACCENT_HOVER": "#34d399",
            "ACCENT_SOFT": "#064e3b",
            "BORDER": "#1a4d3e",
            "BTN_SECONDARY": "#123528",
            "BTN_SECONDARY_HOVER": "#1a4a38",
            "PROGRESS_TRACK": "#0f2920",
            "LOG_BG": "#060f0c",
        },
        "light": {
            "BG_PRIMARY": "#ecfdf5",
            "BG_PANEL": "#ffffff",
            "BG_CARD": "#f0fdf4",
            "BG_INPUT": "#ffffff",
            "FG_PRIMARY": "#064e3b",
            "FG_MUTED": "#047857",
            "FG_SUB": "#065f46",
            "ACCENT": "#059669",
            "ACCENT_HOVER": "#047857",
            "ACCENT_SOFT": "#a7f3d0",
            "BORDER": "#6ee7b7",
            "BTN_SECONDARY": "#d1fae5",
            "BTN_SECONDARY_HOVER": "#a7f3d0",
            "PROGRESS_TRACK": "#a7f3d0",
            "LOG_BG": "#f0fdf4",
        },
    },
    "sunset": {
        "dark": {
            "BG_PRIMARY": "#120e08",
            "BG_PANEL": "#221a0f",
            "BG_CARD": "#2e2418",
            "BG_INPUT": "#1a140c",
            "FG_PRIMARY": "#fffbeb",
            "FG_MUTED": "#fcd34d",
            "FG_SUB": "#fde68a",
            "ACCENT": "#f59e0b",
            "ACCENT_HOVER": "#fbbf24",
            "ACCENT_SOFT": "#78350f",
            "BORDER": "#5c4018",
            "BTN_SECONDARY": "#352818",
            "BTN_SECONDARY_HOVER": "#4a3820",
            "PROGRESS_TRACK": "#2a2010",
            "LOG_BG": "#0e0a06",
        },
        "light": {
            "BG_PRIMARY": "#fffbeb",
            "BG_PANEL": "#ffffff",
            "BG_CARD": "#fef3c7",
            "BG_INPUT": "#ffffff",
            "FG_PRIMARY": "#78350f",
            "FG_MUTED": "#b45309",
            "FG_SUB": "#92400e",
            "ACCENT": "#d97706",
            "ACCENT_HOVER": "#b45309",
            "ACCENT_SOFT": "#fde68a",
            "BORDER": "#fcd34d",
            "BTN_SECONDARY": "#fef3c7",
            "BTN_SECONDARY_HOVER": "#fde68a",
            "PROGRESS_TRACK": "#fde68a",
            "LOG_BG": "#fffbeb",
        },
    },
    "rose": {
        "dark": {
            "BG_PRIMARY": "#120810",
            "BG_PANEL": "#221018",
            "BG_CARD": "#2e1822",
            "BG_INPUT": "#1a0c14",
            "FG_PRIMARY": "#fff1f2",
            "FG_MUTED": "#fda4af",
            "FG_SUB": "#fecdd3",
            "ACCENT": "#f43f5e",
            "ACCENT_HOVER": "#fb7185",
            "ACCENT_SOFT": "#881337",
            "BORDER": "#6b2038",
            "BTN_SECONDARY": "#351828",
            "BTN_SECONDARY_HOVER": "#4a2035",
            "PROGRESS_TRACK": "#2a1420",
            "LOG_BG": "#0e060a",
        },
        "light": {
            "BG_PRIMARY": "#fff1f2",
            "BG_PANEL": "#ffffff",
            "BG_CARD": "#ffe4e6",
            "BG_INPUT": "#ffffff",
            "FG_PRIMARY": "#881337",
            "FG_MUTED": "#be123c",
            "FG_SUB": "#9f1239",
            "ACCENT": "#e11d48",
            "ACCENT_HOVER": "#be123c",
            "ACCENT_SOFT": "#fecdd3",
            "BORDER": "#fda4af",
            "BTN_SECONDARY": "#ffe4e6",
            "BTN_SECONDARY_HOVER": "#fecdd3",
            "PROGRESS_TRACK": "#fecdd3",
            "LOG_BG": "#fff1f2",
        },
    },
    "grape": {
        "dark": {
            "BG_PRIMARY": "#0e0814",
            "BG_PANEL": "#1a1028",
            "BG_CARD": "#241836",
            "BG_INPUT": "#140c20",
            "FG_PRIMARY": "#faf5ff",
            "FG_MUTED": "#d8b4fe",
            "FG_SUB": "#e9d5ff",
            "ACCENT": "#a855f7",
            "ACCENT_HOVER": "#c084fc",
            "ACCENT_SOFT": "#581c87",
            "BORDER": "#4a2868",
            "BTN_SECONDARY": "#2a1840",
            "BTN_SECONDARY_HOVER": "#382050",
            "PROGRESS_TRACK": "#1e1230",
            "LOG_BG": "#0a0610",
        },
        "light": {
            "BG_PRIMARY": "#faf5ff",
            "BG_PANEL": "#ffffff",
            "BG_CARD": "#f3e8ff",
            "BG_INPUT": "#ffffff",
            "FG_PRIMARY": "#581c87",
            "FG_MUTED": "#7e22ce",
            "FG_SUB": "#6b21a8",
            "ACCENT": "#9333ea",
            "ACCENT_HOVER": "#7e22ce",
            "ACCENT_SOFT": "#e9d5ff",
            "BORDER": "#d8b4fe",
            "BTN_SECONDARY": "#f3e8ff",
            "BTN_SECONDARY_HOVER": "#e9d5ff",
            "PROGRESS_TRACK": "#e9d5ff",
            "LOG_BG": "#faf5ff",
        },
    },
    "slate": {
        "dark": {
            "BG_PRIMARY": "#0f1218",
            "BG_PANEL": "#1a2028",
            "BG_CARD": "#242b36",
            "BG_INPUT": "#141820",
            "FG_PRIMARY": "#f8fafc",
            "FG_MUTED": "#94a3b8",
            "FG_SUB": "#cbd5e1",
            "ACCENT": "#64748b",
            "ACCENT_HOVER": "#94a3b8",
            "ACCENT_SOFT": "#334155",
            "BORDER": "#475569",
            "BTN_SECONDARY": "#2a3340",
            "BTN_SECONDARY_HOVER": "#384454",
            "PROGRESS_TRACK": "#1e2530",
            "LOG_BG": "#0a0d12",
        },
        "light": {
            "BG_PRIMARY": "#f8fafc",
            "BG_PANEL": "#ffffff",
            "BG_CARD": "#f1f5f9",
            "BG_INPUT": "#ffffff",
            "FG_PRIMARY": "#1e293b",
            "FG_MUTED": "#64748b",
            "FG_SUB": "#475569",
            "ACCENT": "#475569",
            "ACCENT_HOVER": "#334155",
            "ACCENT_SOFT": "#e2e8f0",
            "BORDER": "#cbd5e1",
            "BTN_SECONDARY": "#f1f5f9",
            "BTN_SECONDARY_HOVER": "#e2e8f0",
            "PROGRESS_TRACK": "#e2e8f0",
            "LOG_BG": "#f8fafc",
        },
    },
    "crimson": {
        "dark": {
            "BG_PRIMARY": "#140808",
            "BG_PANEL": "#241010",
            "BG_CARD": "#321818",
            "BG_INPUT": "#180c0c",
            "FG_PRIMARY": "#fef2f2",
            "FG_MUTED": "#fca5a5",
            "FG_SUB": "#fecaca",
            "ACCENT": "#dc2626",
            "ACCENT_HOVER": "#ef4444",
            "ACCENT_SOFT": "#7f1d1d",
            "BORDER": "#6b2020",
            "BTN_SECONDARY": "#351818",
            "BTN_SECONDARY_HOVER": "#4a2222",
            "PROGRESS_TRACK": "#2a1414",
            "LOG_BG": "#0e0606",
        },
        "light": {
            "BG_PRIMARY": "#fef2f2",
            "BG_PANEL": "#ffffff",
            "BG_CARD": "#fee2e2",
            "BG_INPUT": "#ffffff",
            "FG_PRIMARY": "#7f1d1d",
            "FG_MUTED": "#b91c1c",
            "FG_SUB": "#991b1b",
            "ACCENT": "#dc2626",
            "ACCENT_HOVER": "#b91c1c",
            "ACCENT_SOFT": "#fecaca",
            "BORDER": "#fca5a5",
            "BTN_SECONDARY": "#fee2e2",
            "BTN_SECONDARY_HOVER": "#fecaca",
            "PROGRESS_TRACK": "#fecaca",
            "LOG_BG": "#fef2f2",
        },
    },
    "amber": {
        "dark": {
            "BG_PRIMARY": "#141008",
            "BG_PANEL": "#241c0e",
            "BG_CARD": "#322814",
            "BG_INPUT": "#181008",
            "FG_PRIMARY": "#fffbeb",
            "FG_MUTED": "#fde047",
            "FG_SUB": "#fef08a",
            "ACCENT": "#eab308",
            "ACCENT_HOVER": "#facc15",
            "ACCENT_SOFT": "#713f12",
            "BORDER": "#6b5010",
            "BTN_SECONDARY": "#352a14",
            "BTN_SECONDARY_HOVER": "#4a3a1a",
            "PROGRESS_TRACK": "#2a2210",
            "LOG_BG": "#0e0c06",
        },
        "light": {
            "BG_PRIMARY": "#fffbeb",
            "BG_PANEL": "#ffffff",
            "BG_CARD": "#fef9c3",
            "BG_INPUT": "#ffffff",
            "FG_PRIMARY": "#713f12",
            "FG_MUTED": "#a16207",
            "FG_SUB": "#854d0e",
            "ACCENT": "#ca8a04",
            "ACCENT_HOVER": "#a16207",
            "ACCENT_SOFT": "#fef08a",
            "BORDER": "#fde047",
            "BTN_SECONDARY": "#fef9c3",
            "BTN_SECONDARY_HOVER": "#fef08a",
            "PROGRESS_TRACK": "#fef08a",
            "LOG_BG": "#fffbeb",
        },
    },
    "teal": {
        "dark": {
            "BG_PRIMARY": "#081412",
            "BG_PANEL": "#0f2420",
            "BG_CARD": "#15322c",
            "BG_INPUT": "#0c1a18",
            "FG_PRIMARY": "#f0fdfa",
            "FG_MUTED": "#5eead4",
            "FG_SUB": "#99f6e4",
            "ACCENT": "#14b8a6",
            "ACCENT_HOVER": "#2dd4bf",
            "ACCENT_SOFT": "#115e59",
            "BORDER": "#1a524a",
            "BTN_SECONDARY": "#123530",
            "BTN_SECONDARY_HOVER": "#1a4840",
            "PROGRESS_TRACK": "#0f2a26",
            "LOG_BG": "#060e0c",
        },
        "light": {
            "BG_PRIMARY": "#f0fdfa",
            "BG_PANEL": "#ffffff",
            "BG_CARD": "#ccfbf1",
            "BG_INPUT": "#ffffff",
            "FG_PRIMARY": "#115e59",
            "FG_MUTED": "#0d9488",
            "FG_SUB": "#0f766e",
            "ACCENT": "#0d9488",
            "ACCENT_HOVER": "#0f766e",
            "ACCENT_SOFT": "#99f6e4",
            "BORDER": "#5eead4",
            "BTN_SECONDARY": "#ccfbf1",
            "BTN_SECONDARY_HOVER": "#99f6e4",
            "PROGRESS_TRACK": "#99f6e4",
            "LOG_BG": "#f0fdfa",
        },
    },
    "cyan": {
        "dark": {
            "BG_PRIMARY": "#081416",
            "BG_PANEL": "#0f2428",
            "BG_CARD": "#153238",
            "BG_INPUT": "#0c1a1e",
            "FG_PRIMARY": "#ecfeff",
            "FG_MUTED": "#67e8f9",
            "FG_SUB": "#a5f3fc",
            "ACCENT": "#06b6d4",
            "ACCENT_HOVER": "#22d3ee",
            "ACCENT_SOFT": "#155e75",
            "BORDER": "#1a5260",
            "BTN_SECONDARY": "#123540",
            "BTN_SECONDARY_HOVER": "#1a4850",
            "PROGRESS_TRACK": "#0f2a30",
            "LOG_BG": "#060e10",
        },
        "light": {
            "BG_PRIMARY": "#ecfeff",
            "BG_PANEL": "#ffffff",
            "BG_CARD": "#cffafe",
            "BG_INPUT": "#ffffff",
            "FG_PRIMARY": "#155e75",
            "FG_MUTED": "#0891b2",
            "FG_SUB": "#0e7490",
            "ACCENT": "#0891b2",
            "ACCENT_HOVER": "#0e7490",
            "ACCENT_SOFT": "#a5f3fc",
            "BORDER": "#67e8f9",
            "BTN_SECONDARY": "#cffafe",
            "BTN_SECONDARY_HOVER": "#a5f3fc",
            "PROGRESS_TRACK": "#a5f3fc",
            "LOG_BG": "#ecfeff",
        },
    },
    "violet": {
        "dark": {
            "BG_PRIMARY": "#0e0818",
            "BG_PANEL": "#1a1028",
            "BG_CARD": "#241838",
            "BG_INPUT": "#140c20",
            "FG_PRIMARY": "#f5f3ff",
            "FG_MUTED": "#c4b5fd",
            "FG_SUB": "#ddd6fe",
            "ACCENT": "#8b5cf6",
            "ACCENT_HOVER": "#a78bfa",
            "ACCENT_SOFT": "#4c1d95",
            "BORDER": "#4a3080",
            "BTN_SECONDARY": "#2a1848",
            "BTN_SECONDARY_HOVER": "#382060",
            "PROGRESS_TRACK": "#1e1238",
            "LOG_BG": "#0a0614",
        },
        "light": {
            "BG_PRIMARY": "#f5f3ff",
            "BG_PANEL": "#ffffff",
            "BG_CARD": "#ede9fe",
            "BG_INPUT": "#ffffff",
            "FG_PRIMARY": "#4c1d95",
            "FG_MUTED": "#6d28d9",
            "FG_SUB": "#5b21b6",
            "ACCENT": "#7c3aed",
            "ACCENT_HOVER": "#6d28d9",
            "ACCENT_SOFT": "#ddd6fe",
            "BORDER": "#c4b5fd",
            "BTN_SECONDARY": "#ede9fe",
            "BTN_SECONDARY_HOVER": "#ddd6fe",
            "PROGRESS_TRACK": "#ddd6fe",
            "LOG_BG": "#f5f3ff",
        },
    },
}

THEME_ORDER: List[str] = [
    "indigo",
    "ocean",
    "forest",
    "sunset",
    "rose",
    "grape",
    "slate",
    "crimson",
    "amber",
    "teal",
    "cyan",
    "violet",
]

_mode = "dark"
_accent = "indigo"
C: Dict[str, str] = {}


def _rebuild() -> None:
    global C
    C = dict(_THEMES[_accent][_mode])


_rebuild()


def current_mode() -> str:
    return _mode


def current_accent() -> str:
    return _accent


def accent_choices() -> List[str]:
    return list(THEME_ORDER)


def accent_row_groups(row_size: int = 6) -> List[List[str]]:
    """主题色预览分行（导航栏每行 row_size 个）。"""
    return [THEME_ORDER[i : i + row_size] for i in range(0, len(THEME_ORDER), row_size)]


def theme_preview_color(accent_key: str) -> str:
    """主题色预览圆点。"""
    if accent_key in _THEMES:
        return _THEMES[accent_key]["dark"]["ACCENT"]
    return "#6366f1"


def set_mode(name: str) -> None:
    global _mode
    if _accent in _THEMES and name in _THEMES[_accent]:
        _mode = name
        _rebuild()


def set_accent(name: str) -> None:
    global _accent
    if name in _THEMES:
        _accent = name
        _rebuild()


def toggle_mode() -> str:
    set_mode("light" if _mode == "dark" else "dark")
    return _mode


def cycle_accent() -> str:
    idx = THEME_ORDER.index(_accent)
    set_accent(THEME_ORDER[(idx + 1) % len(THEME_ORDER)])
    return _accent


def current_theme() -> str:
    return _mode


def set_theme(name: str) -> None:
    set_mode(name)


def toggle_theme() -> str:
    return toggle_mode()


def build_stylesheet() -> str:
    return f"""
    QWidget {{
        background-color: {C['BG_PRIMARY']};
        color: {C['FG_PRIMARY']};
        font-family: 'PingFang SC', 'Helvetica Neue', 'Microsoft YaHei', sans-serif;
        font-size: 12px;
    }}
    QMainWindow {{
        background-color: {C['BG_PRIMARY']};
    }}
    QFrame#navBar {{
        background-color: {C['BG_PANEL']};
        border-bottom: 1px solid {C['BORDER']};
    }}
    QLabel#navBrand {{
        font-size: 15px;
        font-weight: 700;
        color: {C['FG_PRIMARY']};
        background: transparent;
    }}
    QLabel#navTagline {{
        font-size: 10px;
        color: {C['FG_MUTED']};
        background: transparent;
    }}
    QLabel#navGroupLabel {{
        font-size: 9px;
        font-weight: 600;
        color: {C['FG_MUTED']};
        background: transparent;
        letter-spacing: 0.5px;
    }}
    QFrame#navDivider {{
        background-color: {C['BORDER']};
        border: none;
    }}
    QPushButton#navSegBtn {{
        background-color: {C['BG_CARD']};
        border: 1px solid {C['BORDER']};
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 11px;
        font-weight: 600;
        min-width: 44px;
    }}
    QPushButton#navSegBtn:checked {{
        background-color: {C['ACCENT']};
        color: white;
        border: none;
    }}
    QPushButton#navFeatureBtn {{
        background-color: transparent;
        border: none;
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 12px;
        font-weight: 600;
        color: {C['FG_MUTED']};
    }}
    QPushButton#navFeatureBtn:checked {{
        background-color: {C['ACCENT_SOFT']};
        color: {C['FG_PRIMARY']};
    }}
    QPushButton#navFeatureBtn:hover:!checked {{
        color: {C['FG_PRIMARY']};
        background-color: {C['BG_CARD']};
    }}
    QPushButton#navMoreBtn {{
        background-color: transparent;
        border: none;
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 12px;
        font-weight: 600;
        color: {C['FG_MUTED']};
    }}
    QPushButton#navMoreBtn:hover {{
        color: {C['FG_PRIMARY']};
        background-color: {C['BG_CARD']};
    }}
    QMenu {{
        background-color: {C['BG_PANEL']};
        border: 1px solid {C['BORDER']};
        border-radius: 10px;
        padding: 6px;
    }}
    QMenu::item {{
        padding: 8px 20px;
        border-radius: 6px;
        color: {C['FG_PRIMARY']};
        font-size: 12px;
    }}
    QMenu::item:selected {{
        background-color: {C['ACCENT_SOFT']};
        color: {C['FG_PRIMARY']};
    }}
    QStackedWidget#contentStack {{
        background-color: {C['BG_PRIMARY']};
        border: none;
    }}
    QLabel#pageTitle {{
        font-size: 16px;
        font-weight: 700;
        color: {C['FG_PRIMARY']};
        background: transparent;
    }}
    QLabel#pageDesc {{
        font-size: 11px;
        color: {C['FG_MUTED']};
        background: transparent;
    }}
    QFrame#placeholderCard {{
        background-color: {C['BG_PANEL']};
        border: 1px dashed {C['BORDER']};
        border-radius: 16px;
    }}
    QLabel#placeholderIcon {{
        font-size: 32px;
        color: {C['ACCENT']};
        background: transparent;
    }}
    QLabel#placeholderTitle {{
        font-size: 15px;
        font-weight: 700;
        color: {C['FG_PRIMARY']};
        background: transparent;
    }}
    QLabel#placeholderDesc {{
        font-size: 11px;
        color: {C['FG_MUTED']};
        background: transparent;
    }}
    QPushButton#navSegBtn:hover:!checked {{
        border-color: {C['ACCENT']};
    }}
    QPushButton#navToggleBtn {{
        background-color: {C['BG_CARD']};
        border: 1px solid {C['BORDER']};
        border-radius: 10px;
        padding: 4px 8px;
        font-size: 11px;
        font-weight: 600;
        color: {C['FG_PRIMARY']};
        min-height: 18px;
    }}
    QPushButton#navToggleBtn:hover {{
        border-color: {C['ACCENT']};
        background-color: {C['ACCENT_SOFT']};
    }}
    QFrame#statusCard {{
        background: transparent;
        border: none;
    }}
    QFrame#previewCard {{
        background-color: {C['BG_PANEL']};
        border: 1px solid {C['BORDER']};
        border-radius: 16px;
    }}
    QFrame#featureCard {{
        background-color: {C['BG_PANEL']};
        border: 1px solid {C['BORDER']};
        border-radius: 14px;
    }}
    QLabel#featureTitle {{
        font-size: 12px;
        font-weight: 700;
        color: {C['FG_PRIMARY']};
        background: transparent;
    }}
    QLabel#previewStats {{
        font-size: 11px;
        font-weight: 600;
        color: {C['ACCENT']};
        background: transparent;
    }}
    QTableWidget#previewTable {{
        background-color: {C['BG_CARD']};
        alternate-background-color: {C['BG_INPUT']};
        border: 1px solid {C['BORDER']};
        border-radius: 12px;
        gridline-color: {C['BORDER']};
        color: {C['FG_PRIMARY']};
        selection-background-color: {C['ACCENT_SOFT']};
        selection-color: {C['FG_PRIMARY']};
    }}
    QTableWidget#previewTable QHeaderView::section {{
        background-color: {C['BG_PANEL']};
        color: {C['FG_SUB']};
        font-weight: 700;
        font-size: 11px;
        padding: 8px 6px;
        border: none;
        border-bottom: 2px solid {C['ACCENT']};
        border-right: 1px solid {C['BORDER']};
    }}
    QTableWidget#previewTable::item {{
        padding: 4px 6px;
        font-size: 11px;
    }}
    QTableWidget#previewTable::item:selected {{
        background-color: {C['ACCENT_SOFT']};
    }}
    QToolButton#replaceIconBtn {{
        background-color: {C['BG_CARD']};
        border: 1px solid {C['BORDER']};
        border-radius: 6px;
        color: {C['FG_SUB']};
        font-size: 9px;
        font-weight: 700;
        padding: 0;
    }}
    QToolButton#replaceIconBtn:hover {{
        border-color: {C['ACCENT']};
        color: {C['ACCENT']};
        background-color: {C['ACCENT_SOFT']};
    }}
    QLabel#tableColHeaderLabel {{
        font-size: 11px;
        font-weight: 700;
        color: {C['FG_SUB']};
        background: transparent;
    }}
    QWidget#newNameHeader {{
        background: transparent;
    }}
    QFrame#panelCard {{
        background-color: {C['BG_PANEL']};
        border: 1px solid {C['BORDER']};
        border-radius: 14px;
    }}
    QFrame#sourceCard {{
        background-color: {C['BG_PANEL']};
        border: 1px solid {C['BORDER']};
        border-radius: 16px;
    }}
    QLabel#sectionTitle {{
        font-size: 12px;
        font-weight: 700;
        color: {C['FG_PRIMARY']};
        background: transparent;
    }}
    QLabel#hintLabel {{
        font-size: 11px;
        color: {C['FG_MUTED']};
        background: transparent;
        line-height: 1.4;
    }}
    QLineEdit#sourceInput {{
        background-color: {C['BG_CARD']};
        border: 1px dashed {C['BORDER']};
        border-radius: 10px;
        padding: 8px 10px;
        font-size: 11px;
        color: {C['FG_SUB']};
        min-height: 20px;
    }}
    QPushButton#pickBtn {{
        background-color: {C['BG_CARD']};
        border: 1px solid {C['BORDER']};
        border-radius: 10px;
        padding: 7px 14px;
        font-size: 11px;
        font-weight: 600;
        min-width: 120px;
    }}
    QPushButton#pickBtn:hover {{
        border-color: {C['ACCENT']};
        background-color: {C['ACCENT_SOFT']};
        color: {C['FG_PRIMARY']};
    }}
    QLabel#appTitle {{
        font-size: 26px;
        font-weight: 700;
        color: {C['FG_PRIMARY']};
        background: transparent;
    }}
    QLabel#appSubtitle {{
        font-size: 13px;
        color: {C['FG_MUTED']};
        background: transparent;
    }}
    QLabel#fieldLabel {{
        font-size: 11px;
        font-weight: 600;
        color: {C['FG_SUB']};
        background: transparent;
    }}
    QLabel#footerLabel {{
        color: {C['FG_MUTED']};
        font-size: 10px;
        background: transparent;
    }}
    QLineEdit, QSpinBox {{
        background-color: {C['BG_INPUT']};
        border: 1px solid {C['BORDER']};
        border-radius: 8px;
        padding: 6px 10px;
        color: {C['FG_PRIMARY']};
        min-height: 18px;
    }}
    QLineEdit:focus, QSpinBox:focus {{
        border: 1px solid {C['ACCENT']};
    }}
    QListWidget {{
        background-color: {C['BG_CARD']};
        border: 1px solid {C['BORDER']};
        border-radius: 10px;
        padding: 6px;
        outline: none;
        color: {C['FG_PRIMARY']};
    }}
    QListWidget::item {{
        border-radius: 8px;
        padding: 10px 12px;
        margin: 2px 0;
    }}
    QListWidget::item:selected {{
        background-color: {C['ACCENT']};
        color: white;
    }}
    QListWidget::item:hover:!selected {{
        background-color: {C['BTN_SECONDARY_HOVER']};
    }}
    QPushButton {{
        background-color: {C['BTN_SECONDARY']};
        border: 1px solid {C['BORDER']};
        border-radius: 8px;
        padding: 8px 16px;
        color: {C['FG_PRIMARY']};
        font-weight: 600;
    }}
    QPushButton:hover {{
        background-color: {C['BTN_SECONDARY_HOVER']};
    }}
    QPushButton#actionBtn {{
        background-color: {C['ACCENT']};
        border: none;
        color: white;
        padding: 7px 18px;
        font-size: 11px;
        font-weight: 600;
        border-radius: 8px;
        min-width: 88px;
    }}
    QPushButton#actionBtn:hover {{
        background-color: {C['ACCENT_HOVER']};
    }}
    QPushButton#actionBtn:disabled {{
        background-color: {C['BORDER']};
        color: {C['FG_MUTED']};
    }}
    QPushButton#primaryBtn {{
        background-color: {C['ACCENT']};
        border: none;
        color: white;
        padding: 8px 18px;
        font-size: 12px;
        border-radius: 8px;
    }}
    QPushButton#primaryBtn:hover {{
        background-color: {C['ACCENT_HOVER']};
    }}
    QPushButton#primaryBtn:disabled {{
        background-color: {C['BORDER']};
        color: {C['FG_MUTED']};
    }}
    QPushButton#ghostBtn {{
        background-color: {C['BTN_SECONDARY']};
        border: 1px solid {C['BORDER']};
        color: {C['FG_PRIMARY']};
    }}
    QPushButton#ghostBtn:hover {{
        background-color: {C['BTN_SECONDARY_HOVER']};
    }}
    QPushButton#accentBtn {{
        background-color: {C['ACCENT']};
        border: none;
        color: white;
        padding: 8px 14px;
        font-weight: 600;
    }}
    QPushButton#accentBtn:hover {{
        background-color: {C['ACCENT_HOVER']};
    }}
    QProgressBar {{
        background-color: {C['PROGRESS_TRACK']};
        border: none;
        border-radius: 3px;
        min-height: 8px;
        max-height: 8px;
        text-align: center;
        color: transparent;
    }}
    QProgressBar::chunk {{
        background-color: {C['ACCENT']};
        border-radius: 3px;
    }}
    QTextEdit#logView {{
        background-color: {C['LOG_BG']};
        border: 1px solid {C['BORDER']};
        border-radius: 10px;
        padding: 10px;
        font-family: 'Menlo', 'Consolas', monospace;
        font-size: 12px;
        color: {C['FG_SUB']};
    }}
    QScrollBar:vertical {{
        background: {C['BG_CARD']};
        width: 10px;
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical {{
        background: {C['BORDER']};
        border-radius: 5px;
        min-height: 24px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    QPushButton#settingsBtn {{
        background-color: {C['BG_CARD']};
        border: 1px solid {C['BORDER']};
        border-radius: 19px;
        padding: 0;
        min-width: 36px;
        max-width: 36px;
        min-height: 36px;
        max-height: 36px;
    }}
    QPushButton#settingsBtn:hover {{
        background-color: {C['BTN_SECONDARY_HOVER']};
        border-color: {C['ACCENT']};
    }}
    QPushButton#settingsBtn:pressed {{
        background-color: {C['ACCENT_SOFT']};
    }}
    QFrame#settingsPopover {{
        background-color: {C['BG_PANEL']};
        border: 1px solid {C['BORDER']};
        border-radius: 14px;
    }}
    QLabel#settingsTitle {{
        font-size: 15px;
        font-weight: 700;
        color: {C['FG_PRIMARY']};
        background: transparent;
    }}
    QLabel#settingsSection {{
        font-size: 11px;
        font-weight: 600;
        color: {C['FG_MUTED']};
        background: transparent;
        padding-top: 2px;
    }}
    QPushButton[chipBtn="true"] {{
        text-align: left;
        padding: 8px 12px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 600;
        background-color: {C['BG_CARD']};
    }}
    QPushButton[chipBtn="true"]:checked {{
        background-color: {C['ACCENT_SOFT']};
        border: 2px solid {C['ACCENT']};
        color: {C['FG_PRIMARY']};
    }}
    QPushButton#segBtn {{
        padding: 8px 0;
        border-radius: 8px;
        font-weight: 600;
        background-color: {C['BG_CARD']};
    }}
    QPushButton#segBtn:checked {{
        background-color: {C['ACCENT']};
        color: white;
        border: none;
    }}
    """

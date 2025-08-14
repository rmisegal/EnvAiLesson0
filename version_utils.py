"""Utility module for cross-platform colored terminal output.

Provides ANSI escape sequences on Unix-like systems and uses
``colorama`` on Windows when available. Falls back to plain text when
color support isn't available.
"""

from __future__ import annotations

import os
import sys

COLORAMA_AVAILABLE = False
if os.name == "nt":
    try:
        from colorama import Fore, Style, init as _colorama_init
        _colorama_init()
        COLORAMA_AVAILABLE = True
    except Exception:
        COLORAMA_AVAILABLE = False


def _colors_disabled() -> bool:
    """Determine if colored output should be disabled."""
    if os.name == "nt":
        return not COLORAMA_AVAILABLE
    # On Unix-like systems, assume color support if stdout is a TTY
    return not sys.stdout.isatty()


class Colors:
    """Collection of color escape sequences."""

    if _colors_disabled():
        RESET = CYAN = GREEN = YELLOW = RED = BLUE = MAGENTA = ""
    elif os.name == "nt" and COLORAMA_AVAILABLE:
        RESET = Style.RESET_ALL
        CYAN = Fore.CYAN
        GREEN = Fore.GREEN
        YELLOW = Fore.YELLOW
        RED = Fore.RED
        BLUE = Fore.BLUE
        MAGENTA = Fore.MAGENTA
    else:  # Unix-like with ANSI support
        RESET = "\033[0m"
        CYAN = "\033[96m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RED = "\033[91m"
        BLUE = "\033[94m"
        MAGENTA = "\033[95m"

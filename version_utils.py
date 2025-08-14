"""Utility functions for version checking scripts."""

from __future__ import annotations

import os

# Track the final status of a version check run
_last_status: bool | None = None


def set_last_status(status: bool) -> None:
    """Record the final success status for later use in the footer."""
    global _last_status
    _last_status = status


def print_footer(script_version: str) -> None:
    """Print footer information, adapting output based on final status."""
    print()
    print("================================================================")
    print("                   JSON CONFIGURATION INFO")
    print("================================================================")
    print()
    print("[INFO] Configuration file: version_config.json")
    print(f"[INFO] Script version: {script_version}")
    print("[INFO] To view detailed version requirements:")
    if os.name == "nt":  # Windows
        print("  type version_config.json")
    else:  # Unix/Linux/Mac
        print("  cat version_config.json")
    print()
    print("[INFO] To update expected versions:")
    print("  Edit version_config.json with your preferred text editor")
    print()
    print("================================================================")
    if _last_status is True:
        print("                   VERSION CHECK SUCCESSFUL")
    elif _last_status is False:
        print("               VERSION CHECK COMPLETED WITH ISSUES")
    else:
        print("                   VERSION CHECK COMPLETE")
    print("================================================================")


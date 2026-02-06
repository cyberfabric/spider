#!/usr/bin/env python3
"""
Spaider Validator - Main Entry Point

This is a thin wrapper that imports from the modular spaider package.
For backward compatibility, all functions are re-exported at module level.

Legacy monolithic implementation preserved in legacy.py.
"""

# Re-export everything from the spaider package for backward compatibility
from spaider import *
from spaider import __all__

# CLI entry point
if __name__ == "__main__":
    from spaider import main
    raise SystemExit(main())

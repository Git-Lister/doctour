#!/usr/bin/env python3
"""Main entry point for Doctour medieval medical AI."""

import argparse
import sys
from typing import Optional


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Doctour - Medieval Medical AI",
        epilog="Educational/experimental use only - not medical advice."
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Start interactive consultation mode"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information"
    )
    return parser.parse_args()


def main() -> int:
    """Main application entry point."""
    args = parse_args()
    
    if args.version:
        from doctour import __version__
        print(f"Doctour version {__version__}")
        return 0
    
    if args.interactive:
        print("🏰 Doctour - Medieval Medical AI")
        print("Educational/experimental use only\n")
        print("Interactive mode coming soon...")
        return 0
    
    print("Usage: doctour --interactive")
    return 1


if __name__ == "__main__":
    sys.exit(main())

"""Command-line interface for qubit_measurement_analysis package."""

# python -m qubit_measurement_analysis.cli cython --is_compiled
# python -m qubit_measurement_analysis.cli cython compile

import argparse
from qubit_measurement_analysis.cython._compilation_utils import (
    check_cython_compiled,
    compile_cython,
)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Qubit Measurement Analysis CLI")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Cython subcommand
    cython_parser = subparsers.add_parser("cython", help="Cython-related commands")

    # Cython arguments
    cython_parser.add_argument(
        "action", nargs="?", choices=["compile"], help="Action to perform with Cython"
    )

    cython_parser.add_argument(
        "--is_compiled",
        action="store_true",
        help="Check if Cython extensions are compiled",
    )

    args = parser.parse_args()

    if args.command == "cython":
        if args.is_compiled:
            is_compiled = check_cython_compiled()
            print(
                f"Cython extensions are {'compiled' if is_compiled else 'not compiled'}"
            )
        elif args.action == "compile":
            compile_cython()
        else:
            cython_parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

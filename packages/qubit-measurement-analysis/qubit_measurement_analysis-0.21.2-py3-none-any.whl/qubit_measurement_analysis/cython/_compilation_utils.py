"""Cython compilation utils for qubit_measurement_analysis package."""

# pylint: disable=broad-exception-caught
from pathlib import Path
import importlib.util
import subprocess
import sys


def check_cython_compiled() -> bool:
    """Check if Cython extensions are compiled."""
    extensions = [
        "qubit_measurement_analysis.cython._sspd",
        "qubit_measurement_analysis.cython._transformations",
        "qubit_measurement_analysis.cython.classification.cttp_utils",
    ]

    return all(importlib.util.find_spec(ext) is not None for ext in extensions)


def compile_cython():
    """Compile Cython extensions using setup.py."""
    try:
        # Get the current working directory
        cwd = Path.cwd()
        setup_py = cwd / "setup.py"

        if not setup_py.exists():
            # Try looking in parent directories
            for parent in cwd.parents:
                setup_py = parent / "setup.py"
                if setup_py.exists():
                    break
            else:
                print("Error: setup.py not found in current or parent directories")
                sys.exit(1)

        # Run compilation command
        print(f"Compiling Cython extensions using {setup_py}")
        result = subprocess.run(
            [sys.executable, str(setup_py), "build_ext", "--inplace"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            print("Successfully compiled Cython extensions")
        else:
            print("Failed to compile Cython extensions:")
            print(result.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error during compilation: {str(e)}")
        sys.exit(1)

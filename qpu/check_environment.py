#!/usr/bin/env python3
"""Check QPU environment setup."""

import sys


def main():
    print("QPU Environment Check")
    print("=" * 50)
    
    # Check Python version
    print(f"Python: {sys.version}")
    
    # Check numpy
    try:
        import numpy as np
        print(f"NumPy: {np.__version__}")
    except ImportError:
        print("NumPy: NOT INSTALLED")
        return 1
    
    # Check scipy
    try:
        import scipy
        print(f"SciPy: {scipy.__version__}")
    except ImportError:
        print("SciPy: NOT INSTALLED")
        return 1
    
    # Check Perceval
    try:
        import perceval
        print(f"Perceval: {perceval.__version__}")
    except ImportError:
        print("Perceval: NOT INSTALLED")
        return 1
    
    # Check QPU token
    import os
    token = os.environ.get("QPU_TOKEN", None)
    if token:
        print(f"QPU Token: SET (length: {len(token)})")
    else:
        print("QPU Token: NOT SET")
        print("  Set with: export QPU_TOKEN='your-token'")
    
    print("\nEnvironment ready for QPU experiments.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

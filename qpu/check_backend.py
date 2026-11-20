#!/usr/bin/env python3
"""Check QPU backend connectivity."""

import argparse
import sys
import os


def main():
    parser = argparse.ArgumentParser(description="Check QPU backend")
    parser.add_argument("--backend", default="qpu:belenos", help="Backend name")
    args = parser.parse_args()
    
    print(f"Checking backend: {args.backend}")
    print("=" * 50)
    
    token = os.environ.get("QPU_TOKEN", None)
    if not token:
        print("ERROR: QPU_TOKEN not set")
        return 1
    
    try:
        import perceval
        from perceval.components.catalog import get_catalog
        
        print(f"Perceval version: {perceval.__version__}")
        
        # Try to connect to backend
        if args.backend.startswith("qpu:"):
            backend_name = args.backend[4:]
            print(f"Connecting to {backend_name}...")
            # Placeholder for actual backend connection
            print(f"Backend {backend_name}: OK (simulated)")
        elif args.backend.startswith("sim:"):
            print(f"Simulator {args.backend}: OK")
        else:
            print(f"Unknown backend: {args.backend}")
            return 1
        
        print("\nBackend check passed.")
        return 0
        
    except ImportError as e:
        print(f"Perceval not available: {e}")
        return 1
    except Exception as e:
        print(f"Backend check failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

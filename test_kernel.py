#!/usr/bin/env python3
"""
Simple test script for VibeKernel functionality
"""

import sys
from vibekernel.kernel import VibeKernel

def test_kernel_basic():
    """Test basic kernel functionality"""
    print("Testing VibeKernel...")
    
    # Create kernel instance
    kernel = VibeKernel()
    
    # Test cases
    test_cases = [
        ("(+ 1 2 3)", 6),
        ("(* 4 5)", 20),
        ("(defn square [x] (* x x))", None),
        ("(square 5)", 25),
        ("(print \"Hello from Hy!\")", None),
    ]
    
    for code, expected in test_cases:
        print(f"\nTesting: {code}")
        try:
            result = kernel.do_execute(code, silent=True)
            if result['status'] == 'ok':
                print(f"✓ Success: {code}")
            else:
                print(f"✗ Failed: {code}")
                print(f"  Error: {result.get('evalue', 'Unknown error')}")
        except Exception as e:
            print(f"✗ Exception: {code}")
            print(f"  {type(e).__name__}: {e}")
    
    print("\nKernel test complete!")

if __name__ == "__main__":
    test_kernel_basic()
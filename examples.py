#!/usr/bin/env python3
"""
Example usage of the UV-Vis Gaussian fitting tool.
This script demonstrates various ways to use the uvvis_gaussian_fit.py tool.
"""

import subprocess
import sys

def run_example(description, command):
    """Run an example command and display results."""
    print(f"\n{'='*60}")
    print(f"Example: {description}")
    print(f"Command: {' '.join(command)}")
    print('='*60)
    
    try:
        result = subprocess.run(command, capture_output=False, text=True)
        if result.returncode != 0:
            print(f"Error running command: {result.stderr}")
    except Exception as e:
        print(f"Failed to run command: {e}")

def main():
    print("UV-Vis Gaussian Fitting Tool - Example Usage")
    print("=" * 60)
    
    # Check if the main script exists
    try:
        with open('uvvis_gaussian_fit.py', 'r'):
            pass
    except FileNotFoundError:
        print("Error: uvvis_gaussian_fit.py not found in current directory")
        return
    
    # Example 1: Basic usage with 3 Gaussians
    run_example(
        "Fit 3 Gaussians with automatic initial guess",
        ["python", "uvvis_gaussian_fit.py", "spectrum.csv", "3"]
    )
    
    # Example 2: Specify initial peak positions
    run_example(
        "Fit 2 Gaussians with specified initial peak positions",
        ["python", "uvvis_gaussian_fit.py", "spectrum.csv", "2", 
         "--initial_peaks", "25000", "15000"]
    )
    
    # Example 3: Restrict wavelength range
    run_example(
        "Fit 3 Gaussians in limited wavelength range (300-700 nm)",
        ["python", "uvvis_gaussian_fit.py", "spectrum.csv", "3",
         "--range_nm", "300", "700"]
    )
    
    # Example 4: Display in wavenumber units
    run_example(
        "Fit 2 Gaussians and display results in wavenumber units",
        ["python", "uvvis_gaussian_fit.py", "spectrum.csv", "2",
         "--display_unit", "cm"]
    )
    
    # Example 5: Save plot to file
    run_example(
        "Fit 3 Gaussians and save plot to file",
        ["python", "uvvis_gaussian_fit.py", "spectrum.csv", "3",
         "--save", "spectrum_fit.png"]
    )

if __name__ == "__main__":
    main()
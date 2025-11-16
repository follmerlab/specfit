#!/usr/bin/env python3
"""
Quick start script for UV-Vis Gaussian fitting.
This provides an interactive way to use the main fitting tool.
"""

import os
import sys

def get_user_input():
    """Get user preferences interactively."""
    print("UV-Vis Gaussian Fitting Tool - Quick Start")
    print("=" * 50)
    
    # Get CSV file
    while True:
        csv_file = input("\nEnter CSV filename (or 'demo' for example): ").strip()
        if csv_file.lower() == 'demo':
            csv_file = 'spectrum.csv'
            break
        elif os.path.exists(csv_file):
            break
        else:
            print(f"File '{csv_file}' not found. Please try again.")
    
    # Get number of Gaussians
    while True:
        try:
            n_gaussians = int(input("\nNumber of Gaussians to fit (2-5 recommended): "))
            if n_gaussians > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Ask about initial peak positions
    use_initial = input("\nSpecify initial peak positions? (y/n): ").lower().startswith('y')
    initial_peaks = []
    
    if use_initial:
        # Ask for units preference
        units = input("Enter peak positions in (nm) or (cm): ").lower()
        if units not in ['nm', 'cm']:
            units = 'nm'  # default to nm
        
        if units == 'nm':
            print(f"\nEnter {n_gaussians} initial peak positions in wavelength (nm):")
            print("Tip: Look at your spectrum to identify peak positions")
        else:
            print(f"\nEnter {n_gaussians} initial peak positions in wavenumber (cm⁻¹):")
            print("Tip: 500 nm = 20,000 cm⁻¹, 400 nm = 25,000 cm⁻¹, 300 nm = 33,333 cm⁻¹")
        
        for i in range(n_gaussians):
            while True:
                try:
                    peak = float(input(f"  Peak {i+1} ({units}): "))
                    initial_peaks.append(peak)
                    break
                except ValueError:
                    print("    Please enter a valid number.")
    
    # Ask about wavelength range
    use_range = input("\nRestrict wavelength range? (y/n): ").lower().startswith('y')
    wavelength_range = None
    
    if use_range:
        while True:
            try:
                min_nm = float(input("  Minimum wavelength (nm): "))
                max_nm = float(input("  Maximum wavelength (nm): "))
                if min_nm < max_nm:
                    wavelength_range = (min_nm, max_nm)
                    break
                else:
                    print("    Minimum must be less than maximum.")
            except ValueError:
                print("    Please enter valid numbers.")
    
    # Ask about display unit
    display_unit = input("\nDisplay units (nm/cm): ").lower()
    if display_unit not in ['nm', 'cm']:
        display_unit = 'nm'
    
    # Ask about saving
    save_file = input("\nSave plot to file? (Enter filename or press Enter to skip): ").strip()
    if not save_file:
        save_file = None
    
    return {
        'csv_file': csv_file,
        'n_gaussians': n_gaussians,
        'initial_peaks': initial_peaks,
        'peak_units': units if use_initial else None,
        'wavelength_range': wavelength_range,
        'display_unit': display_unit,
        'save_file': save_file
    }

def build_command(params):
    """Build the command to run."""
    cmd = ['python', 'uvvis_gaussian_fit.py', params['csv_file'], str(params['n_gaussians'])]
    
    if params['initial_peaks']:
        if params['peak_units'] == 'cm':
            cmd.extend(['--initial_peaks_cm'] + [str(p) for p in params['initial_peaks']])
        else:
            cmd.extend(['--initial_peaks'] + [str(p) for p in params['initial_peaks']])
    
    if params['wavelength_range']:
        cmd.extend(['--range_nm', str(params['wavelength_range'][0]), str(params['wavelength_range'][1])])
    
    if params['display_unit'] != 'nm':
        cmd.extend(['--display_unit', params['display_unit']])
    
    if params['save_file']:
        cmd.extend(['--save', params['save_file']])
    
    return cmd

def main():
    """Main interactive function."""
    try:
        # Get user preferences
        params = get_user_input()
        
        # Build and display command
        cmd = build_command(params)
        print(f"\nRunning command:")
        print(' '.join(cmd))
        print("\n" + "=" * 50)
        
        # Run the command
        os.system(' '.join(cmd))
        
        print("\n" + "=" * 50)
        print("Analysis complete!")
        
    except KeyboardInterrupt:
        print("\n\nAnalysis cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
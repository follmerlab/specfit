#!/usr/bin/env python3
"""
UV-Vis Spectrum Gaussian Fitting Tool

This script converts UV-vis spectrum data from wavelength (nm) to wavenumbers (cm⁻¹),
fits multiple Gaussians to the data, and displays the results with options for
different visualization units.

Usage:
    python uvvis_gaussian_fit.py <csv_file> <n_gaussians> [options]

Example:
    python uvvis_gaussian_fit.py DEM_848_spectrum.csv 3 --initial_peaks 25000 20000 15000
    python uvvis_gaussian_fit.py DEM_848_spectrum.csv 2 --range_nm 300 700
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import argparse
import sys


class UVVisGaussianFitter:
    def __init__(self, csv_file):
        """Initialize with CSV file containing wavelength (nm) and absorbance data."""
        self.data = pd.read_csv(csv_file, header=None, names=['wavelength_nm', 'absorbance'])
        self.wavelength_nm = None
        self.wavenumber_cm = None
        self.absorbance = None
        self.fit_params = None
        self.fit_result = None
        
    def nm_to_wavenumber(self, wavelength_nm):
        """Convert wavelength in nm to wavenumber in cm⁻¹."""
        return 1e7 / wavelength_nm  # 10^7 nm*cm⁻¹ / nm = cm⁻¹
    
    def wavenumber_to_nm(self, wavenumber_cm):
        """Convert wavenumber in cm⁻¹ to wavelength in nm."""
        return 1e7 / wavenumber_cm
    
    def prepare_data(self, range_nm=None):
        """
        Prepare data for fitting by converting to wavenumbers and filtering range.
        
        Parameters:
        -----------
        range_nm : tuple, optional
            (min_nm, max_nm) to restrict fitting range
        """
        # Sort by wavelength (ascending)
        self.data = self.data.sort_values('wavelength_nm')
        
        # Apply wavelength range filter if specified
        if range_nm:
            min_nm, max_nm = range_nm
            mask = (self.data['wavelength_nm'] >= min_nm) & (self.data['wavelength_nm'] <= max_nm)
            self.data = self.data[mask].copy()
        
        # Extract arrays
        self.wavelength_nm = self.data['wavelength_nm'].values
        self.absorbance = self.data['absorbance'].values
        
        # Convert to wavenumbers (this will reverse the order since nm and cm⁻¹ are inversely related)
        self.wavenumber_cm = self.nm_to_wavenumber(self.wavelength_nm)
        
        # Sort by wavenumber for fitting (ascending order)
        sort_indices = np.argsort(self.wavenumber_cm)
        self.wavenumber_cm = self.wavenumber_cm[sort_indices]
        self.absorbance = self.absorbance[sort_indices]
        self.wavelength_nm = self.wavelength_nm[sort_indices]
        
        print(f"Data range: {self.wavenumber_cm.min():.0f} - {self.wavenumber_cm.max():.0f} cm⁻¹")
        print(f"             ({self.wavelength_nm.max():.0f} - {self.wavelength_nm.min():.0f} nm)")
    
    def gaussian(self, x, amplitude, center, width):
        """Single Gaussian function."""
        return amplitude * np.exp(-(x - center)**2 / (2 * width**2))
    
    def multi_gaussian(self, x, *params):
        """Multiple Gaussian function. Parameters: [amp1, center1, width1, amp2, center2, width2, ...]"""
        n_gaussians = len(params) // 3
        result = np.zeros_like(x)
        
        for i in range(n_gaussians):
            amp = params[i*3]
            center = params[i*3 + 1]
            width = params[i*3 + 2]
            result += self.gaussian(x, amp, center, width)
        
        return result
    
    def generate_initial_guess(self, n_gaussians, initial_peaks_wavenumber=None):
        """
        Generate initial parameter guess for fitting.
        
        Parameters:
        -----------
        n_gaussians : int
            Number of Gaussians to fit
        initial_peaks_wavenumber : list, optional
            List of initial peak positions in cm⁻¹
        
        Returns:
        --------
        list : Initial parameter guess [amp1, center1, width1, amp2, center2, width2, ...]
        """
        # Estimate peak positions
        if initial_peaks_wavenumber:
            if len(initial_peaks_wavenumber) != n_gaussians:
                raise ValueError(f"Number of initial peaks ({len(initial_peaks_wavenumber)}) "
                               f"must match number of gaussians ({n_gaussians})")
            centers = initial_peaks_wavenumber
        else:
            # Distribute evenly across the wavenumber range
            centers = np.linspace(self.wavenumber_cm.min(), self.wavenumber_cm.max(), n_gaussians)
        
        # Estimate other parameters
        max_abs = np.max(self.absorbance)
        width_estimate = (self.wavenumber_cm.max() - self.wavenumber_cm.min()) / (n_gaussians * 4)
        
        # Build parameter list: [amp, center, width] for each Gaussian
        initial_guess = []
        for center in centers:
            initial_guess.extend([max_abs / n_gaussians, center, width_estimate])
        
        return initial_guess
    
    def fit_gaussians(self, n_gaussians, initial_peaks_wavenumber=None):
        """
        Fit multiple Gaussians to the data.
        
        Parameters:
        -----------
        n_gaussians : int
            Number of Gaussians to fit
        initial_peaks_wavenumber : list, optional
            List of initial peak positions in cm⁻¹
        """
        initial_guess = self.generate_initial_guess(n_gaussians, initial_peaks_wavenumber)
        
        # Set parameter bounds (amplitudes > 0, reasonable widths)
        n_params = len(initial_guess)
        lower_bounds = []
        upper_bounds = []
        
        for i in range(n_gaussians):
            lower_bounds.extend([0, self.wavenumber_cm.min(), 100])  # amp > 0, center in range, width > 100 cm⁻¹
            upper_bounds.extend([np.inf, self.wavenumber_cm.max(), 10000])  # reasonable upper limits
        
        try:
            # Perform the fit
            popt, pcov = curve_fit(
                self.multi_gaussian, 
                self.wavenumber_cm, 
                self.absorbance,
                p0=initial_guess,
                bounds=(lower_bounds, upper_bounds),
                maxfev=10000
            )
            
            self.fit_params = popt
            
            # Calculate fit quality metrics
            fit_values = self.multi_gaussian(self.wavenumber_cm, *popt)
            r_squared = 1 - np.sum((self.absorbance - fit_values)**2) / np.sum((self.absorbance - np.mean(self.absorbance))**2)
            rmse = np.sqrt(np.mean((self.absorbance - fit_values)**2))
            
            self.fit_result = {
                'r_squared': r_squared,
                'rmse': rmse,
                'n_gaussians': n_gaussians,
                'parameters': self._format_parameters(popt, n_gaussians)
            }
            
            print(f"\nFit Results:")
            print(f"R² = {r_squared:.4f}")
            print(f"RMSE = {rmse:.4f}")
            print(f"\nGaussian Parameters:")
            for i, params in enumerate(self.fit_result['parameters']):
                print(f"Gaussian {i+1}:")
                print(f"  Center: {params['center_cm']:.0f} cm⁻¹ ({params['center_nm']:.1f} nm)")
                print(f"  Amplitude: {params['amplitude']:.4f}")
                print(f"  Width: {params['width_cm']:.0f} cm⁻¹ ({params['width_nm']:.1f} nm)")
            
        except Exception as e:
            print(f"Fitting failed: {e}")
            self.fit_params = None
            self.fit_result = None
    
    def _format_parameters(self, params, n_gaussians):
        """Format fit parameters into readable structure."""
        formatted = []
        for i in range(n_gaussians):
            amp = params[i*3]
            center_cm = params[i*3 + 1]
            width_cm = params[i*3 + 2]
            
            formatted.append({
                'amplitude': amp,
                'center_cm': center_cm,
                'center_nm': self.wavenumber_to_nm(center_cm),
                'width_cm': width_cm,
                'width_nm': abs(self.wavenumber_to_nm(center_cm + width_cm/2) - self.wavenumber_to_nm(center_cm - width_cm/2))
            })
        
        return formatted
    
    def plot_results(self, display_unit='nm', save_figure=None):
        """
        Plot the original data, fit, and individual Gaussians.
        
        Parameters:
        -----------
        display_unit : str
            'nm' or 'cm' for x-axis units
        save_figure : str, optional
            Filename to save the plot
        """
        if self.fit_params is None:
            print("No fit results to plot. Run fit_gaussians() first.")
            return
        
        # Choose x-axis data based on display unit
        if display_unit == 'nm':
            x_data = self.wavelength_nm
            x_label = 'Wavelength (nm)'
            # Create fine grid for smooth plotting
            x_fine = np.linspace(self.wavelength_nm.min(), self.wavelength_nm.max(), 1000)
            x_fine_wavenumber = self.nm_to_wavenumber(x_fine)
        else:  # cm⁻¹
            x_data = self.wavenumber_cm
            x_label = 'Wavenumber (cm⁻¹)'
            x_fine = np.linspace(self.wavenumber_cm.min(), self.wavenumber_cm.max(), 1000)
            x_fine_wavenumber = x_fine
        
        # Calculate fit and individual Gaussians on fine grid
        fit_fine = self.multi_gaussian(x_fine_wavenumber, *self.fit_params)
        
        # Set up the plot
        plt.figure(figsize=(12, 8))
        
        # Plot original data
        plt.plot(x_data, self.absorbance, 'ko-', markersize=3, linewidth=0.5, 
                label='Original Data', alpha=0.7)
        
        # Plot overall fit
        plt.plot(x_fine, fit_fine, 'r-', linewidth=2, 
                label=f'Sum of {self.fit_result["n_gaussians"]} Gaussians')
        
        # Plot individual Gaussians
        n_gaussians = self.fit_result['n_gaussians']
        colors = plt.cm.tab10(np.linspace(0, 1, n_gaussians))
        
        for i in range(n_gaussians):
            # Extract parameters for this Gaussian
            amp = self.fit_params[i*3]
            center = self.fit_params[i*3 + 1]
            width = self.fit_params[i*3 + 2]
            
            # Calculate this Gaussian on fine grid
            gaussian_fine = self.gaussian(x_fine_wavenumber, amp, center, width)
            
            plt.plot(x_fine, gaussian_fine, '--', color=colors[i], linewidth=1.5,
                    label=f'Gaussian {i+1}: {center:.0f} cm⁻¹')
        
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel('Absorbance', fontsize=12)
        plt.title(f'UV-Vis Spectrum Gaussian Fit (R² = {self.fit_result["r_squared"]:.4f})', fontsize=14)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_figure:
            plt.savefig(save_figure, dpi=300, bbox_inches='tight')
            print(f"Figure saved as: {save_figure}")
        
        plt.show()


def main():
    parser = argparse.ArgumentParser(
        description='Fit UV-Vis spectrum with multiple Gaussians',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s spectrum.csv 3
  %(prog)s spectrum.csv 2 --initial_peaks 400 500
  %(prog)s spectrum.csv 2 --initial_peaks_cm 25000 20000
  %(prog)s spectrum.csv 3 --range_nm 300 700 --display_unit cm --save plot.png
        """
    )
    
    parser.add_argument('csv_file', help='CSV file with wavelength (nm) and absorbance data')
    parser.add_argument('n_gaussians', type=int, help='Number of Gaussians to fit')
    parser.add_argument('--initial_peaks', nargs='+', type=float, 
                       help='Initial peak positions in wavelength (nm)')
    parser.add_argument('--initial_peaks_cm', nargs='+', type=float, 
                       help='Initial peak positions in wavenumber (cm⁻¹)')
    parser.add_argument('--range_nm', nargs=2, type=float, metavar=('MIN', 'MAX'),
                       help='Wavelength range to consider (nm)')
    parser.add_argument('--display_unit', choices=['nm', 'cm'], default='nm',
                       help='Display unit for final plot (default: nm)')
    parser.add_argument('--save', type=str, help='Save plot to file')
    
    args = parser.parse_args()
    
    # Validate inputs
    if args.initial_peaks and args.initial_peaks_cm:
        print("Error: Cannot specify both --initial_peaks (nm) and --initial_peaks_cm (cm⁻¹)")
        sys.exit(1)
    
    initial_peaks_provided = args.initial_peaks or args.initial_peaks_cm
    if initial_peaks_provided and len(initial_peaks_provided) != args.n_gaussians:
        print(f"Error: Number of initial peaks ({len(initial_peaks_provided)}) "
              f"must match number of Gaussians ({args.n_gaussians})")
        sys.exit(1)
    
    try:
        # Initialize fitter
        fitter = UVVisGaussianFitter(args.csv_file)
        
        # Prepare data
        print(f"Loading data from: {args.csv_file}")
        fitter.prepare_data(range_nm=args.range_nm)
        
        # Convert initial peaks from nm to wavenumber if provided in nm
        initial_peaks_wavenumber = None
        if args.initial_peaks:
            initial_peaks_wavenumber = [fitter.nm_to_wavenumber(nm) for nm in args.initial_peaks]
            print(f"Initial peaks: {args.initial_peaks} nm → {[f'{wn:.0f}' for wn in initial_peaks_wavenumber]} cm⁻¹")
        elif args.initial_peaks_cm:
            initial_peaks_wavenumber = args.initial_peaks_cm
            print(f"Initial peaks: {args.initial_peaks_cm} cm⁻¹")
        
        # Fit Gaussians
        print(f"\nFitting {args.n_gaussians} Gaussians...")
        fitter.fit_gaussians(args.n_gaussians, initial_peaks_wavenumber)
        
        # Plot results
        if fitter.fit_params is not None:
            fitter.plot_results(display_unit=args.display_unit, save_figure=args.save)
        
    except FileNotFoundError:
        print(f"Error: Could not find file '{args.csv_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
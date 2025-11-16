# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-16

### Added
- Initial release of UV-Vis Gaussian Fitter
- Core fitting functionality with multiple Gaussian peaks
- Automatic wavelength to wavenumber conversion
- Support for initial peak position specification (nm or cm⁻¹)
- Wavelength range restriction option
- Dual display units (nm or cm⁻¹)
- Fit quality metrics (R² and RMSE)
- Plot export functionality
- Interactive quickstart script
- Comprehensive README with examples
- Example usage script

### Features
- Command-line interface with argparse
- Flexible parameter bounds for robust fitting
- Visual output with individual Gaussian components
- High-resolution plot saving (PNG, PDF, etc.)

## [Unreleased]

### Planned
- Unit tests
- Support for other peak shapes (Lorentzian, Voigt)
- Batch processing of multiple files
- JSON export of fit parameters
- Interactive GUI option
- Peak deconvolution tools

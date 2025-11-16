# UV-Vis Spectrum Gaussian Fitting Tool

A Python tool for analyzing UV-Vis spectroscopy data by converting wavelengths to wavenumbers, fitting multiple Gaussian peaks, and visualizing the results.

## Features

- **Automatic unit conversion**: Converts wavelength (nm) to wavenumber (cm⁻¹) for fitting
- **Multiple Gaussian fitting**: Fit any number of Gaussian peaks to your spectrum
- **Flexible initial conditions**: Specify initial peak positions or use automatic distribution
- **Range restriction**: Analyze only a specific wavelength range of your spectrum
- **Dual visualization**: View results in either wavelength (nm) or wavenumber (cm⁻¹) units
- **Fit quality metrics**: Get R² and RMSE values for fit assessment
- **Export capabilities**: Save high-resolution plots of your results

## Installation

1. **Clone or download** this repository to your local machine

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install numpy pandas matplotlib scipy
   ```

## Input Data Format

The tool expects a CSV file with two columns (no headers):
1. **Column 1**: Wavelength in nanometers (nm)
2. **Column 2**: Absorbance values

Example:
```
1100.011719,0.007490207
1099.009399,-0.019240458
1098.006226,-0.004369807
...
```

## Usage

### Basic Syntax
```bash
python uvvis_gaussian_fit.py <csv_file> <n_gaussians> [options]
```

### Parameters

- **`csv_file`**: Path to your CSV data file
- **`n_gaussians`**: Number of Gaussian peaks to fit (integer)

### Options

- **`--initial_peaks PEAK1 PEAK2 ...`**: Specify initial peak positions in wavelength (nm)
- **`--initial_peaks_cm PEAK1 PEAK2 ...`**: Specify initial peak positions in wavenumber (cm⁻¹)
- **`--range_nm MIN MAX`**: Restrict analysis to wavelength range (nm)
- **`--display_unit {nm,cm}`**: Choose display unit for final plot (default: nm)
- **`--save FILENAME`**: Save plot to file (PNG, PDF, etc.)

## Examples

### 1. Basic Usage - Automatic Peak Distribution
```bash
python uvvis_gaussian_fit.py spectrum.csv 3
```
Fits 3 Gaussians with automatically distributed initial peak positions.

### 2. Specify Initial Peak Positions (Wavelength)
```bash
python uvvis_gaussian_fit.py spectrum.csv 2 --initial_peaks 400 500
```
Fits 2 Gaussians with initial centers at 400 and 500 nm.

### 2b. Specify Initial Peak Positions (Wavenumber)
```bash
python uvvis_gaussian_fit.py spectrum.csv 2 --initial_peaks_cm 25000 20000
```
Fits 2 Gaussians with initial centers at 25,000 and 20,000 cm⁻¹.

### 3. Analyze Specific Wavelength Range
```bash
python uvvis_gaussian_fit.py spectrum.csv 3 --range_nm 300 700
```
Only analyzes data between 300-700 nm, fitting 3 Gaussians.

### 4. Display in Wavenumber Units
```bash
python uvvis_gaussian_fit.py spectrum.csv 2 --display_unit cm
```
Shows the final plot with wavenumber (cm⁻¹) on the x-axis.

### 5. Save High-Resolution Plot
```bash
python uvvis_gaussian_fit.py spectrum.csv 3 --save my_spectrum_fit.png
```
Saves the result plot as a high-resolution PNG file.

### 6. Complete Example
```bash
python uvvis_gaussian_fit.py spectrum.csv 3 \
  --initial_peaks 360 450 625 \
  --range_nm 350 650 \
  --display_unit nm \
  --save spectrum_analysis.pdf
```

## Output Information

The tool provides detailed output including:

### Fit Quality Metrics
- **R²**: Coefficient of determination (closer to 1.0 = better fit)
- **RMSE**: Root mean square error (smaller = better fit)

### Gaussian Parameters
For each fitted Gaussian:
- **Center**: Peak position in both cm⁻¹ and nm
- **Amplitude**: Peak height (absorbance units)
- **Width**: Peak width in both cm⁻¹ and nm

### Visual Output
- Original data points
- Sum of all Gaussians (fitted curve)
- Individual Gaussian components
- Fit quality metrics in plot title

## Tips for Best Results

### Choosing Number of Gaussians
- Start with fewer Gaussians (2-3) and increase if needed
- Too many Gaussians may lead to overfitting
- Use physical/chemical knowledge to guide the choice

### Initial Peak Positions
- Examine your spectrum visually to identify approximate peak positions
- **Easy method**: Use `--initial_peaks` with wavelengths in nm (e.g., 400 500 600)
- **Advanced method**: Use `--initial_peaks_cm` with wavenumbers in cm⁻¹
- Conversion: wavenumber = 10,000,000 / wavelength_nm (e.g., 500 nm → 20,000 cm⁻¹)

### Wavelength Range Selection
- Exclude noisy regions at spectrum edges
- Focus on the region of interest for your analysis
- Ensure sufficient data points for reliable fitting

### Troubleshooting Poor Fits
- Try different initial peak positions
- Adjust the number of Gaussians
- Check data quality and remove outliers if necessary
- Consider if Gaussian peaks are appropriate for your system

## Example Workflow

1. **Examine your data**:
   ```bash
   # Quick visual inspection
   python -c "import pandas as pd; import matplotlib.pyplot as plt; 
   data=pd.read_csv('spectrum.csv', header=None); 
   plt.plot(data[0], data[1]); plt.show()"
   ```

2. **Start with basic fit**:
   ```bash
   python uvvis_gaussian_fit.py spectrum.csv 2
   ```

3. **Refine based on results**:
   ```bash
   python uvvis_gaussian_fit.py spectrum.csv 3 --initial_peaks 25000 20000 15000
   ```

4. **Final analysis with range restriction**:
   ```bash
   python uvvis_gaussian_fit.py spectrum.csv 3 \
     --initial_peaks 25000 20000 15000 \
     --range_nm 400 800 \
     --save final_analysis.png
   ```

## Understanding the Mathematics

### Unit Conversion
- **Wavelength to Wavenumber**: ν̃ = 10⁷/λ (cm⁻¹ = 10⁷ nm·cm⁻¹ / nm)
- **Wavenumber to Wavelength**: λ = 10⁷/ν̃ (nm = 10⁷ nm·cm⁻¹ / cm⁻¹)

### Gaussian Function
Each Gaussian peak is defined as:
```
G(ν̃) = A × exp(-(ν̃ - ν̃₀)²/(2σ²))
```
Where:
- A = amplitude (peak height)
- ν̃₀ = center position (cm⁻¹)
- σ = width parameter (cm⁻¹)

### Multi-Gaussian Fit
The total spectrum is the sum of individual Gaussians:
```
S(ν̃) = Σ Aᵢ × exp(-(ν̃ - ν̃₀ᵢ)²/(2σᵢ²))
```

## File Structure

```
uvvis_convertfit/
├── uvvis_gaussian_fit.py    # Main analysis script
├── requirements.txt         # Python dependencies
├── examples.py             # Usage examples
├── README.md              # This documentation
└── spectrum.csv            # Example data file
```

## Support and Contributing

If you encounter issues or have suggestions for improvements:
1. Check that your CSV file format matches the expected structure
2. Verify all dependencies are installed correctly
3. Try simpler cases first (fewer Gaussians, no range restrictions)

## License

This tool is provided as-is for scientific and educational use.
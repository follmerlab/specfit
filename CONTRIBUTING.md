# Contributing to UV-Vis Gaussian Fitter

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear title and description
- Steps to reproduce the issue
- Expected vs. actual behavior
- Your environment (Python version, OS)
- Sample data if applicable (anonymized if needed)

### Suggesting Features

We welcome feature suggestions! Please open an issue with:
- A clear description of the feature
- Use case and motivation
- Example of how it would work

### Pull Requests

1. **Fork the repository** and create a new branch for your feature or bugfix
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

3. **Test your changes**
   - Ensure existing functionality still works
   - Test with different input files and parameters
   - Consider edge cases

4. **Commit your changes**
   ```bash
   git commit -m "Add feature: description of your change"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Explain why the change is needed

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/follmerlab/uvvis-gaussian-fitter.git
   cd uvvis-gaussian-fitter
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run tests (if you add them):
   ```bash
   python -m pytest
   ```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

## Documentation

- Update README.md if you add new features
- Add examples for new functionality
- Comment complex algorithms or calculations

## Questions?

Feel free to open an issue for any questions or clarifications.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

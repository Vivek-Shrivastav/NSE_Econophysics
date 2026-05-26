# Contributing to NSE Econophysics Dashboard

Thank you for your interest in contributing! This project bridges statistical physics and financial markets, and we welcome contributions from both communities.

## How to Contribute

### Reporting Issues

- **Bug reports**: Open an issue with steps to reproduce, expected vs actual behaviour, and your Python version
- **Feature requests**: Describe the analysis you'd like to see and its physics/finance motivation
- **Documentation**: Suggest improvements to plot explanations or add new educational content

### Code Contributions

1. **Fork** the repository
2. **Create a branch** for your feature (`git checkout -b feature/my-feature`)
3. **Make your changes** following the code style below
4. **Test** your changes with at least 2–3 different NSE stocks
5. **Submit a Pull Request** with a clear description

### Code Style

- Python code follows PEP 8 (with the exception of line length — we allow up to 120 characters)
- All analysis functions should be pure: input data → output results (no side effects)
- Plots should use the established colour scheme (`STOCK_COLOR`, `REF_COLOR`, `CMAP_BSP`)
- New plots should include a title following the numbered convention (① ② ③...)
- Add docstrings to all public functions

### Documentation

If you add a new plot or analysis:
1. Add a section to `docs/UNDERSTANDING_THE_PLOTS.md` following the existing format
2. Include: one-liner, plain English explanation, going deeper section, diagnosis guide
3. Reference the relevant chapter in Mantegna & Stanley (1999) or Sharma et al. (2025)
4. Use dual vocabulary (physics term + finance equivalent)

### Areas for Contribution

- **New analysis methods**: Wavelet analysis, multifractal spectra, Hurst exponent
- **Additional markets**: BSE, international indices
- **Performance**: Optimising bispectrum computation for large datasets
- **Visualisation**: Interactive plots (Plotly, D3.js)
- **Testing**: Unit tests for core analysis functions
- **Mobile UI**: Responsive improvements to the dashboard

## Development Setup

```bash
git clone https://github.com/Vivek-Shrivastav/NSE_Econophysics.git
cd NSE_Econophysics
pip install -r requirements.txt
python nse_dashboard.py
```

## Questions?

Open an issue or reach out — we're happy to help you get started.

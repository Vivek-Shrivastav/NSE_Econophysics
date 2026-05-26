<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/NSE-India-FF6600?style=for-the-badge" alt="NSE India"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License"/>
  <img src="https://img.shields.io/badge/arXiv-2508.20105-b31b1b?style=for-the-badge&logo=arxiv" alt="arXiv"/>
</p>

<h1 align="center">
  🌊 NSE Econophysics Dashboard
</h1>

<p align="center">
  <strong>Applying turbulence physics to decode the hidden structure of Indian stock markets</strong>
</p>

<p align="center">
  <a href="https://nse-econophysics.onrender.com/">
    <img src="https://img.shields.io/badge/Live%20Demo-Available%20Here-success?style=for-the-badge&logo=render" alt="Live Demo">
  </a>
</p>

<p align="center">
  <em>Does a stock's price behave like fully-developed turbulence in a fluid — or does it contain hidden structure planted by coordinated actors?</em>
</p>

---

## 🔬 What Is This?

This is an interactive web dashboard that analyses any NSE (National Stock Exchange of India) stock through the lens of **econophysics** — the application of statistical physics methods to financial markets.

It implements the analytical framework from two key sources:

> **Mantegna, R.N. & Stanley, H.E. (1999)** — *An Introduction to Econophysics: Correlations and Complexity in Finance*, Cambridge University Press

> **Sharma, Dutta & Mukherjee (2025)** — *Identification of Phase Correlations in Financial Stock Market Turbulence*, [arXiv:2508.20105](https://arxiv.org/abs/2508.20105)

The dashboard fetches any NSE stock's historical data, compares it against the **Nifty 50** index as a reference, and runs a **five-stage analysis pipeline** producing **9 plots** plus a summary stats panel.

---

## 🚀 Quick Start

### One-command launch

```bash
python nse_dashboard.py
```

That's it. The dashboard opens automatically at **http://localhost:8080**. All dependencies (`yfinance`, `numpy`, `scipy`, `matplotlib`, `pandas`, `rapidfuzz`) are auto-installed on first run.

### Requirements

- **Python 3.8+** (tested on 3.9, 3.10, 3.11, 3.12)
- Internet connection (for fetching live NSE data from Yahoo Finance)
- No API keys needed

### Manual installation (optional)

```bash
# Clone the repository
git clone https://github.com/Vivek-Shrivastav/NSE_Econophysics.git
cd NSE_Econophysics

# Install dependencies
pip install -r requirements.txt

# Launch
python nse_dashboard.py
```

---

## 📊 The Analysis Pipeline

The dashboard runs a five-stage pipeline on any NSE stock:

```
Stage 1: Time Domain    → Normalised prices, log-returns, rolling volatility
Stage 2: Distribution   → Fat-tail analysis, Gaussian vs Student-t fitting
Stage 3: Normality Test → Q-Q plots revealing departure from Gaussian
Stage 4: Frequency      → FFT power spectrum, turbulence exponent α
Stage 5: Phase Coupling → Bispectrum analysis, turbulence classification
```

### The Nine Plots

| # | Plot | What It Reveals |
|---|------|-----------------|
| ① | **Time-Domain Analysis** | Normalised price comparison, log-returns, rolling volatility |
| ② | **Return Distribution** | Fat tails — how often extreme events occur vs. Gaussian prediction |
| ③ | **Q-Q Plot** | Visual normality test — the S-curve reveals fat tails |
| ④ | **FFT Power Spectrum** | Turbulence exponent α — compared to Kolmogorov's −5/3 law |
| ⑤ | **Spectrum Overlay** | Direct spectral comparison between stock and Nifty 50 |
| ⑥ | **Bispectrum Heatmap** | Phase coupling detection — the "fingerprint" of hidden structure |
| ⑦ | **Bispectrum Cross-Sections** | 1D slices through the bispectrum for precise frequency analysis |
| ⑧ | **Turbulence Classification** | Final verdict — fully-developed turbulence or phase coupling? |
| ⑨ | **Master Dashboard** | All-in-one summary diagnostic figure |

> 📖 For detailed explanations of every plot, see **[docs/UNDERSTANDING_THE_PLOTS.md](docs/UNDERSTANDING_THE_PLOTS.md)**

---

## 🎓 Educational Resources

This repository includes two educational components:

### 1. Plot Explanations Guide

📄 **[docs/UNDERSTANDING_THE_PLOTS.md](docs/UNDERSTANDING_THE_PLOTS.md)** — A comprehensive, beginner-friendly guide that explains every single plot with:
- **Dual vocabulary**: every physics term includes its finance equivalent
- **Plain English explanations** before any math
- **Diagnosis guides**: "if you see THIS shape → it means THIS"
- **Indian market examples** (Reliance, TCS, HDFC Bank, Nifty 50)

### 2. Interactive Econophysics Textbook

📄 **[claude_peda.html](claude_peda.html)** — An interactive HTML textbook covering all 15 chapters of Mantegna & Stanley's book, with:
- Interactive simulations (random walks, Lévy flights, GARCH)
- Quiz questions with instant feedback
- Beautiful typography and visualisations
- Progress tracking across chapters

Open it in any browser — no server needed.

---

## 🏗️ Project Structure

```
nse-econophysics/
├── nse_dashboard.py          # Main application (Python + HTTP server)
├── dashboard.html            # Dashboard frontend (HTML/CSS/JS)
├── claude_peda.html          # Interactive econophysics textbook
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License
├── .gitignore                # Git ignore rules
├── CONTRIBUTING.md           # Contribution guidelines
├── docs/
│   └── UNDERSTANDING_THE_PLOTS.md   # Detailed plot explanations
└── notebooks/
    └── combined_nse_analysis.ipynb   # Jupyter notebook (full analysis)
```

---

## 🔑 Key Concepts

### The Turbulence Analogy

The central idea: **financial markets and turbulent fluids share the same statistical fingerprint**.

In a turbulent fluid (a river rapid, a jet engine exhaust), large eddies break into smaller eddies in a self-similar cascade. Kolmogorov (1941) showed that this produces a power spectrum with a precise slope of **−5/3**.

This dashboard tests whether NSE stock prices exhibit the same spectral signature — and goes further by using **bispectral analysis** to detect hidden phase correlations that turbulent systems lack.

### What the Bispectrum Reveals

The standard power spectrum tells you *how much* energy is at each frequency. The bispectrum tells you whether specific frequency pairs are **talking to each other** — a sign of non-random, structured information flow.

- **Flat bispectrum** → Fully-developed turbulence → Consistent with efficient markets
- **Bright spots** → Phase coupling → Structured trading patterns at specific time scales
- **Sharma et al. (2025)** found that Infosys showed pronounced bispectrum spikes during 2015–2022, while most other NSE stocks showed flat bispectra

---

## 📚 References

1. **Mantegna, R.N. & Stanley, H.E.** (1999). *An Introduction to Econophysics: Correlations and Complexity in Finance*. Cambridge University Press.

2. **Sharma, K., Dutta, S. & Mukherjee, S.** (2025). *Identification of Phase Correlations in Financial Stock Market Turbulence*. arXiv:2508.20105.

3. **Kolmogorov, A.N.** (1941). *The local structure of turbulence in incompressible viscous fluid for very large Reynolds numbers*. Doklady Akademii Nauk SSSR, 30, 301–305.

4. **Mandelbrot, B.** (1963). *The variation of certain speculative prices*. Journal of Business, 36(4), 394–419.

5. **Kim, Y.C. & Powers, E.J.** (1979). *Digital bispectral analysis and its applications to nonlinear wave interactions*. IEEE Transactions on Plasma Science, 7(2), 120–131.

6. **Fama, E.F.** (1970). *Efficient Capital Markets: A Review of Theory and Empirical Work*. Journal of Finance, 25(2), 383–417.

---

## ⚠️ Disclaimer

This dashboard is a **research and educational tool**. It is NOT financial advice.

- The turbulence classification is NOT a trading signal
- Phase coupling does not necessarily imply market manipulation
- Past statistical properties do not guarantee future behaviour
- Always consult qualified financial advisors for investment decisions

---

## 📝 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

<p align="center">
  <sub>Built with 🧪 physics + 📈 finance + 🐍 Python</sub>
</p>

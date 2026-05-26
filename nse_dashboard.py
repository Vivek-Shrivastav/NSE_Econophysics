#!/usr/bin/env python3
"""
NSE Econophysics Dashboard
==========================
Run:   python nse_dashboard.py
Then open  http://localhost:8080  in your browser (it opens automatically).

No extra setup needed — all dependencies are installed automatically on first run.
"""

import json, http.server, socketserver, threading, webbrowser, io, base64
import os, re, sys, subprocess, warnings
from urllib.parse import urlparse

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
#  Auto-install missing dependencies
# ─────────────────────────────────────────────────────────────────────────────
def _pip(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

for _pkg in ["yfinance", "rapidfuzz", "numpy", "scipy", "matplotlib", "pandas"]:
    try:
        __import__(_pkg.replace("-", "_"))
    except ImportError:
        print(f"  Installing {_pkg}…")
        _pip(_pkg)

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")            # headless – no display window required
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LogNorm
from scipy import stats
import yfinance as yf
from rapidfuzz import fuzz, process as rfprocess

# ─────────────────────────────────────────────────────────────────────────────
#  Company resolver  (identical logic to the notebook)
# ─────────────────────────────────────────────────────────────────────────────
_SUFFIX_RE = re.compile(r"\b(ltd|limited|inc|corp|corporation|plc|pvt|private)\b")

def _normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[._\-+]", " ", text)
    text = re.sub(r"[^a-z0-9&\s]", "", text)
    text = _SUFFIX_RE.sub("", text)
    return re.sub(r"\s+", " ", text).strip()

_COMPANY_MAP: dict[str, str] = {
    "abbotindia":"ABBOTINDIA","abbott india":"ABBOTINDIA",
    "aartiind":"AARTIIND","aarti industries":"AARTIIND","aarti":"AARTIIND",
    "adaniports":"ADANIPORTS","adani ports":"ADANIPORTS",
    "adanient":"ADANIENT","adani enterprises":"ADANIENT",
    "adanigreen":"ADANIGREEN","adani green":"ADANIGREEN",
    "adanipower":"ADANIPOWER","adani power":"ADANIPOWER",
    "alkem":"ALKEM","alkem labs":"ALKEM","alkem laboratories":"ALKEM",
    "apollohosp":"APOLLOHOSP","apollo hospitals":"APOLLOHOSP","apollo":"APOLLOHOSP",
    "apollotyre":"APOLLOTYRE","apollo tyre":"APOLLOTYRE","apollo tyres":"APOLLOTYRE",
    "asianpaint":"ASIANPAINT","asian paints":"ASIANPAINT","asian paint":"ASIANPAINT","asian":"ASIANPAINT",
    "auropharma":"AUROPHARMA","aurobindo pharma":"AUROPHARMA","aurobindo":"AUROPHARMA",
    "axisbank":"AXISBANK","axis bank":"AXISBANK","axis":"AXISBANK",
    "bajaj-auto":"BAJAJ-AUTO","bajaj auto":"BAJAJ-AUTO",
    "bajajfinsv":"BAJAJFINSV","bajaj finserv":"BAJAJFINSV",
    "bajfinance":"BAJFINANCE","bajaj finance":"BAJFINANCE","bajaj fin":"BAJFINANCE",
    "bandhanbnk":"BANDHANBNK","bandhan bank":"BANDHANBNK","bandhan":"BANDHANBNK",
    "bankbaroda":"BANKBARODA","bank of baroda":"BANKBARODA","bob":"BANKBARODA",
    "bergepaint":"BERGEPAINT","berger paints":"BERGEPAINT","berger":"BERGEPAINT",
    "bhel":"BHEL","bharat heavy electricals":"BHEL",
    "biocon":"BIOCON",
    "bpcl":"BPCL","bharat petroleum":"BPCL",
    "britannia":"BRITANNIA",
    "canbk":"CANBK","canara bank":"CANBK","canara":"CANBK",
    "cipla":"CIPLA",
    "coalindia":"COALINDIA","coal india":"COALINDIA",
    "colpal":"COLPAL","colgate palmolive":"COLPAL","colgate":"COLPAL",
    "cumminsind":"CUMMINSIND","cummins india":"CUMMINSIND","cummins":"CUMMINSIND",
    "dabur":"DABUR",
    "deepakntr":"DEEPAKNTR","deepak nitrite":"DEEPAKNTR","deepak":"DEEPAKNTR",
    "divislab":"DIVISLAB","divis labs":"DIVISLAB","divis":"DIVISLAB",
    "dmart":"DMART","avenue supermarts":"DMART",
    "drreddy":"DRREDDY","dr reddys":"DRREDDY","dr reddy":"DRREDDY",
    "eichermot":"EICHERMOT","eicher motors":"EICHERMOT","eicher":"EICHERMOT",
    "emamiltd":"EMAMILTD","emami":"EMAMILTD",
    "federalbnk":"FEDERALBNK","federal bank":"FEDERALBNK",
    "fsn":"FSN","nykaa":"FSN",
    "glenmark":"GLENMARK",
    "godrejcp":"GODREJCP","godrej consumer":"GODREJCP","godrej":"GODREJCP",
    "grasim":"GRASIM",
    "hcltech":"HCLTECH","hcl technologies":"HCLTECH","hcl tech":"HCLTECH","hcl":"HCLTECH",
    "hdfcbank":"HDFCBANK","hdfc bank":"HDFCBANK","hdfc":"HDFCBANK",
    "hdfcamc":"HDFCAMC","hdfc amc":"HDFCAMC",
    "hdfclife":"HDFCLIFE","hdfc life":"HDFCLIFE",
    "heromotoco":"HEROMOTOCO","hero motocorp":"HEROMOTOCO","hero":"HEROMOTOCO",
    "hindalco":"HINDALCO",
    "hindunilvr":"HINDUNILVR","hindustan unilever":"HINDUNILVR","hul":"HINDUNILVR",
    "icicibank":"ICICIBANK","icici bank":"ICICIBANK","icici":"ICICIBANK",
    "idfcfirstb":"IDFCFIRSTB","idfc first bank":"IDFCFIRSTB","idfc first":"IDFCFIRSTB",
    "indigo":"INDIGO","interglobe aviation":"INDIGO","interglobe":"INDIGO",
    "indusindbk":"INDUSINDBK","indusind bank":"INDUSINDBK","indusind":"INDUSINDBK",
    "infy":"INFY","infosys":"INFY",
    "irctc":"IRCTC","irfc":"IRFC","itc":"ITC",
    "jswsteel":"JSWSTEEL","jsw steel":"JSWSTEEL",
    "kotakbank":"KOTAKBANK","kotak mahindra bank":"KOTAKBANK","kotak":"KOTAKBANK",
    "lt":"LT","l&t":"LT","larsen and toubro":"LT","larsen toubro":"LT","larsen":"LT",
    "ltim":"LTIM","ltimindtree":"LTIM","lti mindtree":"LTIM",
    "lupin":"LUPIN",
    "m&m":"M&M","mahindra and mahindra":"M&M","mahindra mahindra":"M&M",
    "marico":"MARICO",
    "maruti":"MARUTI","maruti suzuki":"MARUTI",
    "mrf":"MRF",
    "muthootfin":"MUTHOOTFIN","muthoot finance":"MUTHOOTFIN","muthoot":"MUTHOOTFIN",
    "nestleind":"NESTLEIND","nestle india":"NESTLEIND","nestle":"NESTLEIND",
    "ntpc":"NTPC","ongc":"ONGC",
    "pageind":"PAGEIND","page industries":"PAGEIND",
    "paytm":"PAYTM","pfizer":"PFIZER",
    "pidilitind":"PIDILITIND","pidilite industries":"PIDILITIND","pidilite":"PIDILITIND",
    "pnb":"PNB","punjab national bank":"PNB",
    "policybzr":"POLICYBZR","policybazaar":"POLICYBZR",
    "powergrid":"POWERGRID","power grid":"POWERGRID",
    "rblbank":"RBLBANK","rbl bank":"RBLBANK",
    "reliance":"RELIANCE","reliance industries":"RELIANCE","ril":"RELIANCE",
    "sbin":"SBIN","sbi":"SBIN","state bank of india":"SBIN","state bank":"SBIN",
    "sbilife":"SBILIFE","sbi life":"SBILIFE",
    "shreecem":"SHREECEM","shree cement":"SHREECEM",
    "spicejet":"SPICEJET","srf":"SRF",
    "sunpharma":"SUNPHARMA","sun pharma":"SUNPHARMA","sun pharmaceutical":"SUNPHARMA",
    "suntv":"SUNTV","sun tv":"SUNTV",
    "tatamotors":"TATAMOTORS","tata motors":"TATAMOTORS",
    "tatapower":"TATAPOWER","tata power":"TATAPOWER",
    "tatasteel":"TATASTEEL","tata steel":"TATASTEEL",
    "tcs":"TCS","tata consultancy services":"TCS","tata consultancy":"TCS","tata consult":"TCS",
    "techm":"TECHM","tech mahindra":"TECHM",
    "titan":"TITAN",
    "torntpharm":"TORNTPHARM","torrent pharma":"TORNTPHARM",
    "torntpower":"TORNTPOWER","torrent power":"TORNTPOWER",
    "ultracemco":"ULTRACEMCO","ultratech cement":"ULTRACEMCO","ultratech":"ULTRACEMCO",
    "upl":"UPL","voltas":"VOLTAS","wipro":"WIPRO",
    "zeel":"ZEEL","zee entertainment":"ZEEL","zee":"ZEEL",
    "zomato":"ZOMATO",
}
for _sym in list(set(_COMPANY_MAP.values())):
    _COMPANY_MAP.setdefault(_sym.lower(), _sym)

_NORM_MAP: dict[str, str] = {}
for _k, _v in _COMPANY_MAP.items():
    _NORM_MAP.setdefault(_normalize(_k), _v)
_ALL_SYMBOLS: set[str] = set(_COMPANY_MAP.values())

def _expand_map(symbol: str, long_name: str = "") -> None:
    symbol = symbol.upper()
    _ALL_SYMBOLS.add(symbol)
    _COMPANY_MAP.setdefault(symbol.lower(), symbol)
    _NORM_MAP.setdefault(symbol.lower(), symbol)
    if long_name:
        nk = _normalize(long_name)
        if nk:
            _COMPANY_MAP.setdefault(nk, symbol)
            _NORM_MAP.setdefault(nk, symbol)

def resolve_company(user_input: str) -> tuple[str, str]:
    """Return (symbol, message) where message is a human-readable note."""
    raw = user_input.strip()
    if raw.upper() in _ALL_SYMBOLS:
        return raw.upper(), f"Resolved: {raw.upper()}"
    norm = _normalize(raw)
    if norm in _NORM_MAP:
        return _NORM_MAP[norm], f"Resolved: {_NORM_MAP[norm]}"
    if norm.upper() in _ALL_SYMBOLS:
        return norm.upper(), f"Resolved: {norm.upper()}"
    norm_keys = list(_NORM_MAP.keys())
    r1 = rfprocess.extract(norm, norm_keys, scorer=fuzz.WRatio, limit=5)
    r2 = rfprocess.extract(norm, norm_keys, scorer=fuzz.token_sort_ratio, limit=5)
    scores: dict[str, float] = {}
    for alias, score, _ in r1 + r2:
        scores[alias] = max(scores.get(alias, 0.0), float(score))
    norm_tokens = set(norm.split())
    for alias in norm_keys:
        overlap = len(norm_tokens & set(alias.split()))
        if overlap:
            scores[alias] = min(100.0, scores.get(alias, 0.0) + overlap * 12)
    if not scores:
        return raw.upper(), f"Could not resolve — using '{raw.upper()}' directly"
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    best_alias, best_score = ranked[0]
    best_sym = _NORM_MAP[best_alias]
    if best_score >= 90:
        return best_sym, f"Resolved: {best_sym}"
    elif best_score >= 60:
        return best_sym, f"Assuming you meant: {best_sym} (confidence {best_score:.0f}%)"
    else:
        return best_sym, f"Low confidence — using best match: {best_sym}"

# ─────────────────────────────────────────────────────────────────────────────
#  Plot helpers
# ─────────────────────────────────────────────────────────────────────────────
STOCK_COLOR = "#e31a1c"
REF_COLOR   = "#1f78b4"
CMAP_BSP    = "inferno"

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "#f8f9fa",
    "axes.grid": True, "grid.alpha": 0.35, "grid.linestyle": "--",
    "font.family": "DejaVu Sans", "axes.titlesize": 13,
    "axes.labelsize": 11, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "legend.fontsize": 9, "legend.framealpha": 0.85, "figure.dpi": 110,
})

def _fig_to_b64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=130)
    plt.close(fig)
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode()

# ─────────────────────────────────────────────────────────────────────────────
#  Core analysis
# ─────────────────────────────────────────────────────────────────────────────
def load_series(path: str, col: str = "Close") -> pd.Series:
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="first")]
    return df[col].dropna()

def power_spectrum(series: pd.Series):
    x = series.values.astype(float)
    x = (x - x.mean()) / (x.std() + 1e-12)
    F = np.fft.rfft(x)
    pw = np.abs(F) ** 2
    fr = np.fft.rfftfreq(len(x))
    return fr[1:], pw[1:]

def log_bin(freq, power, n_bins=40):
    if len(freq) == 0:
        return np.array([]), np.array([])
    bins = np.logspace(np.log10(freq[0]+1e-20), np.log10(freq[-1]+1e-20), n_bins + 1)
    f_bin, p_bin = [], []
    for lo, hi in zip(bins[:-1], bins[1:]):
        mask = (freq >= lo) & (freq < hi)
        if mask.sum() > 0:
            f_bin.append(freq[mask].mean())
            p_bin.append(power[mask].mean())
    return np.array(f_bin), np.array(p_bin)

def fit_power_law(freq, power, lo_frac=0.05, hi_frac=0.6):
    if len(freq) == 0:
        return 0.0, 0.0, np.array([])
    mask = (freq > freq[0] + lo_frac*(freq[-1]-freq[0])) & \
           (freq < freq[0] + hi_frac*(freq[-1]-freq[0]))
    if mask.sum() < 3:
        mask = np.ones(len(freq), dtype=bool)
    lf, lp = np.log10(freq[mask]+1e-20), np.log10(power[mask]+1e-20)
    slope, intercept = np.polyfit(lf, lp, 1)
    return slope, intercept, freq[mask]

def compute_bispectrum(signal: np.ndarray, n_modes: int = 80, n_segments: int = 6) -> np.ndarray:
    N = len(signal)
    if N < n_segments * 2:
        return np.zeros((n_modes, n_modes), dtype=float)
    seg = N // n_segments
    n   = min(n_modes, seg // 2)
    BSP_acc = np.zeros((n, n), dtype=np.float64)
    for s in range(n_segments):
        chunk = signal[s * seg: (s + 1) * seg].copy()
        chunk = (chunk - chunk.mean()) / (chunk.std() + 1e-12)
        F = np.fft.fft(chunk)
        for i in range(n):
            j_max = min(n, len(F) - i)
            j_vec = np.arange(i, j_max)
            k_vec = i + j_vec
            vals  = np.abs(F[i] * F[j_vec] * np.conj(F[k_vec]))
            BSP_acc[i, i:j_max] += vals
            BSP_acc[i:j_max, i] += vals
        BSP_acc[np.diag_indices(n)] /= 2
    BSP_avg = BSP_acc / n_segments
    mx = BSP_avg.max()
    return (BSP_avg / mx) if mx > 0 else BSP_avg

def phase_coupling_score(BSP: np.ndarray, top_frac: float = 0.01) -> float:
    flat  = BSP.flatten()
    top_k = max(1, int(len(flat) * top_frac))
    top_v = np.partition(flat, -top_k)[-top_k:]
    return float(top_v.mean() / (flat.mean() + 1e-12))

def classify(score: float) -> tuple[str, str]:
    if score < 3.0:
        return "Fully-developed turbulence ✓", "#d4edda"
    elif score < 6.0:
        return "Weak phase coupling ⚡", "#fff3cd"
    else:
        return "Strong phase coupling ⚠", "#f8d7da"

# ─────────────────────────────────────────────────────────────────────────────
#  Main analysis entry point — returns JSON-serialisable dict
# ─────────────────────────────────────────────────────────────────────────────
def run_analysis(company: str, start: str, end: str, interval: str) -> dict:
    symbol, resolve_msg = resolve_company(company)
    ticker = f"{symbol}.NS"

    # ── Fetch stock data ──────────────────────────────────────────────────────
    df = yf.download(ticker, start=start, end=end, interval=interval,
                     auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    if df.empty:
        return {"error": f"No data found for '{symbol}' ({ticker}). "
                         "Check the symbol / date range and try again."}

    stock_price = df["Close"].dropna()
    stock_price.index = pd.to_datetime(stock_price.index)

    # Try to get official name
    try:
        info = yf.Ticker(ticker).info
        long_name = info.get("longName") or info.get("shortName", symbol)
        _expand_map(symbol, long_name)
    except Exception:
        long_name = symbol

    # ── Fetch Nifty 50 reference ──────────────────────────────────────────────
    nifty_raw = yf.download("^NSEI", start=start, end=end, interval=interval,
                             auto_adjust=True, progress=False)
    if isinstance(nifty_raw.columns, pd.MultiIndex):
        nifty_raw.columns = nifty_raw.columns.get_level_values(0)
    nifty_price = nifty_raw["Close"].dropna()
    nifty_price.index = pd.to_datetime(nifty_price.index)

    # Align
    common_idx  = stock_price.index.intersection(nifty_price.index)
    stock_price = stock_price.loc[common_idx]
    nifty_price = nifty_price.loc[common_idx]

    if len(common_idx) < 10:
        return {"error": "Not enough overlapping data points. Try a wider date range."}

    # ── Derived series ────────────────────────────────────────────────────────
    stock_norm = stock_price / stock_price.iloc[0] * 100
    nifty_norm = nifty_price / nifty_price.iloc[0] * 100
    stock_ret  = np.log(stock_price / stock_price.shift(1)).dropna()
    nifty_ret  = np.log(nifty_price / nifty_price.shift(1)).dropna()
    roll_win   = max(20, len(stock_ret) // 30)
    stock_vol  = stock_ret.rolling(roll_win).std() * np.sqrt(252)
    nifty_vol  = nifty_ret.rolling(roll_win).std() * np.sqrt(252)

    # ── FFT ───────────────────────────────────────────────────────────────────
    s_freq, s_pow = power_spectrum(stock_price)
    n_freq, n_pow = power_spectrum(nifty_price)
    sb_freq, sb_pow = log_bin(s_freq, s_pow)
    nb_freq, nb_pow = log_bin(n_freq, n_pow)
    s_slope, s_int, s_fit_f = fit_power_law(sb_freq, sb_pow)
    n_slope, n_int, n_fit_f = fit_power_law(nb_freq, nb_pow)

    # ── Bispectrum ────────────────────────────────────────────────────────────
    N_MODES = min(80, len(stock_price) // 12)
    N_SEGS  = 6
    BSP_stock = compute_bispectrum(stock_price.values, N_MODES, N_SEGS)
    BSP_nifty = compute_bispectrum(nifty_price.values, N_MODES, N_SEGS)
    score_s   = phase_coupling_score(BSP_stock)
    score_n   = phase_coupling_score(BSP_nifty)
    s_verdict, s_col = classify(score_s)
    n_verdict, n_col = classify(score_n)

    plots = []

    # ── Plot 1: Time Domain ───────────────────────────────────────────────────
    fig, axes = plt.subplots(3, 1, figsize=(14, 11), sharex=True,
                             gridspec_kw={"height_ratios": [2.5, 2, 2]})
    fig.suptitle(f"① Time-Domain Analysis  |  {symbol}  vs  Nifty 50",
                 fontsize=14, fontweight="bold", y=1.01)
    ax = axes[0]
    ax.plot(nifty_norm.index, nifty_norm.values, color=REF_COLOR, lw=1.4, alpha=0.85, label="Nifty 50")
    ax.plot(stock_norm.index, stock_norm.values, color=STOCK_COLOR, lw=1.4, alpha=0.90, label=symbol)
    ax.fill_between(stock_norm.index, nifty_norm.values, stock_norm.values,
                    where=(stock_norm.values >= nifty_norm.values), alpha=0.10, color=STOCK_COLOR)
    ax.fill_between(stock_norm.index, nifty_norm.values, stock_norm.values,
                    where=(stock_norm.values < nifty_norm.values), alpha=0.10, color=REF_COLOR)
    ax.set_ylabel("Normalised Price (Base=100)"); ax.legend(loc="upper left")
    ax.set_title("Normalised Price — both rebased to 100 at start of period")
    ax = axes[1]
    ax.axhline(0, color="grey", lw=0.8, ls="--")
    ax.plot(nifty_ret.index, nifty_ret.values, color=REF_COLOR, lw=0.7, alpha=0.65, label="Nifty 50")
    ax.plot(stock_ret.index, stock_ret.values, color=STOCK_COLOR, lw=0.7, alpha=0.80, label=symbol)
    ax.set_ylabel("Log-Return r(t)"); ax.legend(loc="upper left")
    ax.set_title("Daily Log-Returns   r(t) = ln[P(t) / P(t−1)]")
    ax = axes[2]
    ax.plot(nifty_vol.index, nifty_vol.values * 100, color=REF_COLOR, lw=1.3, alpha=0.85, label="Nifty 50")
    ax.plot(stock_vol.index, stock_vol.values * 100, color=STOCK_COLOR, lw=1.3, alpha=0.90, label=symbol)
    ax.set_ylabel(f"Annualised Volatility (%)\n(rolling {roll_win}-day)"); ax.set_xlabel("Date")
    ax.set_title(f"Rolling Annualised Volatility  (window = {roll_win} days)"); ax.legend(loc="upper left")
    plt.tight_layout()
    plots.append({"title": "① Time-Domain Analysis", "img": _fig_to_b64(fig)})

    # ── Plot 2: Return Distribution ───────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"② Return Distribution & Fat Tails  |  {symbol}  vs  Nifty 50",
                 fontsize=14, fontweight="bold")
    bins = max(10, min(60, len(stock_ret) // 10))
    for ax, ret, name, col in [
            (axes[0], stock_ret, symbol, STOCK_COLOR),
            (axes[1], nifty_ret, "Nifty 50", REF_COLOR)]:
        mu, sigma = ret.mean(), ret.std()
        x_range   = np.linspace(ret.min(), ret.max(), 300)
        gauss     = stats.norm.pdf(x_range, mu, sigma)
        ax.hist(ret, bins=bins, density=True, color=col, alpha=0.45, edgecolor="white", linewidth=0.4, label="Empirical")
        ax.plot(x_range, gauss, color="black", lw=2.0, ls="--",
                label=f"Gaussian  μ={mu:.4f}, σ={sigma:.4f}")
        nu, t_loc, t_scale = stats.t.fit(ret)
        ax.plot(x_range, stats.t.pdf(x_range, nu, t_loc, t_scale),
                color="darkorange", lw=2.0, ls="-.", label=f"Student-t  ν={nu:.1f}")
        kurt = stats.kurtosis(ret)
        skew = stats.skew(ret)
        ax.set_title(f"{name}\nKurtosis = {kurt:.2f}   Skewness = {skew:.2f}")
        ax.set_xlabel("Log-Return r(t)"); ax.set_ylabel("Probability Density")
        ax.legend()
        if not np.isnan(sigma) and sigma > 0:
            ax.set_xlim(mu - 6*sigma, mu + 6*sigma)
        sign = "FAT TAILS" if kurt > 1.0 else ("near-Normal" if kurt < 0.5 else "moderate tails")
        ax.text(0.97, 0.97, sign, transform=ax.transAxes, ha="right", va="top",
                fontsize=9, color="darkred",
                bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", ec="grey", alpha=0.8))
    plt.tight_layout()
    plots.append({"title": "② Return Distribution & Fat Tails", "img": _fig_to_b64(fig)})

    # ── Plot 3: Q-Q Plot ──────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("③ Q-Q Plot vs Normal  (deviation from line = fat tails)",
                 fontsize=13, fontweight="bold")
    for ax, ret, name, col in [
            (axes[0], stock_ret, symbol, STOCK_COLOR),
            (axes[1], nifty_ret, "Nifty 50", REF_COLOR)]:
        (osm, osr), (slope, intercept, _r) = stats.probplot(ret, dist="norm")
        ax.plot(osm, osr, "o", ms=2.5, color=col, alpha=0.6, label="Data")
        ax.plot(osm, slope*np.array(osm)+intercept, color="black", lw=2, ls="--", label="Gaussian")
        ax.set_title(f"{name}"); ax.set_xlabel("Theoretical Quantiles"); ax.set_ylabel("Sample Quantiles")
        ax.legend()
    plt.tight_layout()
    plots.append({"title": "③ Q-Q Plot (Normality Test)", "img": _fig_to_b64(fig)})

    # ── Plot 4: Power Spectrum ────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f"④ FFT Power Spectrum  |  {symbol}  vs  Nifty 50",
                 fontsize=13, fontweight="bold")
    for ax_i, (rf, rp, rbf, rbp, slope, intercept, fit_f, name, col) in enumerate([
        (s_freq, s_pow, sb_freq, sb_pow, s_slope, s_int, s_fit_f, symbol, STOCK_COLOR),
        (n_freq, n_pow, nb_freq, nb_pow, n_slope, n_int, n_fit_f, "Nifty 50", REF_COLOR),
    ]):
        ax_obj = axes[ax_i]
        ax_obj.loglog(rf, rp, color=col, alpha=0.20, lw=0.6)
        ax_obj.loglog(rbf, rbp, "o-", color=col, ms=4, lw=1.8, alpha=0.90, label=f"{name} (log-binned)")
        if len(fit_f) > 0:
            fit_line = 10**(intercept + slope * np.log10(fit_f+1e-20))
            ax_obj.loglog(fit_f, fit_line, color="black", lw=2.0, ls="--",
                          label=f"Fit: α = {-slope:.2f}")
        if len(rbf) > 2:
            kol_ref = rp.max() * (rbf / (rbf[0]+1e-20)) ** (-5/3) * 0.5
            ax_obj.loglog(rbf, kol_ref, color="grey", lw=1.2, ls=":", label="Kolmogorov −5/3")
        ax_obj.set_xlabel("Frequency ω"); ax_obj.set_ylabel("|F(ω)|² Power")
        ax_obj.set_title(f"{name}\nPower-law exponent  α = {-slope:.2f}")
        ax_obj.legend()
        ax_obj.text(0.03, 0.05,
            f"Turbulence exponent\n  α = {-slope:.2f}\n  (Kolmogorov: 5/3 ≈ 1.67)",
            transform=ax_obj.transAxes, fontsize=8.5, va="bottom",
            bbox=dict(boxstyle="round,pad=0.4", fc="lightyellow", ec="grey", alpha=0.85))
    plt.tight_layout()
    plots.append({"title": "④ FFT Power Spectrum (Turbulence Spectrum)", "img": _fig_to_b64(fig)})

    # ── Plot 5: Spectrum overlay ──────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_title(f"⑤ Power Spectrum Comparison  |  {symbol}  vs  Nifty 50  (log–log)",
                 fontsize=13, fontweight="bold")
    ax.loglog(sb_freq, sb_pow, "o-", color=STOCK_COLOR, ms=4, lw=1.8, label=symbol)
    ax.loglog(nb_freq, nb_pow, "s-", color=REF_COLOR,   ms=4, lw=1.8, label="Nifty 50")
    if len(s_fit_f) > 0:
        ax.loglog(s_fit_f, 10**(s_int + s_slope * np.log10(s_fit_f+1e-20)),
                  color=STOCK_COLOR, lw=1.5, ls="--", alpha=0.6, label=f"{symbol} fit α={-s_slope:.2f}")
    if len(n_fit_f) > 0:
        ax.loglog(n_fit_f, 10**(n_int + n_slope * np.log10(n_fit_f+1e-20)),
                  color=REF_COLOR, lw=1.5, ls="--", alpha=0.6, label=f"Nifty fit α={-n_slope:.2f}")
    if len(sb_freq) > 3:
        kol_x = np.array([sb_freq[2], sb_freq[-3]])
        kol_y = sb_pow[2] * (kol_x / kol_x[0]) ** (-5/3)
        ax.loglog(kol_x, kol_y, "k:", lw=1.5, label="Kolmogorov −5/3 guide")
    ax.set_xlabel("Frequency ω"); ax.set_ylabel("|F(ω)|²"); ax.legend(ncol=2)
    plt.tight_layout()
    plots.append({"title": "⑤ Power Spectrum Overlay (Both Stocks)", "img": _fig_to_b64(fig)})

    # ── Plot 6: Bispectrum heatmaps ───────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f"⑥ Bispectrum (Phase Coupling)  |  {symbol}  vs  Nifty 50",
                 fontsize=13, fontweight="bold")
    for ax_idx, (BSP, name, col, score, verdict) in enumerate([
            (BSP_stock, symbol, STOCK_COLOR, score_s, s_verdict),
            (BSP_nifty, "Nifty 50", REF_COLOR, score_n, n_verdict)]):
        ax = axes[ax_idx]
        _n = BSP.shape[0]
        mask = np.zeros_like(BSP)
        mask[np.tril_indices(_n, k=-1)] = np.nan
        im = ax.imshow(BSP + mask, origin="lower", aspect="equal",
                       cmap=CMAP_BSP, vmin=0, vmax=1, extent=[0, _n, 0, _n])
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04).set_label("Normalised |P|", fontsize=9)
        ax.set_xlabel("Fourier mode ωα"); ax.set_ylabel("Fourier mode ωβ")
        ax.set_title(f"{name}\nPhase-coupling score = {score:.3f}", fontsize=12)
        fc_c = "#fff3cd" if score > 3.0 else "#d4edda"
        tc_c = "darkred"  if score > 3.0 else "darkgreen"
        ax.text(0.97, 0.97, verdict, transform=ax.transAxes, ha="right", va="top",
                fontsize=9, color=tc_c, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.4", fc=fc_c, ec="grey", alpha=0.90))
    plt.tight_layout()
    plots.append({"title": "⑥ Bispectrum Heatmap (Phase Coupling)", "img": _fig_to_b64(fig)})

    # ── Plot 7: Bispectrum cross-sections ─────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"⑦ Bispectrum Cross-Sections  |  {symbol}  vs  Nifty 50",
                 fontsize=13, fontweight="bold")
    n_rows = min(5, BSP_stock.shape[0] // 4)
    row_indices = np.linspace(2, BSP_stock.shape[0] - 2, n_rows, dtype=int)
    for ax_idx in range(2):
        ax = axes[ax_idx]
        for ri, ridx in enumerate(row_indices):
            alpha_val = 0.5 + 0.5 * (ri / len(row_indices))
            ax.plot(BSP_stock[ridx, ridx:], color=STOCK_COLOR, lw=1.2,
                    alpha=alpha_val * 0.9,
                    label=f"{symbol}" if ri == 0 else "_nolegend_")
            ax.plot(BSP_nifty[ridx, ridx:], color=REF_COLOR, lw=1.2,
                    alpha=alpha_val * 0.9, ls="--",
                    label="Nifty 50" if ri == 0 else "_nolegend_")
        ax.set_xlabel("Fourier mode ωβ"); ax.set_ylabel("|P(ωα, ωβ)| (normalised)")
        ax.set_title(f"Row-slices (ωα from {row_indices[0]} to {row_indices[-1]})\n"
                     f"Stock = solid    Nifty = dashed")
        ax.legend()
    plt.tight_layout()
    plots.append({"title": "⑦ Bispectrum Cross-Sections", "img": _fig_to_b64(fig)})

    # ── Plot 8: Turbulence classification ─────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.bar([symbol, "Nifty 50"], [score_s, score_n],
                  color=[STOCK_COLOR, REF_COLOR], alpha=0.75,
                  edgecolor="black", linewidth=1.2, width=0.4)
    ax.axhline(3.0, color="darkorange", ls="--", lw=1.8, label="Weak-coupling threshold (3.0)")
    ax.axhline(6.0, color="darkred", ls=":", lw=1.8, label="Strong-coupling threshold (6.0)")
    for bar, score, verdict in zip(bars, [score_s, score_n], [s_verdict, n_verdict]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f"{score:.3f}", ha="center", va="bottom", fontweight="bold", fontsize=11)
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
                verdict.split("  ")[0], ha="center", va="center",
                fontsize=8.5, color="white", fontweight="bold")
    ax.set_ylabel("Phase-Coupling Score")
    ax.set_title("⑧ Turbulence Classification — Bispectrum Phase-Coupling Score",
                 fontsize=13, fontweight="bold")
    ax.legend(loc="upper right")
    ax.set_ylim(0, max(score_s, score_n) * 1.3 + 1)
    plt.tight_layout()
    plots.append({"title": "⑧ Turbulence Classification", "img": _fig_to_b64(fig)})

    # ── Plot 9: Master Dashboard ──────────────────────────────────────────────
    fig = plt.figure(figsize=(18, 14))
    fig.suptitle(f"NSE Econophysics Master Dashboard\n{symbol}  vs  Nifty 50",
                 fontsize=15, fontweight="bold", y=1.01)
    gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.45, wspace=0.38)

    ax_price = fig.add_subplot(gs[0, :3])
    ax_price.plot(nifty_norm.index, nifty_norm.values, color=REF_COLOR, lw=1.2, alpha=0.85, label="Nifty 50")
    ax_price.plot(stock_norm.index, stock_norm.values, color=STOCK_COLOR, lw=1.4, alpha=0.90, label=symbol)
    ax_price.set_ylabel("Normalised Price (base=100)"); ax_price.set_title("① Normalised Price")
    ax_price.legend(); ax_price.xaxis.set_tick_params(rotation=20)

    ax_dist = fig.add_subplot(gs[0, 3])
    bins2 = max(10, min(50, len(stock_ret) // 8))
    ax_dist.hist(nifty_ret, bins=bins2, density=True, color=REF_COLOR, alpha=0.40, label="Nifty 50")
    ax_dist.hist(stock_ret, bins=bins2, density=True, color=STOCK_COLOR, alpha=0.50, label=symbol)
    x_r = np.linspace(stock_ret.min(), stock_ret.max(), 200)
    ax_dist.plot(x_r, stats.norm.pdf(x_r, stock_ret.mean(), stock_ret.std()), "k--", lw=1.5, label="Gaussian")
    ax_dist.set_xlabel("Log-Return"); ax_dist.set_ylabel("Density"); ax_dist.set_title("② Distribution")
    ax_dist.legend(fontsize=7)

    ax_ret = fig.add_subplot(gs[1, :2])
    ax_ret.axhline(0, color="grey", lw=0.7, ls="--")
    ax_ret.plot(nifty_ret.index, nifty_ret.values, color=REF_COLOR, lw=0.6, alpha=0.65, label="Nifty 50")
    ax_ret.plot(stock_ret.index, stock_ret.values, color=STOCK_COLOR, lw=0.7, alpha=0.80, label=symbol)
    ax_ret.set_ylabel("Log-Return r(t)"); ax_ret.set_title("③ Log-Returns"); ax_ret.legend()
    ax_ret.xaxis.set_tick_params(rotation=20)

    ax_fft = fig.add_subplot(gs[1, 2:])
    ax_fft.loglog(sb_freq, sb_pow, "o-", color=STOCK_COLOR, ms=3, lw=1.4, label=symbol)
    ax_fft.loglog(nb_freq, nb_pow, "s-", color=REF_COLOR, ms=3, lw=1.4, label="Nifty 50")
    ax_fft.set_xlabel("Frequency ω"); ax_fft.set_ylabel("|F(ω)|²")
    ax_fft.set_title(f"④ Power Spectrum\nα: {symbol}={-s_slope:.2f} | Nifty={-n_slope:.2f}")
    ax_fft.legend(fontsize=7)

    ax_bs = fig.add_subplot(gs[2, :2])
    _n = BSP_stock.shape[0]
    ms = np.zeros_like(BSP_stock); ms[np.tril_indices(_n, k=-1)] = np.nan
    im1 = ax_bs.imshow(BSP_stock + ms, origin="lower", aspect="equal",
                       cmap=CMAP_BSP, vmin=0, vmax=1, extent=[0, _n, 0, _n])
    fig.colorbar(im1, ax=ax_bs, fraction=0.046, pad=0.04)
    ax_bs.set_xlabel("ωα"); ax_bs.set_ylabel("ωβ")
    ax_bs.set_title(f"⑤ Bispectrum  {symbol}\nScore = {score_s:.3f}  |  {s_verdict.split('  ')[0]}")

    ax_bn = fig.add_subplot(gs[2, 2:])
    _n2 = BSP_nifty.shape[0]
    mn = np.zeros_like(BSP_nifty); mn[np.tril_indices(_n2, k=-1)] = np.nan
    im2 = ax_bn.imshow(BSP_nifty + mn, origin="lower", aspect="equal",
                       cmap=CMAP_BSP, vmin=0, vmax=1, extent=[0, _n2, 0, _n2])
    fig.colorbar(im2, ax=ax_bn, fraction=0.046, pad=0.04)
    ax_bn.set_xlabel("ωα"); ax_bn.set_ylabel("ωβ")
    ax_bn.set_title(f"⑥ Bispectrum  Nifty 50\nScore = {score_n:.3f}  |  {n_verdict.split('  ')[0]}")
    plt.tight_layout()
    plots.append({"title": "⑨ Master Dashboard (All-in-One)", "img": _fig_to_b64(fig)})

    # ── Summary stats ─────────────────────────────────────────────────────────
    summary = {
        "symbol": symbol,
        "long_name": long_name,
        "resolve_msg": resolve_msg,
        "period_start": str(common_idx[0].date()),
        "period_end":   str(common_idx[-1].date()),
        "points":       len(common_idx),
        "stock_final":  round(float(stock_norm.iloc[-1]), 2),
        "nifty_final":  round(float(nifty_norm.iloc[-1]), 2),
        "stock_vol_pct": round(float(stock_vol.iloc[-1] * 100), 2),
        "nifty_vol_pct": round(float(nifty_vol.iloc[-1] * 100), 2),
        "stock_kurt":   round(float(stats.kurtosis(stock_ret)), 2),
        "nifty_kurt":   round(float(stats.kurtosis(nifty_ret)), 2),
        "stock_alpha":  round(float(-s_slope), 3),
        "nifty_alpha":  round(float(-n_slope), 3),
        "stock_score":  round(float(score_s), 3),
        "nifty_score":  round(float(score_n), 3),
        "stock_verdict": s_verdict,
        "nifty_verdict": n_verdict,
    }
    return {"plots": plots, "summary": summary}

# ─────────────────────────────────────────────────────────────────────────────
#  Embedded HTML
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_file(filename: str) -> str:
    path = os.path.join(BASE_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# ─────────────────────────────────────────────────────────────────────────────
#  HTTP handler
# ─────────────────────────────────────────────────────────────────────────────
class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # suppress console noise

    def do_GET(self):
        if self.path == "/" or self.path == "/book.html":
            content = _load_file("book.html")
        elif self.path == "/dashboard_ui":
            content = _load_file("dashboard.html")
        else:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode())

    def do_POST(self):
        if urlparse(self.path).path != "/analyze":
            self.send_response(404); self.end_headers(); return
        length = int(self.headers.get("Content-Length", 0))
        body   = json.loads(self.rfile.read(length))
        try:
            result = run_analysis(
                body.get("company", ""),
                body.get("start", ""),
                body.get("end", ""),
                body.get("interval", "1d"),
            )
        except Exception as e:
            result = {"error": str(e)}
        payload = json.dumps(result).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

# ─────────────────────────────────────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8080))
    print("=" * 60)
    print("  NSE Econophysics Dashboard")
    print("=" * 60)
    print(f"  Starting server on  http://localhost:{PORT}")
    print("  Press  Ctrl+C  to stop.\n")

    # Open browser after a short delay
    def _open():
        import time; time.sleep(1.2)
        webbrowser.open(f"http://localhost:{PORT}")
    threading.Thread(target=_open, daemon=True).start()

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.allow_reuse_address = True
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Server stopped. Goodbye!")

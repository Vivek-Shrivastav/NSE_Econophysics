# NSE Econophysics for Beginners — Understanding Your Plots

> *"The same mathematics that describes a tornado ripping through Kansas can describe a crash ripping through Dalal Street."*
>
> This guide walks you through every plot the dashboard produces. Whether you're a physics student, a commerce graduate, or a self-taught coder staring at nine colourful panels — by the end of this document, you'll know exactly what each one means.

---

## Before You Start: Three Foundational Ideas

Before we touch a single plot, you need three concepts. Everything else builds on them.

### 1. Log-Returns — The "Natural Variable" of Market Physics

Imagine you bought Reliance at ₹2,000 and it rose to ₹2,100. A simple return says +5%. But what if it then fell back to ₹2,000? The simple return for the second day is −4.76%, not −5%. Simple returns are asymmetric — they don't add up neatly over time.

A **log-return** fixes this. It is defined as r(t) = ln[P(t) / P(t−1)], where P(t) is today's closing price and ln is the natural logarithm. Log-returns are additive: the log-return over two days is the sum of the two daily log-returns. In physics, log-returns arise naturally when you model prices as a *multiplicative stochastic process* (a random walk where shocks multiply rather than add). In finance, log-returns connect directly to continuous compounding — the way banks and derivatives desks actually calculate interest and option prices.

Every plot in this dashboard uses log-returns rather than raw prices. Mantegna & Stanley devote Chapter 5 to explaining why this choice is fundamental.

### 2. Nifty 50 as a Reference — Separating the Tide from the Boat

If TCS rose 15% this year, is that impressive? Not if the entire market (Nifty 50) rose 20%. The Nifty 50 index is our **benchmark** — it represents the average behaviour of the 50 largest companies on the NSE.

By always plotting a stock *alongside* the Nifty 50, we separate **systematic risk** (market-wide forces that lift or sink all boats — like RBI rate cuts or global recessions) from **idiosyncratic risk** (company-specific events — like HDFC Bank's quarterly earnings surprise or a pharma company's drug approval). In physics language, we're separating the external driving force from the intrinsic dynamics of the system.

### 3. The Turbulence Analogy — The Heart of This Project

Here is the central philosophical claim: **financial markets and turbulent fluids have the same statistical fingerprint.**

In a turbulent river, large eddies (swirls) break into smaller eddies, which break into even smaller ones. Energy injected at large scales "cascades" down to small scales. The Russian physicist Kolmogorov showed in 1941 that this cascade produces a very specific mathematical signature — the famous **−5/3 power law** in the energy spectrum.

In a stock market, large macroeconomic shocks (an RBI rate decision, a union budget, a pandemic) propagate down to shorter time-scale fluctuations — weekly trends, daily swings, intraday noise. The question this dashboard answers is: *does this cascade look statistically identical to fluid turbulence, or is there hidden structure — a fingerprint of coordinated, non-random information injection?*

Mantegna & Stanley discuss this analogy in Chapter 11. Sharma, Dutta & Mukherjee (2025) quantify it rigorously for NSE stocks using the bispectrum.

---

## The Summary Stats Panel

Before the plots, the dashboard shows eight stat cards. Here's what each one means:

| # | Card | Finance Meaning | Physics Meaning |
|---|------|----------------|-----------------|
| 1 | **Price Performance** | Total percentage gain/loss from start to end of period | Drift of the stochastic process — how far the random walk has drifted from its origin |
| 2 | **Nifty 50 Return** | Benchmark return over the same period | Drift of the reference process |
| 3 | **Relative to Nifty (Alpha)** | Excess return over the benchmark — did the stock beat the market? | Difference in drift between the two processes |
| 4 | **Annualised Volatility %** | Annualised standard deviation of daily returns — the most common risk measure in finance (σ × √252) | The diffusion coefficient (spreading rate) of the Brownian motion model, scaled to annual units |
| 5 | **Excess Kurtosis** | Tail risk indicator — how much fatter the tails are than a bell curve. Values > 3 mean severe crash risk | Fourth standardised cumulant of the distribution — measures how "peaked and fat-tailed" the distribution is relative to a Gaussian |
| 6 | **Power-law Exponent α** | How persistent or structured the return series is across time scales | Spectral slope characterising the turbulence regime; α ≈ 1.67 is Kolmogorov turbulence |
| 7 | **Phase-Coupling Score** | A measure of "hidden structure" in the price dynamics — are certain periodicities locked together? | Normalised bispectrum concentration — ratio of the brightest 1% of bispectrum values to the global mean |
| 8 | **Data Points** | Number of trading days in the analysis window | Sample size for all statistical calculations |

---

## Plot ① — Time-Domain Analysis

### What This Plot Shows
A three-panel snapshot of how the stock's price, returns, and risk evolved over time compared to the Nifty 50.

### The Axes
- **Top panel — Normalised Price.** X-axis: calendar date. Y-axis: price rebased to 100 at the start of the period. Both the stock (red) and Nifty 50 (blue) begin at 100, so the gap between them is pure relative performance. The shaded area is red when the stock is above Nifty, blue when below.
- **Middle panel — Log-Returns.** X-axis: date. Y-axis: daily log-return r(t) = ln[P(t)/P(t−1)]. Values hover around zero; spikes up are big gains, spikes down are big losses.
- **Bottom panel — Rolling Annualised Volatility.** X-axis: date. Y-axis: rolling standard deviation of log-returns multiplied by √252, expressed as a percentage — the finance convention for annualising daily risk. In physics, this is the time-varying diffusion coefficient (spreading rate) of the stochastic process.

### Plain English Explanation
Why do we rebase both lines to 100? Because a ₹5,000 stock (like MRF) and a ₹200 stock (like Tata Power) can't be compared on the same chart without normalisation. Rebasing to 100 lets you directly read off percentage gains: if the red line hits 150, the stock is up 50%.

The middle panel reveals something beautiful and disturbing: large swings cluster together. After COVID hit in March 2020, the daily returns of almost every NSE stock showed a burst of extreme swings — positive and negative — for weeks. Then things calmed down. This phenomenon, called **volatility clustering** (physics: intermittency in turbulence), is one of the most famous empirical facts about financial markets. Mandelbrot documented it in 1963; Engle formalised it in ARCH models in 1982. It means risk is not constant — it comes in storms.

The bottom panel makes volatility clustering visually obvious. Look for periods where the line stays low and flat (calm seas) followed by sudden spikes (a storm). These spikes often correspond to real events — RBI rate decisions, union budgets, global crises.

### Going Deeper (Physics + Finance Theory)
The shaded region between the two normalised-price lines is called **alpha** (finance: excess return over the benchmark) or, in physics terms, the deviation of the stock from the index "attractor." If a stock consistently stays above the Nifty line, it is generating alpha — a fund manager's dream.

The √252 factor in the volatility panel comes from diffusion physics. In a random walk, the standard deviation of displacement grows as √t. Since there are ~252 trading days per year, daily volatility scales up to annual volatility by multiplying by √252. This is identical to the physics of diffusion (Einstein, 1905) — the same √t scaling that governs how ink spreads in water.

Mantegna & Stanley cover volatility in Chapter 7 and ARCH/GARCH models in Chapter 10.

### Diagnosis Guide
| You see… | Physics interpretation | Finance interpretation |
|----------|----------------------|----------------------|
| Stock line rising faster than Nifty | Deviation from index attractor | Outperformance — alpha generation |
| Stock line tracking Nifty closely | Weak coupling to external field | High beta — systematic risk dominates |
| Volatility spike in bottom panel | Intermittency burst (turbulence episode) | Market stress — COVID, budget shock, RBI decision |
| Long calm period → sudden spike | ARCH-type clustering / intermittency | Volatility regime change — risk models need updating |

### Key Takeaway
This plot tells you *what happened* — the story of the stock over time. The next plots ask *why* and *how*.

---

## Plot ② — Return Distribution & Fat Tails

### What This Plot Shows
How often each size of daily gain or loss occurred — and whether extreme events happen more than a bell curve predicts.

### The Axes
- X-axis: daily log-return r(t). Negative values are losses, positive are gains. The centre is near zero (most days are small moves).
- Y-axis: probability density — how often each return value occurs, scaled so the total area under the curve equals 1.
- Black dashed line: the best-fit **Gaussian** (normal / "bell curve") distribution — what returns would look like if they were generated by many small, independent random shocks (Central Limit Theorem).
- Orange dash-dot line: the best-fit **Student-t distribution** — a fatter-tailed alternative with parameter ν (degrees of freedom). Smaller ν = fatter tails. When ν → ∞, it becomes a Gaussian.

### Plain English Explanation
Imagine collecting every single daily return of Reliance for 10 years and plotting how often each size of gain or loss occurred. That histogram IS the return distribution.

If markets were perfectly "textbook" — if every day's price change were driven by thousands of tiny, independent news items — the histogram would follow a perfect bell curve. But real markets don't behave that way. The histogram is typically *taller in the centre* (more "do nothing" days than the Gaussian predicts) and *taller in the extreme tails* (more crashes AND more rallies than the Gaussian predicts). This shape is called **fat tails** (technically: leptokurtosis).

Why does this matter? Because every risk model in a bank's VaR (Value-at-Risk) calculation starts with an assumption about this distribution. If you assume Gaussian tails, you dramatically underestimate the probability of a 5-sigma crash. The 2008 financial crisis was partly caused by exactly this assumption failure.

### Going Deeper (Physics + Finance Theory)
**Kurtosis** (physics: the fourth standardised moment of the distribution) quantifies "tailedness." For a Gaussian, excess kurtosis = 0. A value of 3, 5, or 10 means the distribution has progressively fatter tails. The dashboard prints the excess kurtosis in the title.

**Skewness** (the third standardised moment) measures asymmetry. Negative skewness (the left tail is longer than the right) means the stock experiences larger crashes than rallies — a common feature of equity markets because fear is a stronger force than greed.

The **Student-t distribution** (the orange line) is a practical fat-tail model. It has a parameter ν (degrees of freedom) that controls tail thickness. Banks use it in risk calculations. In physics, it arises as a generalisation of the Gaussian for systems with limited data or heavy-tailed noise.

The fully general fat-tail model is the **Lévy α-stable distribution** (Mantegna & Stanley Chapter 4). It allows for infinite variance when the stability parameter α < 2, which is theoretically elegant but practically inconvenient. The Student-t is a finite-variance approximation that captures most of the relevant behaviour.

Mantegna & Stanley Chapter 3 covers the Gaussian, Chapter 4 covers Lévy processes, and the fat-tail finding for real market data is the central empirical result of Chapter 4.

### Diagnosis Guide
| You see… | Physics interpretation | Finance interpretation |
|----------|----------------------|----------------------|
| Bars taller than Gaussian in centre + taller in tails | Leptokurtic — excess kurtosis > 1 | FAT TAILS — crashes happen more often than models predict |
| Bars roughly follow Gaussian | System near Gaussian equilibrium | Classical finance assumptions approximately valid |
| Strong left asymmetry (skewness < −0.5) | Asymmetric fluctuation distribution | Crash risk exceeds rally potential — risk is one-sided |
| Student-t fits well with low ν (< 5) | Heavy-tailed noise process | Extreme daily moves are "normal" for this stock |

### Key Takeaway
Real stock returns have fatter tails than a bell curve. This means extreme events — crashes and rallies — are far more likely than standard models assume.

---

## Plot ③ — Q-Q Plot (Normality Test)

### What This Plot Shows
A visual stress-test: how badly do the actual returns deviate from a perfect bell curve?

### The Axes
- X-axis: **theoretical quantiles** — where each data point *would* fall if the returns were perfectly Gaussian. (A quantile is just a specific percentile — the 10th percentile is the value below which 10% of returns fall.)
- Y-axis: **sample quantiles** — where each data point *actually* falls in the real data.
- Diagonal reference line: what perfect Gaussian data would look like. If every point sits on this line, the data is Gaussian.

### Plain English Explanation
Think of the Q-Q plot as a "lie detector test" for the bell-curve assumption. We line up every observed return from smallest to largest, and compare each one against where a perfectly Gaussian dataset would have placed it. If the data is truly Gaussian, all the dots lie neatly on the diagonal line. Any deviation from the line is a signal.

The characteristic shape you'll see for most NSE stocks is the **S-curve**: the dots curl *below* the line on the left side (the actual crashes are more extreme than the Gaussian predicts) and *above* the line on the right side (the actual rallies are also more extreme). This is the Q-Q plot's way of shouting "FAT TAILS" — confirming what Plot ② showed as a histogram.

### Going Deeper (Physics + Finance Theory)
The Q-Q plot is a workhorse of statistical hypothesis testing, used in physics whenever you need to check whether experimental data follow a theoretical distribution — for example, testing whether detector noise is Gaussian. Mantegna & Stanley Chapter 5 shows Q-Q plots for S&P 500 returns; our dashboard applies the same analysis to NSE stocks.

For finance practitioners: if your risk model assumes Gaussian returns and the Q-Q plot shows an S-curve, your Value-at-Risk estimates are **underestimating tail risk**. The further the dots deviate from the line at the extremes, the worse your risk model is.

### Diagnosis Guide
| You see… | Physics interpretation | Finance interpretation |
|----------|----------------------|----------------------|
| Points on the diagonal | Returns are Gaussian | Classical models (Black-Scholes, CAPM) are valid |
| S-curve (below left, above right) | Fat-tailed distribution | Crash/rally risk underestimated by Gaussian models |
| Points deviate only at extremes | Mild leptokurtosis — bulk is Gaussian, tails are not | Only extreme events deviate — moderate tail risk |
| Strong upward curl on right only | Positive skew — unusually large right tail | More extreme positive returns than expected (rare) |

### Key Takeaway
The Q-Q plot is the simplest, most visual way to see if your data is Gaussian. For most NSE stocks, it's not — and the S-curve tells you exactly how severe the fat tails are.

---

## Plot ④ — FFT Power Spectrum

### What This Plot Shows
The "frequency fingerprint" of the stock — how much energy (variability) lives at each time scale, from long-term trends to daily noise, plotted on a log-log scale to reveal power laws.

### The Axes
- X-axis: **frequency ω** (log scale) — the "speed" of fluctuations. Low frequencies = slow, long-term trends (months, years). High frequencies = fast, short-term noise (days).
- Y-axis: **|F(ω)|² — power** (log scale) — how much energy (variability) exists at that frequency. In finance: how much of the stock's total movement is driven by fluctuations at that time scale.
- Faint background: the raw spectrum. Solid circles: the **log-binned** (smoothed) spectrum. Black dashed line: the power-law fit with slope α. Grey dotted line: the **Kolmogorov −5/3 reference** — the theoretical prediction for fully-developed fluid turbulence.

### Plain English Explanation
Think of this like a music equaliser. When you play a song, the equaliser shows you how loud the bass is versus the treble. The Fourier transform does the same thing for a stock's price history: it decomposes the complex up-and-down wiggles into their constituent "frequencies" — slow undulations (the bass) and rapid daily jitter (the treble) — and tells you how much energy is at each.

The **Fourier transform** (formally: F(ω) = Σ f(t) · e^{−i2πωt/N}) converts a time-series into a frequency-series. The **power spectrum** |F(ω)|² tells you the energy at each frequency.

Both axes are logarithmic. This is essential because on a log-log plot, a straight line means the relationship is a **power law**: |F(ω)|² ∝ ω^{−α}. And power laws are the signature of **scale invariance** (physics: self-similarity / finance: fractal structure) — the idea that the statistical character of the fluctuations looks the same whether you zoom in or zoom out.

### Going Deeper (Physics + Finance Theory)
The star of this plot is the **power-law exponent α** — the slope of the straight-line fit on the log-log plot (negated, since the line slopes downward):

- **α = 0** (flat spectrum): white noise — every frequency has equal power. Completely random, no structure, no memory.
- **α = 2**: Brownian motion spectrum — a smooth random walk (a random walk in physics; the classic "efficient market" price model in finance).
- **α = 5/3 ≈ 1.67**: the **Kolmogorov spectrum** — the theoretical prediction for the inertial range of fully-developed fluid turbulence. Energy injected at large scales cascades down through a sequence of eddies, and the power spectrum follows exactly this exponent.

This is **the heart of the project**. In a turbulent river, large eddies break into smaller eddies. In a stock market, large macro shocks (RBI decisions, budgets) propagate down to daily and intraday fluctuations. If this cascade is statistically similar to fluid turbulence, the power spectrum should show a slope near −5/3.

Typical NSE stock α values fall between 1.5 and 2.5. Proximity to 1.67 is the key question of Sharma et al. (2025). Mantegna & Stanley Chapter 11 discusses this analogy explicitly.

### Diagnosis Guide
| You see… | Physics interpretation | Finance interpretation |
|----------|----------------------|----------------------|
| α ≈ 1.67 | Kolmogorov spectrum — market turbulence mimics fluid turbulence | Consistent with chaotic, efficient information processing |
| α < 1 (flatter) | Closer to white noise — weak correlations | Price is more random, less "memory" — hard to predict |
| α > 2 (steeper) | Long-range persistence / fractional Brownian motion | Strong trend persistence — momentum strategies might work |
| Stock α deviates from Nifty α | Different turbulence character | Stock has its own dynamics, not explained by market-wide forces |

### Key Takeaway
The power-law exponent α tells you whether the stock's fluctuations cascade across time scales like a turbulent fluid (α ≈ 1.67), like pure randomness (α ≈ 0), or like a persistent random walk (α ≈ 2).

---

## Plot ⑤ — Power Spectrum Comparison

### What This Plot Shows
Both the stock and Nifty 50 power spectra overlaid on the same axes — a direct comparison of their turbulence structure.

### The Axes
- Same as Plot ④ (log-log frequency vs. power), but now both series appear on one chart.
- Red circles: the stock's log-binned spectrum. Blue squares: Nifty 50. Dashed lines: respective power-law fits. Dotted black line: the Kolmogorov −5/3 guide.

### Plain English Explanation
This plot answers a simple question: *does this stock vibrate at the same frequencies as the market?* If the two lines are nearly parallel (same slope but different height), the stock and the index have the same turbulence exponent — the stock's frequency content mirrors the market.

The vertical separation between the lines is NOT meaningful — it depends on the stock's price level and is just a scale factor. Only the **slope** matters. In physics terms, we're comparing the energy spectra of two turbulent flows. In finance: we're asking whether the stock processes information across time scales in the same way as the broader market.

### Going Deeper (Physics + Finance Theory)
If the stock's slope is steeper (larger α) than Nifty's, the stock has more long-range structure and persistence. This is analogous to a more "viscous" turbulent flow — one where the energy cascades more slowly. For a trader, this might mean trend-following strategies have an edge. If the stock's slope is flatter, the stock is noisier — more like white noise with less structure to exploit.

### Diagnosis Guide
| You see… | Physics interpretation | Finance interpretation |
|----------|----------------------|----------------------|
| Parallel lines (same slope) | Same turbulence structure | Stock's dynamics are market-driven (systematic) |
| Stock line steeper (larger α) | More persistence / longer memory | Trend-following strategies may work |
| Stock line flatter (smaller α) | Noisier, closer to white noise | Signal is harder to extract from noise |

### Key Takeaway
If the slopes match, the stock is a "child of the market" — its turbulence structure is inherited from the index. If the slopes differ, the stock has its own personality.

---

## Plot ⑥ — Bispectrum Heatmap

### What This Plot Shows
A 2D colour map detecting whether pairs of frequencies are "talking to each other" — the most advanced plot in the dashboard, and the one that can distinguish genuine turbulence from structured manipulation.

### The Axes
- X-axis: Fourier mode ωα (a frequency index from 0 to N_modes).
- Y-axis: Fourier mode ωβ (a frequency index from 0 to N_modes).
- Colour intensity: the normalised magnitude of P(ωα, ωβ) = F(ωα) · F(ωβ) · F*(ωα + ωβ), where F* is the complex conjugate. The colourmap runs from black (zero coupling) through purple and orange to yellow/white (maximum coupling).

### Plain English Explanation
The standard power spectrum (Plot ④) tells you *how much* energy is at each frequency — but it throws away all **phase information**. Two completely different signals can have identical power spectra if their Fourier components have different relative phases. It's like knowing the ingredients of a dish but not the recipe.

The **bispectrum** (the "Extended Fourier Transform" or EFT) recovers this missing information. It asks: does knowing the phase at frequency ωα tell you anything about the phase at frequency ωα + ωβ? If yes, those frequencies are **phase-coupled** — they're "talking to each other."

Here is the key insight. In **fully-developed fluid turbulence** (physics) / an **efficient market** (finance), each Fourier mode evolves independently with its own random phase. Energy cascades from large to small scales, but the phases are completely uncorrelated. The bispectrum is flat and noisy — no bright spots in the heatmap.

In a **non-turbulent** signal / a market with **structured information injection**: some frequencies are locked together. Mode ωα and mode ωβ are correlated — there's a predictable relationship between them. This produces bright spots or streaks in the heatmap. Sharma et al. (2025) found that Infosys showed pronounced bispectrum spikes during 2015–2022, while other NSE stocks showed flat bispectra.

### Going Deeper (Physics + Finance Theory)
Formally, the bispectrum is: P(ωα, ωβ) = F(ωα) · F(ωβ) · F*(ωα + ωβ).

In nonlinear optics, the bispectrum detects second-order nonlinear interactions — two laser beams at frequencies ω₁ and ω₂ combining to produce light at ω₁ + ω₂ (second harmonic generation). The bispectrum would show a spike at (ω₁, ω₂). In a stock market, the analogue would be a mechanism creating fluctuations at frequency ωα + ωβ whenever both ωα and ωβ are active — a sign of a nonlinear, structured driving force.

The original bispectral analysis technique comes from Kim & Powers (1979). Sharma et al. (2025) apply it to NSE stocks for the first time.

### Diagnosis Guide
| You see… | Physics interpretation | Finance interpretation |
|----------|----------------------|----------------------|
| Dark/uniform heatmap | No phase coupling — fully-developed turbulence ✓ | Consistent with efficient markets — Green verdict |
| Bright isolated spots | Specific frequency pairs are coupled | Possible structured trading patterns at those time scales |
| Bright diagonal streak | Periodic coupling across modes | An annual or quarterly driving force (earnings? Index rebalancing?) |
| Bright region near origin (low ωα, low ωβ) | Coupling at long time scales | Macroeconomic or fundamental structure in the price series |

### Key Takeaway
A flat bispectrum means the market is behaving like genuine turbulence — random, efficient, unpredictable. Bright spots are the "fingerprint" of hidden structure — something non-random is shaping the price.

---

## Plot ⑦ — Bispectrum Cross-Sections

### What This Plot Shows
1D "slices" through the bispectrum heatmap — letting you pinpoint exactly which frequency pairs are responsible for any coupling detected in Plot ⑥.

### The Axes
- X-axis: Fourier mode ωβ — scanning across the columns of the heatmap.
- Y-axis: |P(ωα, ωβ)| (normalised bispectrum magnitude) — the coupling strength between mode ωα and mode ωβ.
- Each line is a horizontal "cut" through the heatmap at a fixed ωα value. Multiple cuts are shown (from low to high ωα). Stock lines are solid red; Nifty 50 lines are dashed blue.

### Plain English Explanation
Think of the bispectrum heatmap (Plot ⑥) as a 2D photograph taken from above. The cross-sections are like taking a ruler and reading off the brightness along several horizontal lines at different heights. If the heatmap is flat (turbulent), each slice should look like random noise around a low mean — no prominent peaks. If a spike appears at a specific ωβ, that particular pair (ωα, ωβ) is phase-coupled.

This plot is complementary to Plot ⑥. The heatmap shows the global structure; the cross-sections let you zoom in and ask: "exactly which frequency pairs are responsible?"

### Going Deeper (Physics + Finance Theory)
If you see a spike at, say, (ωα = 5, ωβ = 10), it means the 5-day-cycle and 10-day-cycle components of the stock's returns are correlated — suggesting a two-week periodicity is driven by weekly periodicity. In NSE markets, this could be caused by monthly derivatives expiry (F&O settlement), scheduled quarterly earnings, or systematic institutional fund rebalancing.

### Diagnosis Guide
| You see… | Physics interpretation | Finance interpretation |
|----------|----------------------|----------------------|
| All cross-sections flat, stock and Nifty overlapping | Both turbulent — no coupling | Efficient market behaviour |
| Stock has a spike where Nifty is flat | Stock-specific coupling at that frequency | Company-specific mechanism (earnings cycle? Insider activity?) |
| Both stock and Nifty show similar spikes | Market-wide coupling at that frequency | Macroeconomic driver (RBI policy cycle? F&O expiry?) |

### Key Takeaway
Cross-sections let you identify the *specific* time-scale pairs that are coupled — turning a qualitative "there's structure" verdict into a quantitative "the structure is at *this* frequency."

---

## Plot ⑧ — Turbulence Classification

### What This Plot Shows
A single-number verdict: is this stock turbulent (efficient) or structured (potentially manipulated)?

### The Axes
- X-axis: two bars — the selected stock and Nifty 50.
- Y-axis: **phase-coupling score** — defined as the mean of the top 1% of bispectrum values divided by the global mean of the bispectrum. Two horizontal threshold lines are drawn: orange dashed at 3.0 (weak coupling) and red dotted at 6.0 (strong coupling).

### Plain English Explanation
The phase-coupling score takes the entire bispectrum heatmap and collapses it into one number. It asks: "how concentrated are the bright spots relative to the average?" A score near 1.0 means the heatmap is completely uniform — every point has roughly equal brightness — which means perfect turbulence and no coupling. A higher score means the bright spots are much brighter than the background — there's concentrated structure.

The thresholds are calibrated from Sharma et al. (2025):
- **< 3.0**: Fully-developed turbulence (most NSE stocks and Nifty 50 fall here)
- **3.0 – 6.0**: Weak coupling / borderline
- **> 6.0**: Strong phase coupling (Infosys 2015–2022 was in this range)

### Going Deeper (Physics + Finance Theory)
In plain finance language, this score answers: *"Is the market treating this stock like a turbulent, random process — or is there hidden structure in how information flows into the price?"*

A low score means the market is efficient for this stock. No detectable, systematic information advantage exists for anyone — a level playing field for retail investors. A high score means the price contains non-random structure — which could indicate scheduled information events (earnings, dividends), systematic institutional order flow, or, in extreme cases, coordinated manipulation.

### Diagnosis Guide
| You see… | Physics interpretation | Finance interpretation |
|----------|----------------------|----------------------|
| Both bars below 3.0, similar height | Both turbulent — stock mirrors market | Stock behaves like the index — efficient |
| Stock bar significantly higher than Nifty | Stock-specific phase coupling | Dig deeper with Plots ⑥ and ⑦ |
| Both bars above 6.0 | Market-wide non-turbulent regime | Systematic event affecting all stocks (COVID, policy shock) |

### Key Takeaway
The phase-coupling score is your "traffic light" — green (< 3) means efficient turbulence, amber (3–6) means investigate further, red (> 6) means something non-random is shaping the price.

---

## Plot ⑨ — Master Dashboard

### What This Plot Shows
A one-page "quant tearsheet" combining six key sub-plots into a single glanceable figure.

### The Axes
The master dashboard is a 3×4 grid containing miniature versions of the core analyses:
- **Top-left (¾ width):** Normalised price — same as Plot ① top panel.
- **Top-right (¼ width):** Return distributions — overlaid histograms of stock and Nifty with a Gaussian reference.
- **Middle-left (½ width):** Log-returns time series — same as Plot ① middle panel.
- **Middle-right (½ width):** FFT power spectrum — both stock and Nifty, with their α values labelled.
- **Bottom-left (½ width):** Stock bispectrum heatmap — with phase-coupling score and verdict.
- **Bottom-right (½ width):** Nifty bispectrum heatmap — for comparison.

### Plain English Explanation
This is not a replacement for the individual detailed plots — it's a **summary at a glance**. Read it as a story, left-to-right, top-to-bottom:

1. **Top-left:** *Has this stock made money?* (price performance)
2. **Top-right:** *Are the returns fat-tailed?* (distribution shape)
3. **Middle-left:** *Are there volatility clusters?* (time-domain dynamics)
4. **Middle-right:** *What is the turbulence spectrum?* (frequency-domain structure)
5. **Bottom row:** *Is there phase coupling?* (bispectral fingerprint)

In finance, this is your "one-page econophysics report" — the kind of figure you'd put in a presentation or research note. In physics, it's a multi-panel diagnostic figure like those in experimental physics papers — all the key measurements on one page.

### Diagnosis Guide
Follow this five-step checklist:
1. **Performance**: Is the red line above or below the blue? (Did the stock beat the market?)
2. **Tails**: Does the histogram match the Gaussian dashed line, or are the bars taller at the extremes?
3. **Clustering**: Are the log-return spikes clustered or evenly spread?
4. **Spectrum slope**: Is α near 1.67 (Kolmogorov), or significantly different?
5. **Bispectrum**: Is the heatmap uniformly dark (turbulent) or does it have bright spots (structured)?

### Key Takeaway
The master dashboard is a characterisation of market microstructure — not a trading signal. It tells you *what kind of statistical animal this stock is*, not whether to buy or sell it.

---

## Connections Map

| Plot | Physics Tradition | Finance Tradition | Book Chapter |
|------|-------------------|-------------------|--------------|
| ① Time-Domain Analysis | Time-series analysis, dynamical systems | Technical analysis, price charts | Ch. 5 |
| ② Return Distribution | Statistical mechanics, CLT / Lévy stable laws | Risk management, VaR | Ch. 3, 4 |
| ③ Q-Q Plot | Statistical hypothesis testing | Model validation, risk modelling | Ch. 3 |
| ④⑤ Power Spectrum | Signal processing, turbulence theory (Kolmogorov 1941) | Frequency trading, cycle analysis | Ch. 11 |
| ⑥⑦ Bispectrum | Nonlinear wave physics, plasma physics (Kim & Powers 1979) | Market microstructure, manipulation detection | Sharma et al. 2025 |
| ⑧ Classification | Phase transition analogy | Regime detection | Sharma et al. 2025 |
| ⑨ Master Dashboard | Multi-panel diagnostic figure | Quant tearsheet | — |

---

## Glossary

**Log-return**
*Physics:* The natural logarithm of the ratio of consecutive prices — the natural variable for a multiplicative stochastic process.
*Finance:* The continuously compounded return; preferred because log-returns are additive over time.
*Equation:* r(t) = ln[P(t) / P(t−1)]

**Volatility**
*Physics:* The standard deviation of the displacement increments of a random walk — closely related to the diffusion coefficient.
*Finance:* The standard deviation of returns; the most common measure of risk, typically annualised by multiplying by √252.
*Equation:* σ_annual = σ_daily × √252

**Fat tails**
*Physics:* A probability distribution whose tails decay more slowly than a Gaussian — extreme events are more probable.
*Finance:* The empirical observation that market crashes and rallies happen far more often than a bell curve predicts.

**Kurtosis**
*Physics:* The fourth standardised moment of a distribution, measuring the weight of its tails relative to a Gaussian.
*Finance:* A tail-risk indicator; excess kurtosis > 0 means heavier tails than normal, signalling underestimated crash risk.
*Equation:* κ = E[(X − μ)⁴] / σ⁴ − 3 (excess kurtosis)

**Skewness**
*Physics:* The third standardised moment, measuring asymmetry of the distribution around its mean.
*Finance:* Negative skewness means crashes are larger than rallies; positive skewness is the opposite.
*Equation:* γ = E[(X − μ)³] / σ³

**Power spectrum**
*Physics:* |F(ω)|² — the squared magnitude of the Fourier transform, showing the energy distribution across frequencies.
*Finance:* How much of a stock's total variability is driven by fluctuations at each time scale (daily, weekly, monthly).
*Equation:* S(ω) = |F(ω)|²

**Fourier transform**
*Physics:* A mathematical operation that decomposes a time-domain signal into its constituent frequencies — like splitting white light into a rainbow.
*Finance:* Decomposing a stock's price history into periodic components at different time scales.
*Equation:* F(ω) = Σ_t f(t) · e^{−i2πωt/N}

**Power law**
*Physics:* A relationship where one quantity varies as a power of another: y ∝ x^α. Appears as a straight line on a log-log plot.
*Finance:* A relationship suggesting scale invariance — the same statistical pattern at daily, weekly, and monthly scales.

**Kolmogorov spectrum**
*Physics:* The −5/3 power-law exponent predicted by Kolmogorov (1941) for the inertial range of fully-developed fluid turbulence.
*Finance:* The benchmark turbulence exponent; if a stock's spectral slope ≈ 1.67, its information cascade resembles fluid turbulence.

**Turbulence exponent α**
*Physics:* The negative slope of the power spectrum on a log-log plot, characterising the scaling of the energy cascade.
*Finance:* A measure of how "structured" or "persistent" the return series is across time scales.

**Bispectrum**
*Physics:* A third-order spectral analysis tool that detects nonlinear phase coupling between frequency pairs.
*Finance:* A diagnostic for hidden structure in price dynamics — it reveals whether certain periodicities are locked together.
*Equation:* P(ωα, ωβ) = F(ωα) · F(ωβ) · F*(ωα + ωβ)

**Phase coupling**
*Physics:* A condition where the phases of two or more Fourier modes are correlated, indicating nonlinear interaction.
*Finance:* Evidence that fluctuations at certain time scales are systematically linked — a sign of structured information flow.

**Phase-coupling score**
*Physics:* The ratio of the mean of the top 1% of bispectrum magnitudes to the global mean — a measure of spectral concentration.
*Finance:* A single number summarising how much "hidden structure" exists in the stock's price dynamics. Below 3.0 = turbulent; above 6.0 = structured.

**Gaussian (normal distribution)**
*Physics:* The probability distribution predicted by the Central Limit Theorem for the sum of many small, independent random variables.
*Finance:* The "bell curve" underlying Black-Scholes, CAPM, and most portfolio theory — the default assumption of textbook finance.
*Equation:* f(x) = (1 / σ√2π) · exp[−(x − μ)² / 2σ²]

**Student-t distribution**
*Physics:* A generalisation of the Gaussian with heavier tails, parameterised by degrees of freedom ν; converges to Gaussian as ν → ∞.
*Finance:* A practical fat-tail model used in Value-at-Risk calculations when Gaussian tails underestimate crash risk.

**Lévy distribution (Lévy stable)**
*Physics:* A family of probability distributions characterised by a stability parameter α (0 < α ≤ 2); the Gaussian is the special case α = 2. For α < 2, variance is infinite.
*Finance:* The general framework for modelling fat-tailed returns, proposed by Mandelbrot (1963) for cotton prices.

**Autocorrelation**
*Physics:* The correlation of a signal with a delayed copy of itself, measuring how much the past predicts the future.
*Finance:* A measure of serial dependence in returns; strong autocorrelation implies momentum or mean-reversion effects.
*Equation:* C(τ) = ⟨r(t) · r(t + τ)⟩ / ⟨r(t)²⟩

**Stationarity**
*Physics:* A property of a process whose statistical properties (mean, variance, correlations) do not change over time.
*Finance:* An assumption underlying most time-series models — that the "rules of the game" don't change. Market regime changes violate stationarity.

**Nifty 50**
*Physics:* The reference process — a weighted average of 50 systems, against which a single system's behaviour is compared.
*Finance:* The flagship index of the National Stock Exchange of India, comprising the 50 largest companies by free-float market capitalisation.

**Alpha (finance)**
*Physics:* The drift difference between the stock process and the reference process.
*Finance:* The excess return of a stock over its benchmark — the portion of performance not explained by market-wide movements.

**Beta (finance)**
*Physics:* The sensitivity of the stock to the external driving force (the market index).
*Finance:* A stock's sensitivity to market movements. β = 1 means the stock moves with the market; β > 1 means amplified moves.
*Equation:* β = Cov(r_stock, r_market) / Var(r_market)

**Annualisation**
*Physics:* Scaling a diffusion rate from one time step to a standard time horizon using √t scaling (since variance scales linearly with time in a random walk).
*Finance:* Converting daily volatility to annual volatility by multiplying by √252 (approximately 252 trading days per year).
*Equation:* σ_annual = σ_daily × √252

**Normalised price**
*Physics:* A rescaled variable where the initial value is set to a common reference (100), enabling comparison of systems with different natural scales.
*Finance:* Rebasing stock prices to 100 at the start of a period so that percentage gains can be read directly from the chart.
*Equation:* P_norm(t) = P(t) / P(0) × 100

**Diffusion**
*Physics:* The random spreading of particles (e.g., ink in water), governed by the diffusion equation. Standard deviation grows as √t.
*Finance:* The mathematical model underlying the random walk hypothesis — stock prices "diffuse" away from their starting point over time.
*Equation:* ⟨x²⟩ = 2Dt (Einstein relation)

**Random walk**
*Physics:* A stochastic process where each step is independent and identically distributed — the simplest model of diffusion.
*Finance:* The hypothesis that stock prices follow an unpredictable path where past prices contain no information about future prices — the mathematical backbone of the Efficient Market Hypothesis.

---

## Further Reading

1. **Mantegna, R.N. & Stanley, H.E. (1999).** *An Introduction to Econophysics: Correlations and Complexity in Finance.* Cambridge University Press. — The foundational textbook. Start with Chapters 3–5 for distributions, Chapter 7 for volatility, Chapter 11 for the turbulence analogy.

2. **Sharma, Dutta & Mukherjee (2025).** *Identification of Phase Correlations in Financial Stock Market Turbulence.* arXiv:2508.20105. — The research paper that this dashboard implements. Introduces bispectral analysis to NSE data.

3. **Mandelbrot, B.B. (1963).** *The Variation of Certain Speculative Prices.* Journal of Business, 36(4), 394–419. — The paper that started econophysics before the word existed. First documentation of fat tails and volatility clustering in financial data.

4. **Kolmogorov, A.N. (1941).** *The Local Structure of Turbulence in Incompressible Viscous Fluid for Very Large Reynolds Numbers.* Doklady Akademii Nauk SSSR, 30, 301–305. — The origin of the −5/3 power law.

5. **Kim, Y.C. & Powers, E.J. (1979).** *Digital Bispectral Analysis and its Applications to Nonlinear Wave Interactions.* IEEE Transactions on Plasma Science, 7(2), 120–131. — The original bispectral analysis paper.

6. **Fama, E.F. (1970).** *Efficient Capital Markets: A Review of Theory and Empirical Work.* Journal of Finance, 25(2), 383–417. — The Efficient Market Hypothesis — the claim that prices fully reflect all available information.

---

> *You've reached the end. If the plots have made you curious about the mathematics of turbulence, pick up Mantegna & Stanley — it's one of the most readable physics textbooks ever written, and it'll change how you think about markets forever.* 🌊📈

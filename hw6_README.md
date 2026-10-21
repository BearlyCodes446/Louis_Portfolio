# Market Risk Analytics in Python: Returns, VaR & Expected Shortfall

**Course:** Coding for Risk Management (ERMC PS5355), Columbia University, Homework 6
**Author:** Changchi (Louis) Zhang · `cz2990`
**Stack:** Python 3 · NumPy · pandas · yfinance · Matplotlib · SciPy

## Overview

This project is a compact, end-to-end market-risk workflow. It pulls historical equity prices from Yahoo Finance, converts them into a daily return series, and estimates two standard tail-risk measures using historical simulation: **Value-at-Risk (VaR)** and **Expected Shortfall (ES)**. Goldman Sachs (`GS`) is the worked example, but every step is a reusable function that works for any ticker. Each risk function is unit-tested against a distribution with a known closed-form answer.

## Files

| File | Description |
|---|---|
| `hw6_cz2990.py` | Script containing all four questions |
| `hw6_cz2990.ipynb` | Google Colab notebook with the same code, organized by question |

## What the Code Does

### 1. `WhoAmI()`
Returns the author's university ID for grading.

### 2. `get_stock_data(symbol)` and `get_returns(pricevec)`
- Downloads the full daily price history for a ticker with `yfinance`, then selects that ticker's closing-price column from the returned pandas DataFrame.
- Converts the prices to a NumPy array and computes simple daily returns with a single vectorized expression and no loops:

$$r_t = \frac{P_t}{P_{t-1}} - 1 \quad\Longleftrightarrow\quad \texttt{pricevec[1:n] / pricevec[:n-1] - 1}$$

- Reports the mean, maximum, minimum, and standard deviation of the return series.

### 3. `percent_var(r, alpha)`: Historical VaR
- Estimates VaR as the empirical $(1-\alpha)$ percentile of returns, stated as a positive loss, and plots the return distribution as a histogram.
- **Unit test:** for returns drawn from $N(5\%,\ 3\%)$ with $\alpha = \Phi(2) \approx 97.72\%$, the 2-standard-deviation left tail is $\lvert 0.05 - 2(0.03) \rvert = 0.01$.

### 4. `es(losses, alpha=None, VaR=None)`: Expected Shortfall
- Computes ES as the average loss beyond the VaR threshold:

$$\text{ES}_\alpha = \mathbb{E}\left[\,L \mid L > \text{VaR}_\alpha\,\right]$$

- Accepts *either* a confidence level (VaR is then derived from the loss distribution) *or* an explicit VaR threshold, so it can be chained directly with the output of `percent_var`.
- **Unit test:** for losses drawn from $U(0, 100)$, $\alpha = 0.8$ gives VaR = 80 and ES ≈ 90. Both input paths are tested.

## Concepts Demonstrated

**Python and data handling**
- Function design with optional and keyword arguments (`alpha=None, VaR=None`)
- Sourcing market data from an external library (`yfinance`) and moving between pandas and NumPy (DataFrame → column selection → Series → array via `.values`)

**NumPy vectorization**
- Slicing to build lagged price vectors, so a vector is expressed as a function of itself
- Element-wise arithmetic and broadcasting (`ratiovec - 1`, `-returns`)
- Boolean masking to isolate the loss tail (`losses[losses > VaR]`)
- Summary statistics and empirical percentiles (`np.mean`, `np.std`, `np.percentile`)

**Risk management**
- Simple returns and historical simulation of the return distribution
- VaR vs. ES: VaR gives the loss *threshold* at a confidence level, while ES gives the *average severity* beyond it. ES is a coherent (subadditive) risk measure, which is why the Basel FRTB framework moved market-risk capital from 99% VaR to **97.5% ES**.

**Testing and visualization**
- Unit tests that validate each function against analytically known results
- Distribution histograms with Matplotlib

## Sample Results: GS Daily Returns

*May 1999 – October 21, 2026 · 6,909 daily returns · run on October 21, 2026*

| Statistic | Value |
|---|---|
| Average daily return | 0.068% |
| Standard deviation | 2.27% |
| Largest gain | +26.5% (Nov 24, 2008) |
| Largest loss | −19.0% (Jan 20, 2009) |
| 1-day VaR, 95% | 3.27% |
| 1-day VaR, 99% | 5.75% |
| 1-day ES, 97.5% | 6.34% |
| 1-day ES, 99% | 8.58% |

On a typical day GS moves about ±2.3%. On its worst 1% of days, however, the average loss is about 8.6%, roughly 1.5× the 99% VaR. This gap is exactly the tail severity that VaR alone does not capture. Re-running the code pulls the latest prices, so figures will shift slightly over time.

## Methodology Notes and Assumptions

- **Full price history** (`period="max"`), which includes the 2008 financial crisis and the 2020 COVID shock. Recent versions of `yfinance` default to roughly one month of data, which is far too few observations to estimate a 99% tail.
- **Sign convention:** losses are stated as positive numbers ($L = -r$), so the ES threshold is the upper $\alpha$ percentile of losses. This is equivalent to the lower $(1-\alpha)$ percentile of returns used by `percent_var`.
- Simple (not log) returns, a 1-day horizon, equally weighted observations, and population standard deviation.
- **Limitations:** historical simulation assumes the past distribution is representative of the future. No volatility weighting, multi-day scaling, or backtesting is applied.

## Class 6 Topics: Data Analysis with pandas

This assignment accompanied the course's pandas module, which covered:

- **DataFrames:** 2-D labeled tables built with `pd.DataFrame(data, columns=[...], index=[...])`, using zero-based default indexing and the rows-before-columns convention
- **Selecting vs. filtering:** selecting chooses columns, while filtering chooses rows, either by position or by condition (e.g., `df[df["names"] == "Alan"]`)
- **`loc` vs. `iloc`:** label-based vs. integer-position access. `iloc` slices exclude the endpoint, like `np.arange`.
- **Arrange vs. mutate:** `sort_values` returns a sorted copy and leaves the original unchanged. Assignment (e.g., adding a Boolean column) and `del` permanently modify the DataFrame.
- **Group and summarize:** SQL-style aggregation, e.g., `df.groupby("city")["ages"].mean()`
- **File I/O:** `to_csv` / `read_csv`, and using `index_col=0` so a saved index is not re-imported as an extra column

## How to Run

**Google Colab:** upload `hw6_cz2990.ipynb` and select *Runtime → Run all*. If `yfinance` is not available, run `!pip install yfinance` first.

**Locally:**
```bash
pip install numpy pandas yfinance matplotlib scipy
python hw6_cz2990.py
```

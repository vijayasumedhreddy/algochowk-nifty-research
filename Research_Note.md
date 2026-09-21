# NIFTY 50 Post-Drop Recovery: Event Study and Backtest

## 1. Hypothesis

After a significant one-day fall in the NIFTY 50, the market tends to recover over the following few trading days.

## 2. Data

Daily NIFTY 50 OHLC data was obtained from Yahoo Finance using the `^NSEI` ticker. The available sample covers **17 Sep 2007–21 Sep 2026**, with **4,664 trading observations**. NSE documentation was used as a reference for the NIFTY 50 index and historical-data fields.

Data checks found:

* 0 missing OHLC values
* 0 duplicate dates
* dates correctly ordered
* 0 invalid/non-positive OHLC observations
* 0 cases where High < Open/Close, Low > Open/Close, or High < Low

Three absolute daily returns above 10% were flagged for review (2008-10-24, 2009-05-18, 2020-03-23) and retained because large moves are economically plausible and should not be removed solely because they are extreme.

## 3. Event Definition and Trading Rules

A **significant fall** is defined as a close-to-close daily return of **≤ −2%**.

To avoid look-ahead bias:

* Event is identified using the event day's close.
* Entry occurs at the **next trading day's Open**.
* Exit occurs at the Close after **1, 3, or 5 trading days**.
* Forward return = Exit Close / Entry Open − 1.

The primary threshold and horizons were fixed before interpreting the main results. Closely occurring events were also examined using a **5-trading-day non-overlap window**.

## 4. Event-Study Results

For the full event sample (**N = 200**):

| Holding period |     Mean |   Median | Win rate | Std. dev. |
| -------------- | -------: | -------: | -------: | --------: |
| 1 day          | −0.0380% | −0.0123% |   49.00% |   2.4812% |
| 3 days         | +0.1217% | +0.4551% |   55.00% |   4.1021% |
| 5 days         | +0.1586% | +0.4105% |   52.50% |   5.4101% |

The corresponding descriptive baseline, using non-event observations, produced mean returns of **−0.0502%, +0.0329%, and +0.1194%** for 1-, 3-, and 5-day horizons. Event-minus-baseline differences were therefore small: **+0.0122, +0.0888, and +0.0392 percentage points**.

Bootstrap 95% confidence intervals for event means all included zero. Welch tests comparing event and baseline returns produced p-values of **0.9449, 0.7612, and 0.9190** for 1, 3, and 5 days respectively. These tests do not provide statistically strong evidence of an abnormal recovery effect in the overlapping full sample.

## 5. Robustness

Thresholds of **−1.5%, −2.0%, −2.5%, and −3.0%** were tested with 1-, 3-, and 5-day holding periods, using a 5-day non-overlap rule.

Results were mixed. Five-day mean returns were positive at all four thresholds, but the −2% case produced only **+0.0202%** across 124 non-overlapping events, while the −3% case produced **+0.7423%** from only 53 events. The stronger −3% result should not be selected post-hoc as the primary rule because that would introduce data-snooping/selection bias.

## 6. Chronological Out-of-Sample Test

The −2% rule was fixed and tested chronologically.

* Training: **17 Sep 2007–19 Jan 2021**, 175 events
* OOS: **20 Jan 2021–21 Sep 2026**, 25 events

OOS mean returns were:

* 1 day: **+0.6659%**, p = 0.0433
* 3 days: **+0.8241%**, p = 0.0719
* 5 days: **+1.1418%**, p = 0.0899

The OOS results are positive, but the sample contains only 25 events and event dependence can affect uncertainty. They therefore provide evidence worth reporting, not definitive proof of a persistent anomaly.

## 7. Event-Driven Backtest

A simple index-level backtest used the **−2% threshold, 5-day holding period, next-day Open entry, and 0.10% round-trip transaction cost**.

Using 5-day non-overlapping events:

* Trades: **124**
* Average net return: **+0.2839%**
* Median net return: **+0.2816%**
* Win rate: **50.81%**
* Trade volatility: **4.5318%**
* Compounded net return: **+25.02%**
* Maximum drawdown: **−39.80%**

The chronological OOS backtest produced **19 trades**, average net return **+0.7014%**, win rate **57.89%**, compounded net return **+13.14%**, and maximum drawdown **−6.31%**.

These are historical index-level simulations, not claims of directly executable NIFTY trading performance.

## 8. Limitations and Conclusion

The analysis is subject to clustered events, limited OOS sample size, regime changes, transaction costs, slippage, and differences between an index-level simulation and an actually tradable instrument. The descriptive baseline is not a perfectly matched control because observations can overlap event windows.

Overall, the full-sample event study shows only modest average recovery relative to normal days, with confidence intervals spanning zero. Robustness is mixed, while the fixed-rule OOS period is more positive but small. The evidence therefore **does not establish a stable, risk-free recovery effect**, and further testing with independent events, alternative market regimes, and more realistic execution assumptions would be required.

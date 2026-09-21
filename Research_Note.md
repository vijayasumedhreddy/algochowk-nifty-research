\# NIFTY 50 Post-Fall Recovery: Event Study and Backtest



\## 1. Hypothesis



This study tests whether the NIFTY 50 tends to recover over the next few trading days after a significant one-day decline.



The primary event definition is a one-day close-to-close NIFTY 50 return of \*\*-2% or lower\*\*. The main holding period is \*\*5 trading days\*\*, with 1-day and 3-day horizons also examined.



The analysis is designed to test the hypothesis without assuming that a recovery exists.



\## 2. Data



Daily NIFTY 50 OHLC data were obtained from \*\*Yahoo Finance using the `^NSEI` ticker\*\*, covering \*\*17 September 2007 to 21 September 2026\*\*.



The dataset contains:



\- 4,664 trading-day observations

\- Date

\- Open

\- High

\- Low

\- Close



Data validation found:



\- 0 missing OHLC observations

\- 0 duplicate dates

\- Dates correctly sorted

\- 0 invalid non-positive OHLC values

\- 0 observations where High < Open/Close

\- 0 observations where Low > Open/Close

\- 0 observations where High < Low



Three unusually large daily moves were flagged for review. They were retained because large market moves are relevant to the research question and magnitude alone is not sufficient reason for exclusion.



\## 3. Event Definition and Trading Rules



An event occurs when:



\*\*NIFTY 50 close-to-close return <= -2%\*\*



To avoid look-ahead bias:



\- The event is identified using the closing price of the event day.

\- Entry occurs at the \*\*next trading day's Open\*\*.

\- Exit occurs at the Close after the specified holding period.



Holding periods tested:



\- 1 trading day

\- 3 trading days

\- 5 trading days



The primary backtest uses:



\- Event threshold: -2%

\- Holding period: 5 trading days

\- Entry: next trading day Open

\- Exit: fifth trading day Close

\- Round-trip transaction cost: 0.10%



Because closely occurring events can create overlapping observations, a \*\*5-trading-day non-overlap rule\*\* was also applied as an independence/robustness check.



\## 4. Event Study Results



Using all detected -2% events, 200 events were identified.



| Holding period | Mean return | Median return | Win rate |

|---|---:|---:|---:|

| 1 day | -0.0380% | -0.0123% | 49.00% |

| 3 days | +0.1217% | +0.4551% | 55.00% |

| 5 days | +0.1586% | +0.4105% | 52.50% |



The corresponding baseline analysis using non-event days produced mean returns of:



\- 1 day: -0.0502%

\- 3 days: +0.0329%

\- 5 days: +0.1194%



The event-minus-baseline differences were therefore:



\- 1 day: +0.0122 percentage points

\- 3 days: +0.0888 percentage points

\- 5 days: +0.0392 percentage points



These differences were small relative to return variability.



\## 5. Statistical Tests



Bootstrap 95% confidence intervals for the event mean included zero at all three holding periods.



Welch tests comparing event returns with the baseline produced:



\- 1 day: p = 0.9449

\- 3 days: p = 0.7612

\- 5 days: p = 0.9190



The event means were therefore not statistically distinguishable from zero or from the descriptive baseline under these tests.



Because events can cluster in periods of market stress, the standard bootstrap and simple tests should not be interpreted as fully accounting for dependence between nearby events.



\## 6. Robustness



The threshold was varied from -1.5% to -3.0%, while retaining the 5-trading-day non-overlap rule.



For the 5-day holding period:



| Threshold | Events | Mean return | Win rate |

|---|---:|---:|---:|

| -1.5% | 207 | +0.2282% | 53.14% |

| -2.0% | 124 | +0.0202% | 49.19% |

| -2.5% | 75 | +0.3120% | 58.67% |

| -3.0% | 53 | +0.7423% | 60.38% |



The results are mixed across thresholds and holding periods. The stronger result at -3% comes from only 53 events and was not selected as the primary specification after observing the results. This reduces the risk of presenting a post-hoc parameter choice as if it had been specified in advance.



\## 7. Out-of-Sample Validation



A chronological split was used:



\- Training period: 17 September 2007 – 19 January 2021

\- Out-of-sample period: 20 January 2021 – 21 September 2026



The -2% threshold and 5-day holding rule were kept fixed.



The non-overlapping OOS backtest produced:



\- 19 trades

\- Average net return: +0.7014%

\- Median net return: +0.5009%

\- Win rate: 57.89%

\- Trade volatility: 3.2420%

\- Compounded net return: +13.14%

\- Maximum drawdown: -6.31%



The OOS sample is small, so these results provide limited evidence about persistence and should not be treated as proof of a stable trading edge.



\## 8. Backtest Results



Across the full sample, the 5-day non-overlapping backtest produced:



\- 124 trades

\- Average net return: +0.2839%

\- Median net return: +0.2816%

\- Win rate: 50.81%

\- Trade volatility: 4.5318%

\- Compounded net return: +25.02%

\- Maximum drawdown: -39.80%



The corresponding all-event backtest produced a higher compounded return but also a substantially larger drawdown. Removing closely occurring events reduced the apparent performance, which demonstrates the importance of accounting for event dependence.



The backtest is an index-level research simulation. It does not assume that a specific investment product exactly replicates the NIFTY 50 at the stated Open and Close prices.



\## 9. Limitations



Important limitations include:



1\. The historical sample contains relatively few large-fall events compared with ordinary trading days.

2\. Event clustering can reduce statistical independence.

3\. The OOS backtest contains only 19 non-overlapping trades.

4\. Transaction costs are modeled as a fixed 0.10% round-trip assumption rather than observed execution costs.

5\. Slippage, bid-ask spreads, taxes, and market impact are not modeled separately.

6\. The analysis uses historical index prices and therefore does not guarantee implementability through a particular tradable instrument.

7\. Results can vary across market regimes.

8\. Testing multiple thresholds and holding periods creates a risk of data snooping and post-hoc selection.

9\. The baseline is descriptive and is not a fully matched control portfolio.



\## 10. Conclusion



The analysis finds a \*\*small positive average recovery at the 3-day and 5-day horizons in the all-event sample\*\*, but the event returns are not statistically distinguishable from the baseline under the tests used.



The robustness analysis is mixed, while the fixed -2% rule remains positive in the chronological OOS backtest under the stated assumptions. However, the OOS sample is small and the full-period non-overlapping backtest experienced a substantial maximum drawdown.



Overall, the evidence is \*\*not sufficient to establish a robust, persistent recovery effect\*\*. The results are better viewed as a historical event-study finding that requires further testing across independent datasets, market regimes, execution assumptions, and larger out-of-sample samples.


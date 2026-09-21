\# NIFTY 50 Post-Fall Recovery — Event Study \& Backtest



\## Overview



This project investigates the hypothesis:



> After a significant one-day fall in the NIFTY 50, does the index tend to recover over the following few trading days?



The primary event is defined as a \*\*one-day close-to-close return of -2% or lower\*\*.



The analysis combines:



\- Historical data validation

\- Event-study analysis

\- Baseline comparison

\- Statistical testing

\- Threshold and holding-period robustness checks

\- Non-overlapping event analysis

\- Chronological out-of-sample testing

\- Event-driven backtesting

\- Transaction-cost modeling

\- Drawdown analysis



The project was completed as part of a quantitative research challenge.



\---



\## Research Question



\*\*Hypothesis:\*\* A significant one-day decline in the NIFTY 50 may be followed by a positive recovery over the next few trading days.



The analysis does not assume that the hypothesis is true. It tests the hypothesis against historical data and compares the results with a baseline.



\---



\## Data



Daily NIFTY 50 OHLC data were obtained from \*\*Yahoo Finance using the `^NSEI` ticker\*\*.



Coverage:



\- Start: 17 September 2007

\- End: 21 September 2026

\- Observations: 4,664



Fields used:



\- Date

\- Open

\- High

\- Low

\- Close



NSE documentation was used as a reference for the NIFTY 50 index and historical-data context.



\### Data validation



The dataset was checked for:



\- Missing values

\- Duplicate dates

\- Chronological ordering

\- Non-positive OHLC values

\- Invalid High/Low relationships

\- Large daily returns

\- Large calendar gaps



No missing or duplicate observations were found.



Three unusually large daily moves were flagged for review and retained because large market movements are relevant to the research question.



\---



\## Methodology



\### Event definition



An event occurs when:



```text

Close-to-close return <= -2%


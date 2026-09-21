\# AI Usage Note



\## AI Tools Used



ChatGPT was used as a research and coding assistant during this project.



AI was used for:



\- Breaking the challenge into manageable research steps

\- Discussing event-study methodology

\- Reviewing possible definitions of a significant market fall

\- Helping structure Python scripts

\- Debugging Python errors

\- Explaining statistical tests and confidence intervals

\- Suggesting robustness checks

\- Reviewing the organization of the research results

\- Helping draft documentation



\## Human Decisions



The research design and final decisions were reviewed and selected by me.



Important decisions included:



\- Using a -2% close-to-close decline as the primary event threshold

\- Using the next trading day's Open to avoid look-ahead bias

\- Testing 1-, 3-, and 5-day holding periods

\- Using a 5-day non-overlap rule to examine dependence between closely occurring events

\- Using a chronological train/OOS split rather than a random split

\- Including transaction costs in the backtest

\- Keeping the -2% threshold fixed for the OOS test

\- Reporting the results even when they did not strongly support the hypothesis



\## AI Suggestions That Were Changed or Challenged



AI initially helped structure the event-study and backtest workflow. During the analysis, I checked the outputs and identified methodological concerns around overlapping events and dependence.



Instead of relying only on the all-event results, I added:



\- Non-overlapping event analysis

\- Threshold robustness testing

\- Chronological out-of-sample testing

\- A separate OOS backtest

\- Transaction-cost analysis

\- Maximum drawdown analysis



These additions were important because the strongest historical result can be misleading if closely related events are counted as independent observations.



\## Incorrect or Incomplete AI-Assisted Suggestions



Some initial analysis steps required correction during implementation.



For example, the first OOS backtest implementation needed adjustment because the event-study and backtest samples were affected differently by the non-overlap rule. The implementation was tested through actual Python execution before accepting the final results.



The baseline comparison was also treated as a descriptive benchmark rather than as a perfect matched control because event windows and ordinary-market observations can differ in their dependence structure.



\## What I Learned



The main learning from the project was that a positive average return is not sufficient evidence for a trading hypothesis.



The analysis showed the importance of:



\- Avoiding look-ahead bias

\- Separating in-sample and out-of-sample testing

\- Accounting for overlapping events

\- Comparing against a baseline

\- Testing robustness rather than selecting the best parameter

\- Including transaction costs

\- Examining drawdowns

\- Being cautious with small OOS samples



AI was used as an assistant for coding, debugging, explanation and research organization, while the final methodology, interpretation and conclusions were checked against the actual data and program outputs.


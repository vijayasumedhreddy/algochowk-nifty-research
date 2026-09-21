import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# --------------------------------------------------
# Paths
# --------------------------------------------------

INPUT_FILE = "results/backtest_trades_non_overlapping.csv"
OUTPUT_DIR = Path("results/charts")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load trade data
# --------------------------------------------------

trades = pd.read_csv(INPUT_FILE)

trades["event_date"] = pd.to_datetime(trades["event_date"])
trades["entry_date"] = pd.to_datetime(trades["entry_date"])
trades["exit_date"] = pd.to_datetime(trades["exit_date"])


# --------------------------------------------------
# 1. Cumulative equity curve
# --------------------------------------------------

trades["equity"] = (
    1 + trades["net_return"]
).cumprod()

plt.figure(figsize=(10, 5))

plt.plot(
    trades["exit_date"],
    trades["equity"]
)

plt.title("Non-Overlapping Event Strategy: Cumulative Equity")
plt.xlabel("Date")
plt.ylabel("Growth of ₹1")

plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "cumulative_equity.png",
    dpi=150
)

plt.close()


# --------------------------------------------------
# 2. Drawdown curve
# --------------------------------------------------

running_max = trades["equity"].cummax()

trades["drawdown"] = (
    trades["equity"] / running_max
) - 1

plt.figure(figsize=(10, 5))

plt.plot(
    trades["exit_date"],
    trades["drawdown"] * 100
)

plt.title("Non-Overlapping Event Strategy: Drawdown")
plt.xlabel("Date")
plt.ylabel("Drawdown (%)")

plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "drawdown.png",
    dpi=150
)

plt.close()


# --------------------------------------------------
# 3. Distribution of trade returns
# --------------------------------------------------

plt.figure(figsize=(9, 5))

plt.hist(
    trades["net_return"] * 100,
    bins=20
)

plt.axvline(
    0,
    linestyle="--"
)

plt.title("Distribution of 5-Day Net Trade Returns")
plt.xlabel("Net Return (%)")
plt.ylabel("Number of Trades")

plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "return_distribution.png",
    dpi=150
)

plt.close()


# --------------------------------------------------
# 4. Save summary statistics
# --------------------------------------------------

summary = {
    "Number of trades": len(trades),
    "Average net return": trades["net_return"].mean(),
    "Median net return": trades["net_return"].median(),
    "Win rate": (trades["net_return"] > 0).mean(),
    "Return volatility": trades["net_return"].std(),
    "Total compounded return": trades["equity"].iloc[-1] - 1,
    "Maximum drawdown": trades["drawdown"].min()
}

summary_df = pd.DataFrame(
    summary.items(),
    columns=["Metric", "Value"]
)

summary_df.to_csv(
    OUTPUT_DIR / "backtest_summary.csv",
    index=False
)


# --------------------------------------------------
# Finished
# --------------------------------------------------

print("=" * 60)
print("CHART GENERATION COMPLETE")
print("=" * 60)

print("\nCreated:")

print(
    "results/charts/cumulative_equity.png"
)

print(
    "results/charts/drawdown.png"
)

print(
    "results/charts/return_distribution.png"
)

print(
    "results/charts/backtest_summary.csv"
)
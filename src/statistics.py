import pandas as pd
import numpy as np
from scipy import stats


DATA_FILE = "data/nifty50_daily.csv"
EVENT_FILE = "results/event_study_results.csv"

EVENT_THRESHOLD = -0.02
HOLDING_PERIODS = [1, 3, 5]

BOOTSTRAP_ITERATIONS = 10000
RANDOM_SEED = 42


def load_data():
    df = pd.read_csv(DATA_FILE)

    df["Date"] = pd.to_datetime(df["Date"])

    for column in ["Open", "High", "Low", "Close"]:
        df[column] = pd.to_numeric(df[column])

    df = df.sort_values("Date").reset_index(drop=True)

    df["Daily_Return"] = df["Close"].pct_change()

    return df


def calculate_baseline(df, holding_period):
    returns = []

    for i in range(len(df)):

        entry_position = i + 1
        exit_position = i + holding_period

        if exit_position >= len(df):
            continue

        daily_return = df.loc[i, "Daily_Return"]

        if pd.notna(daily_return) and daily_return <= EVENT_THRESHOLD:
            continue

        entry_price = df.loc[entry_position, "Open"]
        exit_price = df.loc[exit_position, "Close"]

        forward_return = (
            exit_price / entry_price
        ) - 1

        returns.append(forward_return)

    return np.array(returns)


def bootstrap_mean_ci(values, iterations=10000, seed=42):

    rng = np.random.default_rng(seed)

    values = np.asarray(values)

    bootstrap_means = np.empty(iterations)

    for i in range(iterations):

        sample = rng.choice(
            values,
            size=len(values),
            replace=True
        )

        bootstrap_means[i] = np.mean(sample)

    lower = np.percentile(bootstrap_means, 2.5)
    upper = np.percentile(bootstrap_means, 97.5)

    return lower, upper


def bootstrap_difference_ci(
    event_values,
    baseline_values,
    iterations=10000,
    seed=42
):

    rng = np.random.default_rng(seed)

    event_values = np.asarray(event_values)
    baseline_values = np.asarray(baseline_values)

    differences = np.empty(iterations)

    for i in range(iterations):

        event_sample = rng.choice(
            event_values,
            size=len(event_values),
            replace=True
        )

        baseline_sample = rng.choice(
            baseline_values,
            size=len(baseline_values),
            replace=True
        )

        differences[i] = (
            np.mean(event_sample)
            - np.mean(baseline_sample)
        )

    lower = np.percentile(differences, 2.5)
    upper = np.percentile(differences, 97.5)

    return lower, upper


def analyze_holding_period(
    event_returns,
    baseline_returns,
    holding_period
):

    event_returns = np.asarray(event_returns)
    baseline_returns = np.asarray(baseline_returns)

    event_mean = np.mean(event_returns)
    baseline_mean = np.mean(baseline_returns)

    difference = event_mean - baseline_mean

    # Event mean vs zero
    t_zero, p_zero = stats.ttest_1samp(
        event_returns,
        0
    )

    # Event vs baseline
    t_difference, p_difference = stats.ttest_ind(
        event_returns,
        baseline_returns,
        equal_var=False
    )

    # Bootstrap confidence intervals
    event_ci_low, event_ci_high = bootstrap_mean_ci(
        event_returns,
        BOOTSTRAP_ITERATIONS,
        RANDOM_SEED
    )

    difference_ci_low, difference_ci_high = (
        bootstrap_difference_ci(
            event_returns,
            baseline_returns,
            BOOTSTRAP_ITERATIONS,
            RANDOM_SEED
        )
    )

    print("\n" + "=" * 70)
    print(f"HOLDING PERIOD: {holding_period} TRADING DAY(S)")
    print("=" * 70)

    print(f"\nEvent observations: {len(event_returns)}")
    print(f"Baseline observations: {len(baseline_returns)}")

    print("\nMEANS")
    print("-" * 40)

    print(f"Event mean:     {event_mean:.4%}")
    print(f"Baseline mean:  {baseline_mean:.4%}")
    print(f"Difference:     {difference:.4%}")

    print("\n95% BOOTSTRAP CI")
    print("-" * 40)

    print(
        f"Event mean CI: "
        f"[{event_ci_low:.4%}, {event_ci_high:.4%}]"
    )

    print(
        f"Difference CI: "
        f"[{difference_ci_low:.4%}, "
        f"{difference_ci_high:.4%}]"
    )

    print("\nT-TESTS")
    print("-" * 40)

    print(
        f"Event mean vs zero: "
        f"t={t_zero:.4f}, p={p_zero:.4f}"
    )

    print(
        f"Event vs baseline: "
        f"t={t_difference:.4f}, "
        f"p={p_difference:.4f}"
    )

    print("\nOTHER EVENT STATISTICS")
    print("-" * 40)

    print(
        f"Median: "
        f"{np.median(event_returns):.4%}"
    )

    print(
        f"Std deviation: "
        f"{np.std(event_returns, ddof=1):.4%}"
    )

    print(
        f"Win rate: "
        f"{np.mean(event_returns > 0):.2%}"
    )


def main():

    print("=" * 70)
    print("STATISTICAL ANALYSIS")
    print("=" * 70)

    df = load_data()

    event_results = pd.read_csv(EVENT_FILE)

    for holding_period in HOLDING_PERIODS:

        event_returns = event_results.loc[
            event_results["Holding_Period"] == holding_period,
            "Forward_Return"
        ].dropna().values

        baseline_returns = calculate_baseline(
            df,
            holding_period
        )

        analyze_holding_period(
            event_returns,
            baseline_returns,
            holding_period
        )


if __name__ == "__main__":
    main()
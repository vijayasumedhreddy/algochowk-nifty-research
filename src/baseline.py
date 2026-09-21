import pandas as pd
import numpy as np


FILE_PATH = "data/nifty50_daily.csv"

EVENT_THRESHOLD = -0.02
HOLDING_PERIODS = [1, 3, 5]


def load_data(file_path):
    df = pd.read_csv(file_path)

    df["Date"] = pd.to_datetime(df["Date"])

    for column in ["Open", "High", "Low", "Close"]:
        df[column] = pd.to_numeric(df[column])

    df = df.sort_values("Date").reset_index(drop=True)

    df["Daily_Return"] = df["Close"].pct_change()

    return df


def calculate_baseline(df, holding_period):
    """
    Calculate normal forward returns.

    Entry:
        Next trading day's Open

    Exit:
        Close after the selected holding period

    Event days themselves are excluded so that the baseline
    represents ordinary market days.
    """

    returns = []

    for i in range(len(df)):

        entry_position = i + 1
        exit_position = i + holding_period

        if exit_position >= len(df):
            continue

        # Exclude days that satisfy the event definition
        daily_return = df.loc[i, "Daily_Return"]

        if pd.notna(daily_return) and daily_return <= EVENT_THRESHOLD:
            continue

        entry_price = df.loc[entry_position, "Open"]
        exit_price = df.loc[exit_position, "Close"]

        forward_return = (
            exit_price / entry_price
        ) - 1

        returns.append(forward_return)

    return pd.Series(returns)


def main():

    print("=" * 70)
    print("NIFTY 50 EVENT STUDY BASELINE")
    print("=" * 70)

    df = load_data(FILE_PATH)

    print(
        f"\nData range: "
        f"{df['Date'].min().date()} to {df['Date'].max().date()}"
    )

    print(f"Event threshold: {EVENT_THRESHOLD:.1%}")

    for holding_period in HOLDING_PERIODS:

        baseline = calculate_baseline(
            df,
            holding_period
        )

        print("\n" + "-" * 70)
        print(
            f"Baseline holding period: "
            f"{holding_period} trading day(s)"
        )
        print("-" * 70)

        print(f"Observations: {len(baseline)}")
        print(f"Mean return: {baseline.mean():.4%}")
        print(f"Median return: {baseline.median():.4%}")
        print(f"Std deviation: {baseline.std():.4%}")

        win_rate = (baseline > 0).mean()

        print(f"Win rate: {win_rate:.2%}")
        print(f"Minimum: {baseline.min():.4%}")
        print(f"Maximum: {baseline.max():.4%}")


if __name__ == "__main__":
    main()
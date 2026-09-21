import pandas as pd


DATA_PATH = "data/nifty50_daily.csv"

EVENT_THRESHOLD = -0.02
HOLDING_PERIOD = 5
TRANSACTION_COST = 0.001
EXCLUSION_WINDOW = 5

OOS_START = "2021-01-20"


def calculate_returns(df):
    df = df.copy()
    df["return"] = df["Close"].pct_change()
    return df


def detect_events(df, threshold):
    events = []

    for i in range(1, len(df)):
        if df.loc[i, "return"] <= threshold:
            events.append(i)

    return events


def detect_non_overlapping_events(df, threshold, exclusion_window):
    all_events = detect_events(df, threshold)

    selected = []
    last_event = -999999

    for event in all_events:
        if event > last_event + exclusion_window:
            selected.append(event)
            last_event = event

    return selected


def run_backtest(df, event_indices):
    trades = []

    for event_idx in event_indices:

        entry_idx = event_idx + 1
        exit_idx = entry_idx + HOLDING_PERIOD

        if exit_idx >= len(df):
            continue

        entry_price = df.loc[entry_idx, "Open"]
        exit_price = df.loc[exit_idx, "Close"]

        gross_return = (exit_price / entry_price) - 1
        net_return = gross_return - TRANSACTION_COST

        trades.append({
            "event_date": df.loc[event_idx, "Date"],
            "entry_date": df.loc[entry_idx, "Date"],
            "exit_date": df.loc[exit_idx, "Date"],
            "entry_price": entry_price,
            "exit_price": exit_price,
            "gross_return": gross_return,
            "transaction_cost": TRANSACTION_COST,
            "net_return": net_return
        })

    return pd.DataFrame(trades)


def calculate_max_drawdown(returns):
    equity = (1 + returns).cumprod()
    running_max = equity.cummax()
    drawdown = equity / running_max - 1

    return drawdown.min()


def main():

    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"])

    df = calculate_returns(df)

    # --------------------------------------------------
    # OOS period
    # --------------------------------------------------

    oos_mask = df["Date"] >= OOS_START

    oos_df = df.loc[oos_mask].copy().reset_index(drop=True)

    events = detect_non_overlapping_events(
        oos_df,
        EVENT_THRESHOLD,
        EXCLUSION_WINDOW
    )

    trades = run_backtest(oos_df, events)

    if trades.empty:
        print("No OOS trades found.")
        return

    # --------------------------------------------------
    # Performance
    # --------------------------------------------------

    average_return = trades["net_return"].mean()
    median_return = trades["net_return"].median()
    win_rate = (trades["net_return"] > 0).mean()
    volatility = trades["net_return"].std()

    cumulative_return = (
        (1 + trades["net_return"]).prod() - 1
    )

    max_drawdown = calculate_max_drawdown(
        trades["net_return"]
    )

    print("=" * 65)
    print("OUT-OF-SAMPLE BACKTEST")
    print("=" * 65)

    print(f"OOS period: {oos_df['Date'].iloc[0].date()} -> "
          f"{oos_df['Date'].iloc[-1].date()}")

    print(f"Event threshold: {EVENT_THRESHOLD:.2%}")
    print(f"Holding period: {HOLDING_PERIOD} trading days")
    print(f"Transaction cost: {TRANSACTION_COST:.2%} round trip")
    print(f"Non-overlap window: {EXCLUSION_WINDOW} trading days")

    print("\nPerformance:")
    print(f"Trades: {len(trades)}")
    print(f"Average net return: {average_return:.4%}")
    print(f"Median net return: {median_return:.4%}")
    print(f"Win rate: {win_rate:.2%}")
    print(f"Trade volatility: {volatility:.4%}")
    print(f"Compounded net return: {cumulative_return:.2%}")
    print(f"Maximum drawdown: {max_drawdown:.2%}")

    output_path = "results/oos_backtest_trades.csv"

    trades.to_csv(
        output_path,
        index=False
    )

    print(f"\nSaved: {output_path}")


if __name__ == "__main__":
    main()
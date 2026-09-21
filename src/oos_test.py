import pandas as pd
from scipy import stats

DATA_PATH = "data/nifty50_daily.csv"

EVENT_THRESHOLD = -0.02
HOLDING_PERIODS = [1, 3, 5]

TRAIN_RATIO = 0.70


def calculate_returns(df):
    df = df.copy()
    df["Daily_Return"] = df["Close"].pct_change()
    return df


def detect_events(df, threshold):
    return df.index[df["Daily_Return"] <= threshold].tolist()


def forward_return(df, event_idx, holding_period):
    entry_idx = event_idx + 1
    exit_idx = entry_idx + holding_period

    if exit_idx >= len(df):
        return None

    entry_price = df.iloc[entry_idx]["Open"]
    exit_price = df.iloc[exit_idx]["Close"]

    return exit_price / entry_price - 1


def analyze_events(df, event_indices):
    results = []

    for event_idx in event_indices:

        for holding in HOLDING_PERIODS:

            ret = forward_return(
                df,
                event_idx,
                holding
            )

            if ret is not None:

                results.append({
                    "event_index": event_idx,
                    "event_date": df.iloc[event_idx]["Date"],
                    "holding_period": holding,
                    "forward_return": ret
                })

    # Always return the expected columns
    return pd.DataFrame(
        results,
        columns=[
            "event_index",
            "event_date",
            "holding_period",
            "forward_return"
        ]
    )


def print_results(title, results):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    for holding in HOLDING_PERIODS:

        r = results[
            results["holding_period"] == holding
        ]["forward_return"].dropna()

        if len(r) == 0:
            print(
                f"{holding}-day: "
                f"N=0, no complete observations"
            )
            continue

        print(
            f"{holding}-day: "
            f"N={len(r)}, "
            f"Mean={r.mean():.4%}, "
            f"Median={r.median():.4%}, "
            f"Win Rate={(r > 0).mean():.2%}"
        )


def main():

    df = pd.read_csv(DATA_PATH)

    df["Date"] = pd.to_datetime(df["Date"])

    df = (
        df
        .sort_values("Date")
        .reset_index(drop=True)
    )

    df = calculate_returns(df)

    # --------------------------------------------------
    # Chronological 70/30 split
    # --------------------------------------------------

    split_index = int(len(df) * TRAIN_RATIO)

    train = df.iloc[:split_index].copy().reset_index(drop=True)   
    test = df.iloc[split_index:].copy().reset_index(drop=True)

    print("=" * 60)
    print("CHRONOLOGICAL OUT-OF-SAMPLE TEST")
    print("=" * 60)

    print(f"Total observations     : {len(df)}")
    print(f"Training observations  : {len(train)}")
    print(f"OOS observations       : {len(test)}")

    print("\nTraining period:")
    print(
        f"{train['Date'].min().date()} -> "
        f"{train['Date'].max().date()}"
    )

    print("\nOOS period:")
    print(
        f"{test['Date'].min().date()} -> "
        f"{test['Date'].max().date()}"
    )

    print(
        f"\nSplit date: "
        f"{test['Date'].min().date()}"
    )

    # --------------------------------------------------
    # Fixed research rule
    # --------------------------------------------------

    train_events = detect_events(
        train,
        EVENT_THRESHOLD
    )

    test_events = detect_events(
        test,
        EVENT_THRESHOLD
    )

    train_results = analyze_events(
        train,
        train_events
    )

    test_results = analyze_events(
        test,
        test_events
    )

    # --------------------------------------------------
    # Training results
    # --------------------------------------------------

    print_results(
        "TRAINING SAMPLE",
        train_results
    )

    print(
        f"\nEvent threshold: "
        f"{EVENT_THRESHOLD:.1%}"
    )

    print(
        f"Number of events: "
        f"{len(train_events)}"
    )

    # --------------------------------------------------
    # OOS results
    # --------------------------------------------------

    print_results(
        "OUT-OF-SAMPLE SAMPLE",
        test_results
    )

    print(
        f"\nEvent threshold: "
        f"{EVENT_THRESHOLD:.1%}"
    )

    print(
        f"Number of events: "
        f"{len(test_events)}"
    )

    # --------------------------------------------------
    # OOS statistical tests
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("OOS STATISTICAL TESTS")
    print("=" * 60)

    for holding in HOLDING_PERIODS:

        r = test_results[
            test_results["holding_period"] == holding
        ]["forward_return"].dropna()

        if len(r) < 2:
            print(
                f"{holding}-day: "
                f"Not enough observations for t-test"
            )
            continue

        t_stat, p_value = stats.ttest_1samp(
            r,
            0
        )

        print(
            f"{holding}-day: "
            f"mean={r.mean():.4%}, "
            f"t={t_stat:.4f}, "
            f"p={p_value:.4f}"
        )

    # --------------------------------------------------
    # Save results
    # --------------------------------------------------

    test_results.to_csv(
        "results/oos_event_study_results.csv",
        index=False
    )

    print("\nSaved:")
    print(
        "results/oos_event_study_results.csv"
    )


if __name__ == "__main__":
    main()
import pandas as pd
import numpy as np


FILE_PATH = "data/nifty50_daily.csv"

THRESHOLDS = [-0.015, -0.020, -0.025, -0.030]
HOLDING_PERIODS = [1, 3, 5]


def load_data(file_path):
    df = pd.read_csv(file_path)

    df["Date"] = pd.to_datetime(df["Date"])

    for column in ["Open", "High", "Low", "Close"]:
        df[column] = pd.to_numeric(df[column])

    df = df.sort_values("Date").reset_index(drop=True)

    df["Daily_Return"] = df["Close"].pct_change()

    return df


def detect_non_overlapping_events(
    df,
    threshold,
    exclusion_window
):
    candidate_positions = df.index[
        df["Daily_Return"] <= threshold
    ].tolist()

    selected_positions = []
    last_selected_position = (
        -exclusion_window - 1
    )

    for position in candidate_positions:

        if position > (
            last_selected_position
            + exclusion_window
        ):
            selected_positions.append(position)
            last_selected_position = position

    return df.loc[selected_positions].copy()


def calculate_returns(
    df,
    events,
    holding_period
):
    returns = []

    for event_position, event in events.iterrows():

        entry_position = event_position + 1
        exit_position = (
            event_position + holding_period
        )

        if exit_position >= len(df):
            continue

        entry_price = df.loc[
            entry_position, "Open"
        ]

        exit_price = df.loc[
            exit_position, "Close"
        ]

        forward_return = (
            exit_price / entry_price
        ) - 1

        returns.append(forward_return)

    return np.array(returns)


def main():

    print("=" * 70)
    print("ROBUSTNESS ANALYSIS")
    print("=" * 70)

    df = load_data(FILE_PATH)

    results = []

    for threshold in THRESHOLDS:

        events = detect_non_overlapping_events(
            df,
            threshold,
            max(HOLDING_PERIODS)
        )

        print(
            f"\nThreshold: {threshold:.1%}"
        )

        print(
            f"Non-overlapping events: "
            f"{len(events)}"
        )

        for holding_period in HOLDING_PERIODS:

            returns = calculate_returns(
                df,
                events,
                holding_period
            )

            if len(returns) == 0:
                continue

            mean_return = returns.mean()
            median_return = np.median(returns)
            std_return = returns.std(ddof=1)

            win_rate = (
                returns > 0
            ).mean()

            results.append({
                "Threshold": threshold,
                "Holding_Period": holding_period,
                "Observations": len(returns),
                "Mean_Return": mean_return,
                "Median_Return": median_return,
                "Std_Dev": std_return,
                "Win_Rate": win_rate
            })

            print(
                f"  {holding_period}-day | "
                f"N={len(returns):3d} | "
                f"Mean={mean_return:.4%} | "
                f"Median={median_return:.4%} | "
                f"Win={win_rate:.2%}"
            )

    results_df = pd.DataFrame(results)

    output_file = (
        "results/robustness_results.csv"
    )

    results_df.to_csv(
        output_file,
        index=False
    )

    print("\n" + "=" * 70)
    print(
        f"Results saved to: {output_file}"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()
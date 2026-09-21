import pandas as pd
import numpy as np


FILE_PATH = "data/nifty50_daily.csv"

# Primary research parameters
EVENT_THRESHOLD = -0.02
HOLDING_PERIODS = [1, 3, 5]


def load_data(file_path):
    df = pd.read_csv(file_path)

    df["Date"] = pd.to_datetime(df["Date"])

    for column in ["Open", "High", "Low", "Close"]:
        df[column] = pd.to_numeric(df[column])

    df = df.sort_values("Date").reset_index(drop=True)

    # Close-to-close daily return
    df["Daily_Return"] = df["Close"].pct_change()

    return df


def detect_events(df, threshold):
    """
    Detect significant one-day falls.

    An event occurs when the close-to-close return
    is less than or equal to the specified threshold.
    """

    events = df[df["Daily_Return"] <= threshold].copy()

    events["Event_Return"] = events["Daily_Return"]

    return events


def calculate_forward_returns(df, events, holding_periods):
    """
    Calculate forward returns using:

    Entry = next trading day's Open
    Exit  = Close after h trading days
    """

    results = []

    # Map dates to dataframe positions
    date_to_position = {
        date: position
        for position, date in enumerate(df["Date"])
    }

    for event_number, (_, event) in enumerate(events.iterrows(), start=1):

        event_date = event["Date"]
        event_position = date_to_position[event_date]

        # Need at least one trading day after event
        if event_position + 1 >= len(df):
            continue

        entry_position = event_position + 1

        entry_date = df.loc[entry_position, "Date"]
        entry_price = df.loc[entry_position, "Open"]

        for holding_period in holding_periods:

            exit_position = event_position + holding_period

            if exit_position >= len(df):
                continue

            exit_date = df.loc[exit_position, "Date"]
            exit_price = df.loc[exit_position, "Close"]

            forward_return = (
                exit_price / entry_price
            ) - 1

            results.append({
                "Event_Number": event_number,
                "Event_Date": event_date,
                "Event_Return": event["Event_Return"],
                "Entry_Date": entry_date,
                "Entry_Price": entry_price,
                "Holding_Period": holding_period,
                "Exit_Date": exit_date,
                "Exit_Price": exit_price,
                "Forward_Return": forward_return,
            })

    return pd.DataFrame(results)


def main():

    print("=" * 70)
    print("NIFTY 50 EVENT STUDY")
    print("=" * 70)

    df = load_data(FILE_PATH)

    print(f"\nData rows: {len(df)}")
    print(f"Data range: {df['Date'].min().date()} to {df['Date'].max().date()}")

    print(f"\nEvent threshold: {EVENT_THRESHOLD:.1%}")
    print(f"Holding periods: {HOLDING_PERIODS}")

    # Detect events
    events = detect_events(df, EVENT_THRESHOLD)

    print("\n" + "-" * 70)
    print("EVENT DETECTION")
    print("-" * 70)

    print(f"Number of events: {len(events)}")

    if len(events) > 0:
        print("\nDetected events:")
        print(
            events[
                ["Date", "Open", "Close", "Event_Return"]
            ].to_string(index=False)
        )

    # Calculate forward returns
    results = calculate_forward_returns(
        df,
        events,
        HOLDING_PERIODS
    )

    print("\n" + "-" * 70)
    print("FORWARD RETURN RESULTS")
    print("-" * 70)

    if len(results) == 0:
        print("No forward-return observations available.")
        return

    for holding_period in HOLDING_PERIODS:

        subset = results[
            results["Holding_Period"] == holding_period
        ]

        print(f"\nHolding period: {holding_period} trading day(s)")
        print(f"Observations: {len(subset)}")
        print(f"Mean return: {subset['Forward_Return'].mean():.4%}")
        print(f"Median return: {subset['Forward_Return'].median():.4%}")
        print(f"Std deviation: {subset['Forward_Return'].std():.4%}")

        win_rate = (
            subset["Forward_Return"] > 0
        ).mean()

        print(f"Win rate: {win_rate:.2%}")
        print(f"Minimum: {subset['Forward_Return'].min():.4%}")
        print(f"Maximum: {subset['Forward_Return'].max():.4%}")

    # Save results
    output_file = "results/event_study_results.csv"
    results.to_csv(output_file, index=False)

    print("\n" + "=" * 70)
    print(f"Results saved to: {output_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
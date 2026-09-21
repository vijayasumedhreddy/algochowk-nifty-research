import pandas as pd
import numpy as np


FILE_PATH = "data/nifty50_daily.csv"


def validate_data(file_path):
    print("=" * 60)
    print("NIFTY 50 DATA VALIDATION")
    print("=" * 60)

    # Load data
    df = pd.read_csv(file_path)

    print("\n1. BASIC INFORMATION")
    print("-" * 40)
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    # Required columns
    required_columns = ["Date", "Open", "High", "Low", "Close"]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        print(f"ERROR: Missing columns: {missing_columns}")
        return

    print("Required columns: OK")

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Convert OHLC to numeric
    for col in ["Open", "High", "Low", "Close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Missing values
    print("\n2. MISSING VALUES")
    print("-" * 40)
    print(df[required_columns].isna().sum())

    # Duplicate dates
    print("\n3. DUPLICATE DATES")
    print("-" * 40)
    duplicate_count = df["Date"].duplicated().sum()
    print(f"Duplicate dates: {duplicate_count}")

    # Date ordering
    print("\n4. DATE ORDERING")
    print("-" * 40)
    is_sorted = df["Date"].is_monotonic_increasing
    print(f"Sorted ascending: {is_sorted}")

    # Date coverage
    print("\n5. DATE COVERAGE")
    print("-" * 40)
    print(f"First date: {df['Date'].min().date()}")
    print(f"Last date:  {df['Date'].max().date()}")

    # Invalid/non-positive prices
    print("\n6. INVALID PRICE VALUES")
    print("-" * 40)

    non_positive = (
        (df["Open"] <= 0)
        | (df["High"] <= 0)
        | (df["Low"] <= 0)
        | (df["Close"] <= 0)
    ).sum()

    print(f"Non-positive OHLC rows: {non_positive}")

    # OHLC consistency
    print("\n7. OHLC CONSISTENCY")
    print("-" * 40)

    invalid_high = (
        (df["High"] < df["Open"])
        | (df["High"] < df["Close"])
    ).sum()

    invalid_low = (
        (df["Low"] > df["Open"])
        | (df["Low"] > df["Close"])
    ).sum()

    invalid_range = (df["High"] < df["Low"]).sum()

    print(f"High below Open/Close: {invalid_high}")
    print(f"Low above Open/Close:  {invalid_low}")
    print(f"High below Low:        {invalid_range}")

    # Close-to-close returns
    df["Return"] = df["Close"].pct_change()

    print("\n8. RETURN CHECK")
    print("-" * 40)

    print(f"Minimum daily return: {df['Return'].min():.2%}")
    print(f"Maximum daily return: {df['Return'].max():.2%}")

    # Suspiciously large movements
    suspicious = df[df["Return"].abs() >= 0.10]

    print(f"Returns >= 10% in absolute value: {len(suspicious)}")

    if len(suspicious) > 0:
        print("\nSuspicious observations for review:")
        print(
            suspicious[
                ["Date", "Open", "High", "Low", "Close", "Return"]
            ].to_string(index=False)
        )

    # Calendar gaps
    print("\n9. DATE GAPS")
    print("-" * 40)

    date_diff = df["Date"].diff().dt.days
    large_gaps = df.loc[
        date_diff > 7,
        ["Date"]
    ].copy()

    print(f"Gaps greater than 7 calendar days: {len(large_gaps)}")

    if len(large_gaps) > 0:
        print(large_gaps.to_string(index=False))

    # Final status
    print("\n" + "=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    validate_data(FILE_PATH)
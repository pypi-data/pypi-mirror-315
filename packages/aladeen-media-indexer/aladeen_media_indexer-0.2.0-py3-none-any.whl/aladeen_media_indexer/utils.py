import pandas as pd


def apply_smoothing(df: pd.DataFrame, window=7, smoothing_value=3):
    rolling_averages = df.rolling(window=window, win_type="exponential").mean(
        tau=smoothing_value
    )

    # Apply min-max scaling to normalize the rolling averages
    min_max_scaler = lambda x: (x - x.min()) / (x.max() - x.min())
    rolling_averages = rolling_averages.apply(min_max_scaler)

    return rolling_averages

import pandas as pd
import numpy as np

def minmax_downsample(
    df: pd.DataFrame,
    value_col: str = "value",
    ts_col: str = "ts",
    target_points: int = 2000,
) -> pd.DataFrame:
    """
    Min-max downsampling preserving waveform shape.

    Returns a dataframe containing:
    - min points
    - max points
    """

    if len(df) <= target_points:
        return df.copy()

    bucket_size = max(1, len(df) // (target_points // 2)) # floor division which round the decimals to have an integer instead of a float

    values = df[value_col].to_numpy()
    timestamps = df[ts_col].to_numpy()

    result_ts = []
    result_values = []

    for i in range(0, len(values), bucket_size):
        chunk_values = values[i:i + bucket_size]
        chunk_ts = timestamps[i:i + bucket_size]

        if len(chunk_values) == 0:
            continue

        min_idx = np.argmin(chunk_values)
        max_idx = np.argmax(chunk_values)

        result_ts.append(chunk_ts[min_idx])
        result_values.append(chunk_values[min_idx])

        if min_idx != max_idx:
            result_ts.append(chunk_ts[max_idx])
            result_values.append(chunk_values[max_idx])

    reduced_df = pd.DataFrame({
        ts_col: result_ts,
        value_col: result_values,
    })

    reduced_df.sort_values(ts_col, inplace=True)

    return reduced_df
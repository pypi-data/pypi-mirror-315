import pandas as pd
import numpy as np


def fc32(series: pd.Series) -> pd.Series:
    return series.round(5).astype("float32")


def calendar_calculations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate calendar-related values based on the given DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing the required columns.

    Returns:
        pd.DataFrame: The input DataFrame with additional calculated columns.

    Raises:
        KeyError: If any of the required columns are missing in the input DataFrame.
    """
    required_columns = ["mark_back", "mark_front", "strike", "underlying"]
    if not all(col in df.columns for col in required_columns):
        raise KeyError(f"Required columns {required_columns} not found in DataFrame.")

    df["calCost"] = fc32(df["mark_back"] - df["mark_front"])
    df["calGapPct"] = fc32(df["calCost"] / df["mark_front"])
    df["undPricePctDiff"] = fc32((df["strike"] - df["underlying"]) / df["underlying"])
    df["calCostPct"] = fc32((df["calCost"] / df["underlying"]) * 100)
    return df


def calculate_fb_spread(df: pd.DataFrame, fb: str) -> pd.DataFrame:
    """
    Calculate the spread and spread percentage for the specified front or back columns.

    Args:
        df (pd.DataFrame): The input DataFrame containing the required columns.
        fb (str): The identifier for front or back columns. Must be either 'front' or 'back'.

    Returns:
        pd.DataFrame: The input DataFrame with additional calculated columns.

    Raises:
        AssertionError: If the 'fb' argument is not either 'front' or 'back'.
        KeyError: If any of the required columns are missing in the input DataFrame.
    """
    assert fb in ["front", "back"], "fb must be either 'front' or 'back'"
    required_columns = [f"ask_{fb}", f"bid_{fb}", f"mark_{fb}"]
    if not all(col in df.columns for col in required_columns):
        raise KeyError(f"Required columns {required_columns} not found in DataFrame.")

    df[f"spread_{fb}"] = df[f"ask_{fb}"] - df[f"bid_{fb}"]
    df[f"spreadPct_{fb}"] = (df[f"spread_{fb}"] / df[f"mark_{fb}"]).round(2)
    return df


def calculate_cal_spread(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the calendar spread and spread percentage.

    Args:
        df (pd.DataFrame): The input DataFrame containing the required columns.

    Returns:
        pd.DataFrame: The input DataFrame with additional calculated columns.

    Raises:
        KeyError: If any of the required columns are missing in the input DataFrame.
    """
    required_columns = ["ask_cal", "bid_cal", "mark_cal"]
    if not all(col in df.columns for col in required_columns):
        raise KeyError(f"Required columns {required_columns} not found in DataFrame.")

    df["ask_cal"] = fc32(
        df["bid_front"] - df["ask_back"]
    )  # should be larger than bid_cal
    df["bid_cal"] = fc32(
        df["ask_front"] - df["bid_back"]
    )  # should be smaller than ask_cal
    df["spread_cal"] = df["bid_cal"] - df["ask_cal"]
    # Handle division by zero for spreadPct_cal
    # TODO: Handle division by zero for spreadPct_cal
    df["spreadPct_cal"] = df.apply(
        lambda row: (
            np.nan if row["ask_cal"] == 0 else fc32(row["spread_cal"] / row["ask_cal"])
        ),
        axis=1,
    )
    return df


def calculate_spreads(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the spreads and spread percentages for front, back, and calendar columns.

    Args:
        df (pd.DataFrame): The input DataFrame containing the required columns.

    Returns:
        pd.DataFrame: The input DataFrame with additional calculated columns.

    Raises:
        AssertionError: If the 'fb' argument is not either 'front' or 'back'.
        KeyError: If any of the required columns are missing in the input DataFrame.
    """
    df = calculate_fb_spread(df, "front")
    df = calculate_fb_spread(df, "back")
    df = calculate_cal_spread(df)
    return df

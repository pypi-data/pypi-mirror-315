from typing import List

import polars as pl
import io
from rcd_dev_kit.decorator_manager import timeit

def check_na(
    df: pl.DataFrame, raise_error: bool = False, rows: int = 40, cols: int = 40
) -> None:
    """
    Function check_na.
    Use this function to check %na in a polars dataframe, optional: raise Error if any.

    Args:
        df (pl.DataFrame): The Polars DataFrame to check for missing values.
        raise_error (bool, optional): If True, raises a ValueError if any missing values are found. Defaults to False.
        rows (int, optional): Number of rows to display in the output. Defaults to 40.
        cols (int, optional): Number of columns to display in the output. Defaults to 40.

    Returns:
        None

    Examples:
        >>> check_na(df=my_dataframe, raise_error=False)
    """
    pl.Config.set_tbl_rows(rows)
    pl.Config.set_tbl_cols(cols)

    print("Checking na by column...")

    # Count NA values per column
    na_count = df.select([pl.col(c).is_null().sum().alias(c) for c in df.columns])

    # Convert to DataFrame and compute additional metrics
    na_count_df = na_count.melt().rename({"variable": "variable", "value": "na_count"})
    n_row = df.height
    na_count_df = na_count_df.with_columns(
        [
            pl.lit(n_row).alias("n_row"),
            (pl.col("na_count") / n_row * 100).round(2).alias("na_percent"),
        ]
    )

    # Format the percentage column
    na_count_df = na_count_df.with_columns(
        [(pl.col("na_percent").cast(pl.Utf8) + "%").alias("na%")]
    )

    # Print the results
    print(na_count_df)

    pl.Config.restore_defaults()

    # Raise error if specified
    if raise_error:
        if na_count_df["na_count"].unique().len() > 1:
            raise ValueError("There is NA in the dataframe.")
        print("️⭕️ No NA detected!")

    return na_count_df


def check_duplication(
    df: pl.DataFrame, lst_col: List[str], raise_error: bool = False
) -> pl.DataFrame:
    """
    Function check_duplication.
    Use this function to check %duplicates in a Polars dataframe, optional: raise Error if any.

    Args:
        df (pl.DataFrame): The Polars dataframe to check duplicates.
        lst_col (List[str]): List of columns name to verify the duplicates.
        raise_error (bool): True to raise Error when there is any duplicates, by default: False.

    Returns:
        pl.DataFrame: DataFrame containing duplicates.

    Examples:
        >>> from your_module import check_duplication
        >>> check_duplication(df=my_dataframe, lst_col=["col1", "col2"], raise_error=True)
    """
    print(f"Checking duplication at level {lst_col}...")
    df_copy = df.clone()

    # Get the unique rows based on the specified columns
    unique_df = df_copy.unique(subset=lst_col, keep="none")

    # Calculate the number of duplicates
    num_duplicates = df_copy.shape[0] - unique_df.shape[0]
    percentage_duplicates = round(100 * num_duplicates / df_copy.shape[0], 2)

    sentence = f"There are {num_duplicates} duplications which is {percentage_duplicates}% of the whole data."

    if raise_error:
        assert num_duplicates == 0, sentence
        print("️⭕️No duplication detected!")
    else:
        print(sentence)

    # Return the duplicated rows
    df_dup = df_copy.join(unique_df, on=lst_col, how="anti").sort(lst_col)
    return df_dup




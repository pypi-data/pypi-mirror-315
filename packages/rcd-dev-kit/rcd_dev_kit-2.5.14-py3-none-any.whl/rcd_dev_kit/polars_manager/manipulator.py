from typing import List
import polars as pl

def nest_data_pl(
    dataframe: pl.DataFrame, lst_col: List[str], nested_field_name: str
) -> pl.DataFrame:
    """
    Function to nest data in a Polars DataFrame.

    Args:
        dataframe (pl.DataFrame): The Polars DataFrame to nest.
        lst_col (List[str]): List of columns to group by.
        nested_field_name (str): Name of the nested field.

    Returns:
        pl.DataFrame: Nested Polars DataFrame.
    """
    cols = [col for col in dataframe.columns if col not in lst_col]

    # Group by the specified columns and aggregate the rest into a list of dictionaries
    nested_df = (
        dataframe.group_by(lst_col)
        .agg([pl.struct(cols).alias(nested_field_name)])
        .select(lst_col + [nested_field_name])
    )

    return nested_df

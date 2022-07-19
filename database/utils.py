import pandas as pd


def convert_dataframe_row_to_dict(row, keys) -> dict:
    return {keys[i]: row[i] for i in range(len(keys))}

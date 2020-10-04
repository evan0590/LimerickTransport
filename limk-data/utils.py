import pandas as pd


def inner_json_to_pandas(dataframe, string):
    target_df = pd.read_json((dataframe[string]).to_json(), orient='index')
    target_df = target_df.sort_index(axis=0)
    return target_df


def prepend_identifier(dataframe, string):
    return [string + row for row in dataframe]


def parse_time_format(s):
    """Parse all occurences of - to / for correct time formatting."""
    s = s.replace("-", "/")
    s = s.replace("T", " ")
    sep = '+'
    rest = s.split(sep, 1)[0]
    return rest

import pandas as pd


#def clean_data(df: pd.DataFrame) -> pd.DataFrame:
 #   """Put a function that will select the features we want even if we can do that when we
 #   create the X and the y"""
 #   df = df[df[]]


def Basic_df(df: pd.DataFrame) -> pd.DataFrame:

    """ Create a new DataFrame with only two categories, smoking gestures/non-smoking gestures
    adaptable with other features like drinking if Sit and Stand are too flat"""

    new = {'SmokeSD': 1,
            'SmokeST': 1,
            'Sit': 0,
            'Stand': 0}

    Basic_df = df[df['Class_label'].isin(['SmokeSD', 'SmokeST', 'Sit', 'Stand'])]

    Basic_df['Basic_Class'] = Basic_df['Class_label'].map(new)

    return Basic_df

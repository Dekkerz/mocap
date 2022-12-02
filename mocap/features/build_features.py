import pandas as pd
import mocap.utils.params as params

def select_basic_class(df):
    df = df[df['Class_label'].isin(['SmokeSD', 'SmokeST', 'Sit', 'Stand'])]
    return df


def label_encode_class(df: pd.DataFrame) -> pd.DataFrame:

    #df['']=map(df['']params.CLASS_ENCODING)

    return df

def preprocess_main(df: pd.DataFrame) -> pd.DataFrame:

    """
    wrapper to make the current code work, any pre-processing activities can then
    be added to this wrapper once they are working.
    """

    df = label_encode_class(df)

    return df

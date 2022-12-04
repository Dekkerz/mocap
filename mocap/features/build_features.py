import pandas as pd
import mocap.utils.params as params

def label_encode_class(df: pd.DataFrame) -> pd.DataFrame:
    """

    """
    df['Class_Encoded']=df['Class_label'].map(params.CLASS_ENCODING)
    df.drop('Class_label', axis=1)
    return df

def preprocess_main(df: pd.DataFrame) -> pd.DataFrame:

    """
    wrapper to make the current code work, any pre-processing activities can then
    be added to this wrapper once they are working.
    """

    df = label_encode_class(df)
    return df

import os
import pandas as pd

#file has no header

X_path = os.path.join('smoking_data','smoking_input.csv')
y_path = os.path.join('smoking_data','smoking_targets.csv')

#import X and y csv as a Dataframes

X_data=pd.read_csv(X_path, header=None)
y_data=pd.read_csv(y_path, header=None)

#rename the y Dataframe with 'Target' header

y_data.rename(columns={ y_data.columns[0]: "Target" }, inplace = True)

#concatenate the two Dataframes, the X and the y

df = pd.concat([X_data, y_data], axis=1)

#Replace the Nan with the value from the previous column

def nan_preprocess(df):

    df[299].fillna(df[298], inplace=True)
    df[199].fillna(df[198], inplace=True)
    df[99].fillna(df[98], inplace=True)

    return df

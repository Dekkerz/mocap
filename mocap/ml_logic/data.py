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


def read_from_local_file(path=None, participant=None):
""" dekkerz: work-in-progress for loading data files at the moment if you call
without specifying parameters then it will load Participant1_Data.xlsx
"""

    if path is None:
        data_dir=os.path.join('..','data','external','UT_Smoking_Data')

    if participant is None:
        endswith='Participant1_Data.xlsx'

    #loop through files in the data_dir
    for file in os.listdir(data_dir):
        if file.endswith(endswith):
            filename=os.path.join(data_dir,file)
            data=pd.read_excel(filename, header=None)


    return(data)

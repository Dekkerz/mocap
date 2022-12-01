import os
import pandas as pd

#file has no header

#X_path = os.path.join('smoking_data','smoking_input.csv')
#y_path = os.path.join('smoking_data','smoking_targets.csv')

#import X and y csv as a Dataframes

#X_data=pd.read_csv(X_path, header=None)
#y_data=pd.read_csv(y_path, header=None)

#rename the y Dataframe with 'Target' header

#y_data.rename(columns={ y_data.columns[0]: "Target" }, inplace = True)

#concatenate the two Dataframes, the X and the y

#df = pd.concat([X_data, y_data], axis=1)

#Replace the Nan with the value from the previous column

def nan_preprocess(df):

    df[299].fillna(df[298], inplace=True)
    df[199].fillna(df[198], inplace=True)
    df[99].fillna(df[98], inplace=True)

    return df


def read_from_local_file(path=None, participant=None) -> pd.DataFrame:
    """ work-in-progress for loading data files at the moment if you call
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


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """ renaming the column names of our data set 0,1,2,3,4 to actual names
    as per the research paper
    """

    column_names = {0:'timestamp_WD'
                    ,1:'Accelerometer_x_WD'
                    ,2:'Accelerometer_y_WD'
                    ,3:'Accelerometer_z_WD'
                    ,4:'Linear_acceleration_sensor_x_WD'
                    ,5:'Linear_acceleration_sensor_y_WD'
                    ,6:'Linear_acceleration_sensor_z_WD'
                    ,7:'Gyroscope_x_WD'
                    ,8:'Gyroscope_y_WD'
                    ,9:'Gyroscope_z_WD'
                    ,10:'Magnetometer_x_WD'
                    ,11:'Magnetometer_y_WD'
                    ,12:'Magnetometer_z_WD'
                    ,13:'Pressure_sensor_WD'
                    ,14:'Heart_rate_sensor_WD'
                    ,15:'GAP'
                    ,16:'timestamp_PD'
                    ,17:'Accelerometer_x_PD'
                    ,18:'Accelerometer_y_PD'
                    ,19:'Accelerometer_z_PD'
                    ,20:'Linear_acceleration_sensor_x_PD'
                    ,21:'Linear_acceleration_sensor_y_PD'
                    ,22:'Linear_acceleration_sensor_z_PD'
                    ,23:'Gyroscope_x_PD'
                    ,24:'Gyroscope_y_PD'
                    ,25:'Gyroscope_z_PD'
                    ,26:'Magnetometer_x_PD'
                    ,27:'Magnetometer_y_PD'
                    ,28:'Magnetometer_z_PD'
                    ,29:'GPS_lat_PD'
                    ,30:'GPS_long_PD'
                    ,31:'Class_label'}

    df.rename(columns=column_names,inplace=True)

    return df

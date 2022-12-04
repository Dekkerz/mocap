import pandas as pd
import mocap.utils.params as params
from sklearn.preprocessing import MinMaxScaler

def feature_normalization(df: pd.DataFrame) -> pd.DataFrame:

    MinMaxscaler=MinMaxScaler()
    df[['Accelerometer_x_WD_MMS'
        ,'Accelerometer_y_WD_MMS'
        ,'Accelerometer_z_WD_MMS'
        ,'Linear_acceleration_sensor_x_WD_MMS'
        ,'Linear_acceleration_sensor_y_WD_MMS'
        ,'Linear_acceleration_sensor_z_WD_MMS'
        ,'Gyroscope_x_WD_MMS'
        ,'Gyroscope_y_WD_MMS'
        ,'Gyroscope_z_WD_MMS'
        ,'Magnetometer_x_WD_MMS'
        ,'Magnetometer_y_WD_MMS'
        ,'Magnetometer_z_WD_MMS'
        ,'Pressure_sensor_WD_MMS'
        ,'Heart_rate_sensor_WD_MMS'
        ]]=MinMaxscaler.fit_transform(df[['Accelerometer_x_WD'
        ,'Accelerometer_y_WD'
        ,'Accelerometer_z_WD'
        ,'Linear_acceleration_sensor_x_WD'
        ,'Linear_acceleration_sensor_y_WD'
        ,'Linear_acceleration_sensor_z_WD'
        ,'Gyroscope_x_WD'
        ,'Gyroscope_y_WD'
        ,'Gyroscope_z_WD'
        ,'Magnetometer_x_WD'
        ,'Magnetometer_y_WD'
        ,'Magnetometer_z_WD'
        ,'Pressure_sensor_WD'
        ,'Heart_rate_sensor_WD'
        ]])

    return(df)

def label_encode_class(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simple encoding from string to numeric for the class
    """
    df['Class_Encoded']=df['Class_label'].map(params.CLASS_ENCODING)
    #drop original as we already have it from previous code
    # y_chunk = scrubbed_data_chunk[['Class_label']]
    df.drop(columns=['Class_label'])
    return df

def preprocess_main(df: pd.DataFrame) -> pd.DataFrame:

    """
    wrapper to make the current code work, any pre-processing activities can then
    be added to this wrapper once they are working.
    """
    df = label_encode_class(df)
    df = feature_normalization(df)

    return df

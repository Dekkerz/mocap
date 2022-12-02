import pandas as pd
import re

def scrub_data(df: pd.DataFrame, file: str = "") -> pd.DataFrame:
    """
    clean raw data by removing buggy or irrelevant transactions
    or columns for the training set
    """
    participant_num=''.join([d for d in re.findall(r'\d+',file)])
    df['Participant_Num']=participant_num

    # remove useless/redundant columns
    df = df.drop(columns=['timestamp_WD'
                    ,'GAP'
                    ,'timestamp_PD'
                    ,'Accelerometer_x_PD'
                    ,'Accelerometer_y_PD'
                    ,'Accelerom  eter_z_PD'
                    ,'Linear_acceleration_sensor_x_PD'
                    ,'Linear_acceleration_sensor_y_PD'
                    ,'Linear_acceleration_sensor_z_PD'
                    ,'Gyroscope_x_PD'
                    ,'Gyroscope_y_PD'
                    ,'Gyroscope_z_PD'
                    ,'Magnetometer_x_PD'
                    ,'Magnetometer_y_PD'
                    ,'Magnetometer_z_PD'
                    ,'GPS_lat_PD'
                    ,'GPS_long_PD'])

    print("\n✅ data cleaned")

    return df

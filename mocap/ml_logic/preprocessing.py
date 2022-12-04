import pandas as pd
import re
from colorama import Fore, Style
import mocap.utils.params as params
import datetime

def engineered_timestamp(df: pd.DataFrame, min_timestamp: int = None) -> pd.DataFrame:
    """
    Since the timestamp is incorrect we have to engineer a timestamp.
    The timestamp is incorrect because there are bugs with the logger where we see "leakage"
    of the data into the next seconds, there are also outliers where the data itself appears
    correct but we see 800+ samples for the same second.

    Ideally we should have 50 samples / second to equal the 50Hz sampling rate as outlined in the
    research paper
    """

    chunk_id=1
    start_index=0
    chunk_size=params.FREQUENCY
    no_of_rows=df.shape[0]

    if min_timestamp is None:
        min_timestamp=df[0:1]['timestamp_WD'][0]

    engineered_timestamp=min_timestamp

    while (True):

        #print(Fore.BLUE + f"\nProcessing chunk n°{chunk_id}..." + Style.RESET_ALL)
        end_index=chunk_id*chunk_size

        if end_index > no_of_rows:
            end_index=no_of_rows

        #print(Fore.BLUE + f"\nindex_range:{start_index}:{end_index}" + Style.RESET_ALL)

        df_chunk=df.iloc[start_index:end_index]
        df_chunk['Engineered_Timestamp']=datetime.datetime.fromtimestamp(engineered_timestamp/1000)

        #print(Fore.BLUE + f"\nTimeStamp:{datetime.datetime.fromtimestamp(engineered_timestamp/1000)}" + Style.RESET_ALL)

        if chunk_id == 1:
            data=df_chunk
        else:
            data=pd.concat([data,df_chunk])

        if no_of_rows == end_index:
            break

        chunk_id += 1
        start_index=end_index
        # add 1000 milli seconds for the next chunk
        engineered_timestamp += 1000

    return(data)

def drop_redundant_cols(df: pd.DataFrame) -> pd.DataFrame:
    """
    drop the columns from the phone data which are irrelevant for the model
    """
    # remove useless/redundant columns
    #print(df.columns)

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

    return(df)

def add_participant_num(df: pd.DataFrame,file: str = "") -> pd.DataFrame:

    participant_num=''.join([d for d in re.findall(r'\d+',file)])
    df['Participant_Num']=participant_num
    return(df)

def scrub_data(df: pd.DataFrame, file: str = "",min_timestamp: int = None) -> pd.DataFrame:
    """
    clean raw data by removing buggy or irrelevant transactions
    or columns for the training set
    """
    #df.drop_duplicates(inplace=True)
    df=add_participant_num(df,file)
    df=engineered_timestamp(df,min_timestamp)
    df=drop_redundant_cols(df)

    print("\n✅ data cleaned")

    return df

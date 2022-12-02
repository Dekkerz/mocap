import os
import pandas as pd
import numpy as np
import re
from colorama import Fore, Style
import mocap.utils.params as params
from mocap.features.build_features import preprocess_main
from mocap.data.local import get_pandas_chunk, save_local_chunk

def save_chunk(destination_name: str,
               is_first: bool,
               data: pd.DataFrame) -> None:
    """
    save chunk
    """

    #if os.environ.get("DATA_SOURCE") == "big query":
    #
    #    save_bq_chunk(table=destination_name,
    #                  data=data,
    #                  is_first=is_first)
    #
    #    return

    save_local_chunk(path=destination_name,
                     data=data,
                     is_first=is_first)

def get_chunk(source_name: str,
              index: int = 0,
              chunk_size: int = None,
              verbose=False) -> pd.DataFrame:

    """
    Return a `chunk_size` rows from the source dataset, starting at row `index` (included)
    Always assumes `source_name` (CSV or Big Query table) have headers,
    and do not consider them as part of the data `index` count.
    """

    if "processed" in source_name:
        columns = None
        #dtypes = DTYPES_PROCESSED_OPTIMIZED
    else:
        columns = params.COLUMN_NAMES_RAW
        dtypes = params.DTYPES_RAW_OPTIMIZED_HEADLESS
        #if os.environ.get("DATA_SOURCE") == "big query":
        #    dtypes = DTYPES_RAW_OPTIMIZED
        #else:

    #if os.environ.get("DATA_SOURCE") == "big query":
    #
    #    chunk_df = get_bq_chunk(table=source_name,
    #                            index=index,
    #                            chunk_size=chunk_size,
    #                            dtypes=dtypes,
    #                            verbose=verbose)
    #
    #    return chunk_df

    chunk_df = get_pandas_chunk(path=source_name,
                                index=index,
                                chunk_size=chunk_size,
                                dtypes=dtypes,
                                columns=columns,
                                verbose=verbose)

    return chunk_df

def read_file(filename):

    print("\n⭐️ def: read_file")

    # Iterate on the dataset, in chunks

    chunk_id = 0
    row_count = 0
    cleaned_row_count = 0
    source_name = filename
    base_filename = os.path.basename(filename).split('.')[0]
    destination_name = os.path.join(params.LOCAL_DATA_PATH,"processed",f'{base_filename}.csv')

    while (True):
        print(Fore.BLUE + f"\nProcessing chunk n°{chunk_id}..." + Style.RESET_ALL)

        data_chunk = get_chunk(
            source_name = source_name,
            index=chunk_id * params.CHUNK_SIZE,
            chunk_size = params.CHUNK_SIZE
        )

        # Break out of while loop if data is none
        if data_chunk is None:
            print(Fore.BLUE + "\nNo data in latest chunk..." + Style.RESET_ALL)
            break

        row_count += data_chunk.shape[0]

        #data_chunk_cleaned = clean_data(data_chunk)
        #cleaned_row_count += len(data_chunk_cleaned)

        # Break out of while loop if cleaning removed all rows
        #if len(data_chunk_cleaned) == 0:
        #    print(Fore.BLUE + "\nNo cleaned data in latest chunk..." + Style.RESET_ALL)
        #    break

        #X_chunk = data_chunk_cleaned.drop("fare_amount", axis=1)
        #y_chunk = data_chunk_cleaned[["fare_amount"]]

        #Need to replace this with Labels 1,2,3,4,5,6?
        y_chunk = data_chunk[['Class_label']]
        X_chunk = data_chunk
        X_processed_chunk = preprocess_main(X_chunk)

        data_processed_chunk = pd.DataFrame(
            np.concatenate((X_processed_chunk, y_chunk), axis=1)
        )

        # Save and append the chunk
        is_first = chunk_id == 0

        save_chunk(
            destination_name=destination_name,
            is_first=is_first,
            data=data_processed_chunk
        )

        chunk_id += 1

    if row_count == 0:
        print("\n✅ No new data for the preprocessing 👌")
        return None

    print(f"\n✅ Data processed saved entirely: {row_count} rows ({cleaned_row_count} cleaned)")

    return None

def pre_load_data(mode, path=None, endswith=None):
    """
    Reads the raw data files.

    args:

    endswith - The wildcard can be used to pre-load on specific participant data
    path - overwrite the default path from the env file

    """

    valid_modes=params.validator.get('PRELOAD_MODE')

    if mode not in valid_modes:
        raise NameError(f"Invalid mode for {mode} must be in {valid_modes}")

    #the mode will be processed or raw
    if path is None:
        data_dir=os.path.join(params.LOCAL_DATA_PATH,mode)

    if endswith is None:
        endswith='Participant1_Data.xlsx'

    #loop through files in the data_dir
    for file in os.listdir(data_dir):
        if file.endswith(endswith):
            filename=os.path.join(data_dir,file)
            read_file(filename)

def read_from_local_file(path=None, endswith=None) -> pd.DataFrame:
    """ work-in-progress for loading data files at the moment if you call
    without specifying parameters then it will load Participant1_Data.xlsx
    """

    def read_excel(list) -> pd.DataFrame:

        for f in list:
            data=pd.read_excel(filename, header=None)
            basename=os.path.basename(f)
            participant_num = ''.join([ d for d in re.findall(r'\d+',basename)])
            data['Participant_Num']=participant_num

        return(data)

    if path is None:
        data_dir=os.path.join('..','data','external','UT_Smoking_Data')

    if endswith is None:
        endswith='Participant1_Data.xlsx'

    allfiles=[]
    #loop through files in the data_dir
    for file in os.listdir(data_dir):
        if file.endswith(endswith):
            filename=os.path.join(data_dir,file)
            allfiles.append(filename)

    return(pd.concat(map(read_excel,allfiles)))

def rename_columns(data: pd.DataFrame) -> pd.DataFrame:
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
                    ,19:'Accelerom  eter_z_PD'
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

    data.rename(columns=column_names,inplace=True)

    return data

import os
import pandas as pd
import numpy as np
from colorama import Fore, Style
import mocap.utils.params as params
from mocap.features.build_features import preprocess_main
from mocap.ml_logic.preprocessing import scrub_data
from mocap.data.local import get_pandas_chunk, save_local_chunk

def save_chunk(destination_name: str,
               is_first: bool,
               data: pd.DataFrame,
               chunk_id: int) -> None:
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
                     is_first=is_first,
                     chunk_id=chunk_id)

def get_chunk(source_name: str,
              index: int = 0,
              chunk_size: int = None,
              verbose=True) -> pd.DataFrame:

    """
    Return a `chunk_size` rows from the source dataset, starting at row `index` (included)
    Always assumes `source_name` (CSV or Big Query table) have headers,
    and do not consider them as part of the data `index` count.
    """

    if "processed" in source_name:
        #dtypes=DTYPES_PROCESSED_OPTIMIZED
        #columns=DTYPES_PROCESSED_OPTIMIZED.keys()
        columns=None
    else:
        columns=params.COLUMN_NAMES_RAW
        dtypes=params.DTYPES_RAW_OPTIMIZED_HEADLESS
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
    scrubbed_row_count = 0
    source_name = filename
    base_filename = os.path.basename(filename).split('.')[0]
    destination_name = os.path.join(params.LOCAL_DATA_PATH,"processed",base_filename)

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

        scrubbed_data_chunk = scrub_data(data_chunk,base_filename)
        scrubbed_row_count += len(scrubbed_data_chunk)


        # Break out of while loop if cleaning removed all rows
        if len(scrubbed_data_chunk) == 0:
            print(Fore.BLUE + "\nNo cleaned data in latest chunk..." + Style.RESET_ALL)
            break

        X_chunk = scrubbed_data_chunk.drop('Class_label', axis=1)
        y_chunk = scrubbed_data_chunk[['Class_label']]

        #Need to replace this with Labels 1,2,3,4,5,6?
        X_processed_chunk = preprocess_main(X_chunk)

        data_processed_chunk = pd.DataFrame(
            np.concatenate((X_processed_chunk, y_chunk), axis=1)
        )

        # Save and append the chunk
        is_first = chunk_id == 0

        save_chunk(
            destination_name=destination_name,
            is_first=is_first,
            data=data_processed_chunk,
            chunk_id=chunk_id
        )

        chunk_id += 1

    if row_count == 0:
        print("\n✅ No new data for the preprocessing 👌")
        return None

    print(f"\n✅ Data processed saved entirely: {row_count} rows ({scrubbed_row_count} scrubbed)")

    return None

def pre_load_data(path=None, endswith=None):
    """
    Reads the raw data files and creates pickle files or csv with the pre-processed data
    """
    if path is None:
        data_dir=os.path.join(params.LOCAL_DATA_PATH,params.UNPROCESSED_DATA)

    if endswith is None:
        endswith='Participant1_Data.xlsx'

    #loop through files in the data_dir
    for file in os.listdir(data_dir):
        if file.endswith(endswith):
            filename=os.path.join(data_dir,file)
            read_file(filename)

def load_pickles(path=None, startswith=None) -> pd.DataFrame:
    """ work-in-progress for loading data files at the moment if you call
    without specifying parameters then it will load Participant1_Data.xlsx
    """

    def load_pickles(files) -> pd.DataFrame:

        #data.rename(columns=column_names,inplace=True)
        df=pd.read_pickle(files)
        df.rename(columns=params.COLUMN_NAMES_PROCESSED,inplace=True)

        return(df)

    if path is None:
        data_dir=os.path.join(params.LOCAL_DATA_PATH,params.PROCESSED_DATA)

    if startswith is None:
        startswith='Participant1_Data'

    files=[]
    #loop through files in the data_dir
    for file in os.listdir(data_dir):
        if file.startswith(startswith):
            filename=os.path.join(data_dir,file)
            files.append(filename)

    return(pd.concat(map(load_pickles,files)))

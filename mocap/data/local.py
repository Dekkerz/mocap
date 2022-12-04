import pandas as pd
from colorama import Fore, Style

def save_local_chunk(path: str,
                     data: pd.DataFrame,
                     is_first: bool,
                     chunk_id: int):
    """
    save a chunk of the dataset to local disk
    """
    path=f'{path}.pkl'

    if not is_first:
        df=pd.read_pickle(path)
        data=pd.concat([df,data])

    print(Fore.BLUE + f"\nSave data to {path}:" + Style.RESET_ALL)
    data.to_pickle(path)

def get_pandas_chunk(path: str,
                     index: int,
                     chunk_size: int,
                     dtypes,
                     columns: list = None,
                     verbose=True) -> pd.DataFrame:

    """
    return a chunk of the raw dataset from local disk or cloud storage
    """
    if verbose:
        print(Fore.MAGENTA + f"Source data from {path}: {chunk_size if chunk_size is not None else 'all'} rows (from row {index})" + Style.RESET_ALL)

    try:

        #if not params.HEADERS:
        #    header=None
        #else:
        #    header=0

        df = pd.read_excel(
                path,
                skiprows=index,  # skip header
                nrows=chunk_size,
                dtype=dtypes,
                header=None)  # read all rows

        #pd.read_excel doesn't seem to be raising the pd.errors handler, therefore adding a check based on the shape
        no_of_rows_returned=df.shape[0]

        if verbose:
            print(Fore.MAGENTA + f"No, of rows returns({no_of_rows_returned})" + Style.RESET_ALL)

        if no_of_rows_returned > 0:

            # read_excel(dtypes=...) will silently fail to convert data types, if column names do no match dictionnary key provided.
            if isinstance(dtypes, dict):
                assert dict(df.dtypes) == dtypes

            if columns is not None:
                print(df.columns)
                print(columns)
                df.columns = columns

    except pd.errors.EmptyDataError:

        return None  # end of data

    return df

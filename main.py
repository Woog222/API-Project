from google.oauth2 import service_account
from googleapiclient.discovery import build
import googleapiclient.errors
import os, json
import pandas as pd
import numpy as np
import kbs.kbs_info as KBS
from kbs.data_updater import get_data
from kbs.data_fetcher import *
from kbs.parser import arg_parse

def current_time():
    now = datetime.now()  # Get current date and time
    now = now + timedelta(hours=9)
    return now.strftime("%m%d_%H%M%S")

if __name__ == "__main__":

    ## Arg Parsing
    args = arg_parse()
    num_results = args.num_results

    ## Get Credentials
    credentials = service_account.Credentials.from_service_account_file(
        os.path.join('info', 'service_account_key.json'), scopes=KBS.scopes)
    youtube = build(KBS.API_SERVICE_NAME, KBS.API_VERSION, credentials=credentials)
    cur_time = current_time()
    ## load current dataframe
    try:
        df = pd.read_csv(KBS.DATA_PATH)
    except:
        df = pd.DataFrame(columns=KBS.COLUMNS)

    try:
        meta = pd.read_csv(KBS.META_PATH, index_col='videoId')
    except:
        meta = pd.DataFrame(columns=KBS.META_COLUMNS)
        meta.set_index('videoId', inplace=True)

    ## with new data
    new_df = get_data(youtube, df, num_results = num_results)
    new_df['time'] = cur_time
    with open(os.path.join("data", "log.txt"), "a") as log:
        log.write(f"{meta.shape[0]:8}(existing) + {new_df.shape[0]-meta.shape[0]:8}(new) = {new_df.shape[0]:8} received. ({cur_time})\n")

    df = pd.concat([df, new_df[KBS.COLUMNS]], ignore_index=True)
    df.to_csv(KBS.DATA_PATH, index=False)

    meta_new = new_df[KBS.META_COLUMNS].copy()
    meta_new.set_index('videoId', inplace=True)

    new_ids = (meta_new.index).difference(meta.index).unique()
    for id in new_ids:
        meta.loc[id] = meta_new.loc[id]
    meta.to_csv(KBS.META_PATH, index_label='videoId')


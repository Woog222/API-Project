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



if __name__ == "__main__":

    args = arg_parse()
    num_results = args.num_results

    credentials = service_account.Credentials.from_service_account_file(
        os.path.join('info', 'service_account_key.json'), scopes=KBS.scopes)
    # Run the OAuth flow to obtain credentials
    youtube = build(KBS.API_SERVICE_NAME, KBS.API_VERSION, credentials=credentials)
    try:
        df = pd.read_csv(KBS.DATA_PATH)
    except:
        df = pd.DataFrame(columns=KBS.COLUMNS)


    new_df = get_data(youtube, df, num_results = num_results)
    df = pd.concat([df, new_df], ignore_index=True)

    df.to_csv(KBS.DATA_PATH, index=False)
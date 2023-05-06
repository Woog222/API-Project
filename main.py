import os
import json
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import googleapiclient.errors
import pandas as pd
import numpy as np
from google.oauth2 import service_account
import kbs.kbs_info as KBS
from kbs.data_updater import update

from kbs.data_fetcher import *

columns = [
    'videoId',
    'publishedAt',
    'title',
    'description',
    'categoryId',
    'duration',
    'dimension',
    'definition',
    'caption',
    'contentRating',
    'viewCount',
    'likeCount',
    'commentCount'
]


if __name__ == "__main__":

    credentials = service_account.Credentials.from_service_account_file(
        os.path.join('info', 'service_account_key.json'), scopes=KBS.scopes)
    # Run the OAuth flow to obtain credentials
    youtube = build(KBS.API_SERVICE_NAME, KBS.API_VERSION, credentials=credentials)
    try:
        df = pd.read_csv(KBS.DATA_PATH)
    except:
        df = pd.DataFrame(columns=KBS.COLUMNS)

    print(df.columns)

    update(youtube, df)
    print(df.head())
    df.to_csv(KBS.DATA_PATH, index=False)
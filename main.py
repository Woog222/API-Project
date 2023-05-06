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

    df = pd.read_csv(KBS.DATA_PATH, index_col= KBS.INDEX_COL)
    update(youtube, df)
    df.to_csv(KBS.DATA_PATH, index_label=KBS.INDEX_COL)
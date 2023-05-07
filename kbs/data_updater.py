import kbs.kbs_info as KBS
import pandas as pd
import os
from kbs.data_fetcher import *



def update(youtube, df):

    video_ids = df.index.to_list() + get_video_ids(youtube, numResults= 2)
    video_ids = list(set(video_ids))

    return get_youtube_datas(youtube=youtube, df=df, video_ids=video_ids)

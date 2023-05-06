import kbs.kbs_info as KBS
import pandas as pd
import os
from kbs.data_fetcher import *



def update(youtube, df):

    video_ids = df.index.to_list() + get_video_ids(youtube)
    video_ids = list(set(video_ids))

    get_youtube_datas(youtube=youtube, df=df, video_ids=video_ids)

import kbs.kbs_info as KBS
import pandas as pd
import os
from kbs.data_fetcher import *



def get_data(youtube, df, num_results):

    video_ids = df['videoId'].to_list() + get_video_ids(youtube, numResults= num_results)
    video_ids = list(set(video_ids))

    print(video_ids)

    return get_youtube_datas(youtube=youtube, df=df, video_ids=video_ids)

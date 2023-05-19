import kbs.kbs_info as KBS
from datetime import datetime, timedelta
import pytz
import pandas as pd
from tqdm import tqdm


def convert_time(publishedAt):
    published_time = datetime.fromisoformat(publishedAt[:-1])
    utc_time = pytz.utc.localize(published_time)
    kst_time = utc_time + timedelta(hours=9)
    return kst_time.strftime("%Y-%m-%d %H:%M:%S")


def get_youtube_datas(youtube, video_ids):

    batch_size= 50
    id_chunks = [video_ids[i:i + batch_size] for i in range(0, len(video_ids), batch_size)]
    df = pd.DataFrame(columns = KBS.COLUMNS)

    for ids in tqdm(id_chunks):
        response = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(ids)
        ).execute()

        for video_data in response['items']:
            temp = {}

            temp['videoId'] = video_data['id']
            temp['publishedAt'] = convert_time(video_data['snippet']['publishedAt'])
            temp['title'] = video_data['snippet']['title']
            temp['description'] = video_data['snippet']['description']
            temp['categoryId'] = video_data['snippet']['categoryId']
            temp['duration'] = video_data['contentDetails']['duration']
            temp['dimension'] = video_data['contentDetails']['dimension']
            temp['definition'] = video_data['contentDetails']['definition']
            temp['caption'] = video_data['contentDetails']['caption']
            temp['viewCount'] = video_data['statistics']['viewCount']
            temp['likeCount'] = video_data['statistics']['likeCount']
            try:
                temp['commentCount'] = video_data['statistics']['commentCount']
            except:
                temp['commentCount'] = -1
            temp_df = pd.DataFrame(temp, index=[0])
            df = pd.concat([df, temp_df], ignore_index=True)
    return df


def get_video_ids(youtube, numResults=50):

    uploads_playlist_id = get_upload_list_id(youtube)

    # Retrieve the most recent videos uploaded to the channel
    video_ids = []

    playlist_items = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=uploads_playlist_id,
        maxResults=numResults  # Set the number of videos to retrieve
    ).execute()

    for item in playlist_items['items']:
        video_ids.append(item['contentDetails']['videoId'])

    return video_ids



def get_upload_list_id(youtube):
    channel_info = youtube.channels().list(
        part='contentDetails',
        id=KBS.CHANNEL_ID
    ).execute()

    uploads_playlist_id = channel_info['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return uploads_playlist_id

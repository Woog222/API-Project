import os

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
DEV_KEY = os.environ.get('GOOGLE_API_KEY')
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CHANNEL_ID = "UCcQTRi69dsVYHN3exePtZ1A"
INDEX_COL = 'videoId'
COLUMNS = [
    'videoId',
    'viewCount',
    'likeCount',
    'commentCount'
]

META_COLUMNS = [
    'videoId',
    'publishedAt',
    'title',
    'description',
    'categoryId',
    'duration',
    'dimension',
    'definition',
    'caption',
]
DATA_PATH = os.path.join('data', 'data.csv')
META_PATH = os.path.join('data', 'meta.csv')
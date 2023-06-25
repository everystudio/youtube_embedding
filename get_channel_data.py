from googleapiclient.discovery import build

def get_channel_info(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=channel_id
    )

    response = request.execute()

    return response

from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv('API_KEY')
channel_id = 'UCee7U0mnWxA-0i6lCx5N73Q'

channel_info = get_channel_info(api_key, channel_id)
print(channel_info['items'][0]['snippet']['title'])
#print(channel_info)

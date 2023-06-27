# youtube_api.py
from googleapiclient.discovery import build
import time
from datetime import datetime
import os
from dotenv import load_dotenv

def get_video_urls(api_key, channel_id):

    print(api_key)

    # 現在の日時
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")

    filename = f"mp3/{channel_id}_{date_str}.txt"
    youtube = build('youtube', 'v3', developerKey=api_key)

    def get_channel_videos(channel_id):
        res = youtube.search().list(part='id', channelId=channel_id, maxResults=50).execute()
        videos = []
        
        while res:
            videos += res['items']
            # check if there are next pages
            if 'nextPageToken' in res:
                res = youtube.search().list(part='id', channelId=channel_id, maxResults=50, pageToken=res['nextPageToken']).execute()
            else:
                break

        return videos
    
    def get_from_file(filename):
        video_urls = []
        with open(filename , 'r') as f:
            video_urls = [line.rstrip() for line in f]
        
        return video_urls
    
    if not os.path.exists(filename):
        print ("search youtube")
        videos = get_channel_videos(channel_id)
        
        video_urls = []
        base_url = "https://www.youtube.com/watch?v="
        for video in videos:
            if video['id']['kind'] == "youtube#video":
                video_urls.append(base_url + video['id']['videoId'])
        
        with open(filename, 'w') as f:
            f.write('\n'.join(video_urls))
    else :
        print ("from localfile")

    ret_urls = get_from_file(filename)

    # APIのリクエスト制限を守るために適切なウェイトを設けることを忘れないでください
    time.sleep(1)

    return ret_urls

#load_dotenv()
#api_key = os.getenv('API_KEY')
#channel_id = 'UCee7U0mnWxA-0i6lCx5N73Q'
#get_video_urls(api_key,channel_id)


# youtube_api.py
from googleapiclient.discovery import build
import time

def get_video_urls(api_key, channel_id):
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

    videos = get_channel_videos(channel_id)
    
    video_urls = []
    base_url = "https://www.youtube.com/watch?v="
    for video in videos:
        if video['id']['kind'] == "youtube#video":
            video_urls.append(base_url + video['id']['videoId'])

    # APIのリクエスト制限を守るために適切なウェイトを設けることを忘れないでください
    time.sleep(1)
    
    return video_urls

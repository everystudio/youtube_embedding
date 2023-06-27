from get_urls import get_video_urls
from get_channel_data import get_channel_info
from dl_mp3 import download_as_mp3
from whisper_convert import output_whisper_result
from dotenv import load_dotenv
import os
import whisper

load_dotenv()

api_key = os.getenv('API_KEY')
channel_id = 'UCee7U0mnWxA-0i6lCx5N73Q'

#channel_info = get_channel_info(api_key,channel_id)
#channel_title = channel_info['items'][0]['snippet']['title']

file_path = 'mp3/' + channel_id

if not os.path.exists(file_path):
    os.mkdir(file_path)

video_urls = get_video_urls(api_key,channel_id)
model = whisper.load_model("medium")

for i,url in enumerate(video_urls):
    filename = download_as_mp3(url,file_path)
    print(filename)
    output_whisper_result(file_path,filename,model)

    if 0 <= i:
        break


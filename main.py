from get_urls import get_video_urls
from get_channel_data import get_channel_info
from dl_mp3 import download_as_mp3
from whisper_convert import output_whisper_result
from dotenv import load_dotenv
import os
import whisper
import logging

logging.basicConfig(filename='logfile.txt',level=logging.INFO)
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

load_dotenv()

log_directory = os.getenv('LOG_DIRECTORY')
if not os.path.exists(log_directory) :
    os.makedirs(log_directory)

api_key = os.getenv('API_KEY')
channel_id = 'UCee7U0mnWxA-0i6lCx5N73Q'

#channel_info = get_channel_info(api_key,channel_id)
#channel_title = channel_info['items'][0]['snippet']['title']

file_path = 'mp3/' + channel_id

if not os.path.exists(file_path):
    os.mkdir(file_path)

video_urls = get_video_urls(api_key,channel_id)
model = whisper.load_model("medium")

whisper_count = 0
for i,url in enumerate(video_urls):
    filename = download_as_mp3(url,file_path)
    print(filename)
    if output_whisper_result(file_path,filename,model):
        whisper_count += 1

    if 1 <= whisper_count:
        break


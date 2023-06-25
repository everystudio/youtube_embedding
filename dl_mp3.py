import yt_dlp
import os

def download_as_mp3(url,output_path):
    options = {
        'format': 'bestaudio/best',
        'nooverwrites': True,  # 既に存在するファイルを上書きしない
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        #'outtmpl': output_path + '/%(title)s.%(ext)s',  # ADD THIS LINE
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(url,download=False)
        filename =f"{output_path}/{info_dict['title']}.mp3"

        if not os.path.exists(filename):
            options.update({'outtmpl': filename})
            with yt_dlp.YoutubeDL(options) as ydl_download:
                ydl.download([url])

        return filename

url = 'https://www.youtube.com/watch?v=kq9eMn3iHqg'  # Replace with your YouTube video URL
download_as_mp3(url,'mp3')
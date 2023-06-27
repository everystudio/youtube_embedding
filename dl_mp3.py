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
        filename = info_dict['title'].replace('/','_')
        file_path =f"{output_path}/{filename}"

        print("Download File Path:" + file_path)

        if not os.path.exists(file_path+".mp3"):
            print("Not Exits!!!")
            options.update({'outtmpl': file_path})
            with yt_dlp.YoutubeDL(options) as ydl_download:
                ydl.download([url])
        else:
            print("File Exists!!!")

        # 返すのはファイル名（ただし拡張子なし）
        return filename

#url = 'https://www.youtube.com/watch?v=rDOrH18Iyn0'  # Replace with your YouTube video URL
#download_as_mp3(url,'mp3')
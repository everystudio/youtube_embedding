import whisper
from datetime import timedelta
from srt import Subtitle
import srt
import os

def add_line(s):
    new_s = s
    s_count = len(s)
    s_max_count = 100 # 改行する文字列。基本しなくてもいい
    if s_count >= s_max_count:
        if (s_count - s_max_count) >= 3:
            # s_max_count 文字以上、かつ、2行目が3文字以上あれば、改行する
            new_s = s[:s_max_count] + "\n" + s[s_max_count:]
 
    return new_s

def output_whisper_result(path , filename , model):
    
    ## 音声へのパス
    input =path + '/' +filename
 
    output = path + '/' + filename + '.txt'

    if not os.path.exists(output):

        ## 結果を出力と同時に取得
        result = model.transcribe(input, verbose=True, language='ja')

        segments = result['segments']
        subs = []
        for data in segments:
            index = data["id"] + 1
            start = data["start"]
            end = data["end"]
            text = add_line(data["text"])
            sub = Subtitle(index=1, start=timedelta(seconds=timedelta(seconds=start).seconds,
                                                    microseconds=timedelta(seconds=start).microseconds),
                        end=timedelta(seconds=timedelta(seconds=end).seconds,
                                        microseconds=timedelta(seconds=end).microseconds), content=text, proprietary='')
        
            subs.append(sub)

        with open(output, mode='w' ,encoding='utf-8') as file:
        # 文字列をファイルに書き込みます
            file.write(srt.compose(subs))


#path = 'mp3'
#filename = 'sample.mp3'
# モデルの読み込みにもかなり時間が必要だったので、引数で渡す
#model = whisper.load_model("medium")
#output_whisper_result(path,filename,model)


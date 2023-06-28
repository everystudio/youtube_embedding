import whisper
from datetime import timedelta
from srt import Subtitle
import srt
import os
import time
import logging
from dotenv import load_dotenv

load_dotenv()

def setup_logger():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')

    log_directory = os.getenv('LOG_DIRECTORY')
    if not os.path.exists(log_directory) :
       os.makedirs(log_directory)

    handler = logging.FileHandler(f'{log_directory}/whisper_log.txt', encoding='utf-8-sig')
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

setup_logger()

def time_logging(func):
    def wrapper(*args,**kwargs):
        start_time = time.time()
        result = func(*args,**kwargs)
        elapsed_time = (time.time() - start_time)
        minutes,seconds = divmod(elapsed_time,60)
        elapsed_time = round(elapsed_time, 2)  # Round to 2 decimal places

        if(result):
            if 1 < len(args):
                #logging.info(f"{func.__name__} {args[1]} {elapsed_time} seconds.")
                logging.info(f'{func.__name__:<20} {int(minutes):>2}m {seconds:>05.2f}s {args[1]}')
            else:
                logging.info(f"{func.__name__} took {elapsed_time} seconds.")
        return result
    return wrapper

def add_line(s):
    new_s = s
    s_count = len(s)
    s_max_count = 100 # 改行する文字列。基本しなくてもいい
    if s_count >= s_max_count:
        if (s_count - s_max_count) >= 3:
            # s_max_count 文字以上、かつ、2行目が3文字以上あれば、改行する
            new_s = s[:s_max_count] + "\n" + s[s_max_count:]
 
    return new_s

@time_logging
def output_whisper_result(file_path , filename , model):
    ## 音声へのパス
    input =file_path + '/' +filename + '.mp3'
 
    output = file_path + '/' + filename + '.txt'

    print('INPUT:'+input)
    print('OUTPUT:'+output)

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

        return True

    return False


#path = 'mp3'
#filename = 'sample.mp3'
# モデルの読み込みにもかなり時間が必要だったので、引数で渡す
#model = whisper.load_model("medium")
#output_whisper_result(path,filename,model)


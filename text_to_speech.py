from pydub import AudioSegment
import os
import requests

def text_to_speech_segment(text, lang, speaker_id):
    """
    将单个文本片段转换为语音，并返回语音文件的路径和持续时间。

    参数:
        text (str): 要转换的文本片段。
        lang (str): 语音的语言。
        slow (bool): 是否以慢速说话。

    返回:
        tuple: 包含语音文件路径和持续时间的元组。
    """
    # 调用http api将文本转换为语音
    url = "https://yikuni.com/voice/vits?lang={}&id={}&text={}".format(lang, speaker_id, '"' + text + '"')
    response = requests.get(url)
    if response.status_code == 200:
        voice = response.content
    else:
        print("cannot visit url: " + url + ", and response code is :" + str(response.status_code))
        return None

    # 为语音文件生成唯一的文件名
    filename = f"voice-{hash(text)}.mp3"
    # 保存语音文件
    with open(filename, "wb") as f:
        f.write(voice)

    # 使用pydub计算语音文件的持续时间
    audio = AudioSegment.from_file(filename)
    duration = len(audio) / 1000  # 持续时间，以秒为单位

    return filename, duration

def process_text_to_speech(parsed_text, lang, speaker_id):
    """
    处理一个文本集合，将每一段文本转换为语音。

    参数:
        parsed_text (list): 解析后的文本集合, 结构：编号、同一编号下的顺序号、文本。
        lang (str): 语音的语言。
        speaker_id (num): speaker类型。

    返回:
        list: 列表：编号，序号，语音文件名。
    """
    audio_files = []
    # 遍历解析后的文本集合
    for number, seq, text in parsed_text:
        # 对每个文本片段进行语音转换
        filename, duration = text_to_speech_segment(text, lang, speaker_id)
        if filename is None:
            return None
        # 将结果添加到对应编号的列表中
        audio_files.append((number, seq, filename, duration))

    # audio_files最后存了多少条数据
    """
    total_entries = 0
    for numbers, seqs, files, durations in audio_files:
        total_entries += len(files)
    """

    return audio_files

from gtts import gTTS
from pydub import AudioSegment
import os

def text_to_speech_segment(text, lang='zh-cn', slow=False):
    """
    将单个文本片段转换为语音，并返回语音文件的路径和持续时间。

    参数:
        text (str): 要转换的文本片段。
        lang (str): 语音的语言。
        slow (bool): 是否以慢速说话。

    返回:
        tuple: 包含语音文件路径和持续时间的元组。
    """
    # 使用gTTS将文本转换为语音
    tts = gTTS(text=text, lang=lang, slow=slow)
    # 为语音文件生成唯一的文件名
    filename = f"tts-{hash(text)}.mp3"
    # 保存语音文件
    tts.save(filename)

    # 使用pydub计算语音文件的持续时间
    audio = AudioSegment.from_mp3(filename)
    duration = len(audio)  # 持续时间，以毫秒为单位

    return filename, duration

def process_text_to_speech(parsed_text, lang='en', slow=False):
    """
    处理一个文本集合，将每一段文本转换为语音。

    参数:
        parsed_text (dict): 解析后的文本集合。
        lang (str): 语音的语言。
        slow (bool): 是否以慢速说话。

    返回:
        dict: 键为原文本编号，值为包含语音文件路径和持续时间的列表。
    """
    audio_files = {}
    # 遍历解析后的文本集合
    for number, texts in parsed_text.items():
        audio_files[number] = []
        for text in texts:
            # 对每个文本片段进行语音转换
            filename, duration = text_to_speech_segment(text, lang, slow)
            # 将结果添加到对应编号的列表中
            audio_files[number].append((filename, duration))

    return audio_files

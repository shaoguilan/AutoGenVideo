import cv2
from moviepy.editor import concatenate_videoclips, AudioFileClip, VideoFileClip
import os
import codecs
import numpy
from PIL import Image, ImageDraw, ImageFont

#coding=utf-8
#中文乱码处理
def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, numpy.ndarray)):  #判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype(
        "font/simsun.ttc", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontText)
    return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)


def make_video(parsed_text, audio_files, images, output_filename):
    """
    根据提供的文本、音频文件和图片创建视频。

    参数:
    parsed_text - 解析文本列表，格式为 [(编号, 顺序号, 文本), ...]
    audio_files - 音频文件信息列表，格式为 [(编号, 顺序号, 文件路径, 持续时间), ...]
    images - 图片列表，格式为 [(编号, 图片对象), ...]
    output_filename - 最终视频的输出文件名
    """

    temp_clips = []

    for img_number, img in images:
        # 找到与当前图片编号相匹配的音频和文本
        relevant_audios = [af for af in audio_files if af[0] == img_number]
        relevant_texts = [pt for pt in parsed_text if pt[0] == img_number]

        # 获取图片的尺寸信息
        height, width, _ = img.shape

        # 初始化视频写入器
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_video_path = f"temp_video_{img_number}.mp4"
        video_writer = cv2.VideoWriter(temp_video_path, fourcc, 24.0, (width, height))

        # 对于每个相关的音频，创建视频片段
        for (number, seq, text), (_, _, audio_path, duration) in zip(relevant_texts, relevant_audios):
            audio_duration = AudioFileClip(audio_path).duration  # 获取音频持续时间
            frames_needed = int(audio_duration * 24)  # 计算所需帧数，假设每秒24帧

            # 为每一帧添加文本
            for _ in range(frames_needed):
                frame = img.copy()
                text_left = 300 - len(text)
                frame = cv2ImgAddText(frame, text, text_left, 500, (255, 255, 255), 20)
                #cv2.putText(frame, text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                video_writer.write(frame)

        video_writer.release()

        # 将音频添加到视频片段
        clip = VideoFileClip(temp_video_path)
        audio_clip = AudioFileClip(relevant_audios[0][2])  # 使用第一个音频
        final_clip = clip.set_audio(audio_clip)
        temp_clips.append(final_clip)

    # 将所有视频片段拼接成一个完整的视频
    final_video = concatenate_videoclips(temp_clips)
    final_video.write_videofile(output_filename, codec='libx264')

    # 清理临时视频文件
    for clip in temp_clips:
        os.remove(clip.filename)



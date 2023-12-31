from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeAudioClip, TextClip, CompositeVideoClip
import os


def make_video(image_files, audio_files, text_segments, output_file="output.mp4"):
    """
    创建一个视频，包含图像、文本字幕和语音。

    参数:
        image_files (dict): 处理过的图像文件和它们的编号。
        audio_files (dict): 处理过的语音文件、它们的编号和时长。
        text_segments (dict): 每个编号下的文本片段。
        output_file (str): 输出视频文件的名称。
    """
    clips = []
    for number, images in image_files.items():
        for img in images:
            img_clip = ImageSequenceClip([img[0]], durations=[img[1] / 1000])  # 将时长转换为秒
            texts = text_segments.get(number, [])
            audios = audio_files.get(number, [])

            # 添加字幕
            txt_clips = [TextClip(txt, fontsize=24, color='white').set_duration(dur / 1000).set_position("bottom")
                         for txt, dur in zip(texts, [a[1] for a in audios])]
            video = CompositeVideoClip([img_clip] + txt_clips)

            # 添加音频
            audio = CompositeAudioClip([AudioFileClip(a[0]) for a in audios])
            video = video.set_audio(audio)

            clips.append(video)

    # 合并所有片段
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_file)

# 示例用法
# make_video(processed_images, audio_files, parsed_text)

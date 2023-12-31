import cv2
import subprocess
import os
import numpy as np

def create_video_clip(image, audio_info, text, output_clip):
    """
    为单张图片和对应的音频创建视频片段。

    参数:
        image (numpy.ndarray): 处理过的图像数据。
        audio_info (list): 对应音频文件的信息，包括路径和持续时间。
        text (list): 要添加到视频中的文本列表。
        output_clip (str): 输出视频片段的文件名。
    """
    # 将 PIL Image 对象转换为 NumPy 数组
    np_image = np.array(image)

    # 确定视频尺寸
    height, width, _ = np_image.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_clip = cv2.VideoWriter(output_clip, fourcc, 1, (width, height))

    # 音频总时长（秒）
    total_duration = sum(duration for _, duration in audio_info) / 1000

    # 计算需要重复图像的次数（每秒一帧）
    frame_count = int(total_duration)

    # 为视频添加图像帧和文本
    for _ in range(int(total_duration)):
        frame = np.copy(np_image)
        # 将文本添加到图像帧上
        y_offset = 50  # 文本起始位置的垂直偏移量
        for text_line in text:
            cv2.putText(frame, text_line, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            y_offset += 30  # 为下一行文本调整偏移量

        video_clip.write(frame)

    video_clip.release()
    print(f"请检查中间视频文件 {output_clip} 以确认视频内容。")
    input()

    # 添加音频到视频
    print("添加音频到视频")
    audio_cmd = ['ffmpeg', '-i', output_clip]
    for audio_file, _ in audio_info:
        audio_cmd += ['-i', audio_file]
    audio_cmd += ['-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_clip.replace('.mp4', '_audio.mp4')]
    subprocess.run(audio_cmd, shell=True)

    # 删除原始视频片段，保留添加了音频的版本
    os.remove(output_clip)
    os.rename(output_clip.replace('.mp4', '_audio.mp4'), output_clip)

def make_video(processed_images, audio_files, parsed_text, output_file="output1.mp4"):
    """
    根据处理过的图像、音频和文本创建视频。

    参数:
        processed_images (list): 处理过的图像数据列表，包含图像 numpy 数组和编号。
        audio_files (dict): 音频文件信息的字典，键为编号。
        parsed_text (dict): 解析过的文本，键为编号。
        output_file (str): 最终视频的输出文件名。
    """
    temp_clips = []

    # 为每张图片和对应的音频创建视频片段
    for img, number in processed_images:
        output_clip = f"temp_clip_{number}.mp4"
        create_video_clip(img, audio_files[number], parsed_text[number], output_clip)
        temp_clips.append(output_clip)

    # 创建一个包含所有视频片段文件名的文本文件
    with open('concat_list.txt', 'w') as f:
        for clip in temp_clips:
            f.write(f"file '{clip}'\n")

    # 使用 ffmpeg 将所有片段合并成最终的视频
    # concat_cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'concat_list.txt', '-c', 'copy', output_file]
    # subprocess.run(concat_cmd)

    # 创建一个包含所有视频片段文件名的文本文件
    with open('concat_list.txt', 'w') as f:
        for clip in temp_clips:
            f.write(f"file '{clip}'\n")

    # 使用 ffmpeg 将所有片段合并成最终的视频
    print("使用 ffmpeg 将所有片段合并成最终的视频")
    concat_cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'concat_list.txt', '-c', 'copy', output_file]
    subprocess.run(concat_cmd)
    print("使用 ffmpeg 将所有片段合并成最终的视频成功！")
    # 删除临时文件
    os.remove('concat_list.txt')

    # 清理临时文件
    for clip in temp_clips:
        os.remove(clip)

# 示例用法
# make_video(processed_images, audio_files, parsed_text)

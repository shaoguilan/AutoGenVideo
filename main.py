import os
import text_parser
import image_processor
import text_to_speech
# import video_creator

def main():
    # 让用户输入包含图片和文本文件的目录地址
    # directory_path = input("请输入包含图片和文本文件的目录地址: ")
    directory_path = "D:/Documents/私人文件/My Video/抖音视频创作/20231227独库公路"

    # 初始化变量以存储图片路径和文本文件路径
    image_paths = []
    text_file_path = None

    # 遍历用户指定目录中的所有文件
    for filename in os.listdir(directory_path):
        # 如果找到一个文本文件且之前没有找到，保存其路径
        if filename.endswith(".txt") and text_file_path is None:
            text_file_path = os.path.join(directory_path, filename)
        # 如果文件是图像（基于扩展名），添加到图像路径列表
        elif filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_paths.append(os.path.join(directory_path, filename))

    # 打印找到的文本文件和图像文件路径
    # print("找到的文本文件路径:", text_file_path)
    # print("找到的图像文件路径:")
    # for path in image_paths:
    #    print(path)

    # 检查是否找到文本文件，如果没有，通知用户并退出
    if text_file_path is None:
        print("未找到文本文件，请确保目录中包含一个 .txt 文件。")
        return

    # 检查是否找到任何图像文件，如果没有，通知用户并退出
    if not image_paths:
        print("未找到图片文件，请确保目录中至少包含一个图片文件。")
        return

    # 使用 text_parser 模块解析文本文件
    parsed_text = text_parser.parse(text_file_path)

    """
    # 打印解析后的字幸字
    for number, texts in parsed_text.items():
        print(f"编号[{number}]:")
        for text in texts:
            print(f"  - {text}")
    """
    # 使用 image_processor 模块处理每个图像文件
    processed_images = image_processor.process_images(image_paths)
    # print("image processor done")

    # 使用 text_to_speech 模块将解析后的文本转换为语音
    # audio_clip = text_to_speech.convert_to_speech(parsed_text)
    lang = "zh-cn"
    slow = "no"
    audio_clip = text_to_speech.process_text_to_speech(parsed_text, lang, slow)

    # 可以打印或以其他方式使用 audio_files
    """
    for number, files in audio_clip.items():
        print(f"Number {number}:")
        for filename, duration in files:
            print(f"  File: {filename}, Duration: {duration}ms")
    """
    # 使用 video_creator 模块将处理过的图像和语音合成为视频
    # video_creator.create_video(processed_images, audio_clip)

    # 完成视频生成后，通知用户
    # print("视频生成成功！")

# 确保当直接运行此脚本时才执行 main 函数
if __name__ == "__main__":
    main()

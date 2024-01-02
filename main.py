import os
import text_parser
import image_processor
import text_to_speech
import video_creator

def main():
    # 让用户输入包含图片和文本文件的目录地址
    directory_path = input("请输入包含图片和文本文件的目录地址: ")
    directory_path = directory_path.strip()
    # 初始化变量以存储图片路径和文本文件路径
    image_paths = []
    text_file_path = None

    # 遍历用户指定目录中的所有文件
    for filename in os.listdir(directory_path):
        # 如果找到一个文本文件且之前没有找到，保存其路径
        if filename.endswith(".txt") and text_file_path is None:
            text_file_path = os.path.join(directory_path, filename)

    # 检查是否找到文本文件，如果没有，通知用户并退出
    if text_file_path is None:
        print("未找到文本文件，请确保目录中包含一个 .txt 文件。")
        return

    # 使用 text_parser 模块解析文本文件
    parsed_text = text_parser.parse(text_file_path)
    if parsed_text is None:
        print("text parsed failed!")
        return
    # 打印解析后的列表
    # print("打印解析后的列表\n")
    # for item in parsed_text:
    #    print(item)

    # 使用 image_processor 模块处理每个图像文件
    processed_images = image_processor.process_images(directory_path)

    # 使用 text_to_speech 模块将解析后的文本转换为语音
    lang = "zh-cn"
    slow = True

    audio_clip = text_to_speech.process_text_to_speech(parsed_text, lang, slow)

    #使用video_creator模块将处理过的图像和语音合成为视频
    video_creator.make_video(parsed_text, audio_clip, processed_images, output_filename="output_video.mp4")

    # 完成视频生成后，通知用户
    print("视频生成成功!")


# 确保当直接运行此脚本时才执行 main 函数
if __name__ == "__main__":
    main()

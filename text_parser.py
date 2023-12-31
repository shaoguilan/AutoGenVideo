import re

def parse(file_path):
    """
    尝试使用不同的编码读取并解析文本文件。

    参数:
        file_path (str): 文本文件的路径。

    返回:
        dict: 一个字典，键为编号，值为按顺序对应编号的文本列表。
    """
    subtitles = {}
    encodings = ['GBK', 'ISO-8859-1', 'Windows-1252', 'utf-16', 'utf-8']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                subtitles = {}
                for line in file:
                    match = re.match(r'\[(\d+)\](.*)', line)
                    if match:
                        number, text = match.groups()
                        subtitles.setdefault(number, []).append(text.strip())
                return subtitles
        except UnicodeDecodeError:
            print(f"尝试使用 {encoding} 编码读取文件时出错，尝试其他编码。")

    print(f"无法读取文件: {file_path}，请检查文件编码。")
    return None

import re

def parse(file_path):
    """
    尝试使用不同的编码读取并解析文本文件。

    参数:
        file_path (str): 文本文件的路径。

    返回:
        parsed_data: 一个列表：每行的编号，同一编号的顺序号，每行内容。
    """

    parsed_data = []
    current_number = None
    sequence_number = 0
    encoding = "GBK"

    try:
        with open(file_path, 'r', encoding=encoding) as file:
             # 从每行中提取编号和文本
             for line in file:
                # 从每行中提取编号和文本
                if line.startswith('['):
                    number = int(line[line.find('[') + 1: line.find(']')])
                    text = line[line.find(']') + 1:].strip()

                    # 检查编号是否改变
                    if number != current_number:
                        current_number = number
                        sequence_number = 1
                    else:
                        sequence_number += 1

                    # 将提取的数据添加到列表
                    parsed_data.append((number, sequence_number, text))
    except UnicodeDecodeError:
        print(f"尝试使用 {encoding} 编码读取文件时出错，尝试其他编码。")
        return None

    return parsed_data

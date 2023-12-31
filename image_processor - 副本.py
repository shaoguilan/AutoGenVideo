import os
from PIL import Image
import re

def load_image(image_path):
    """
    加载图像文件，并从文件名中提取编号。

    参数:
        image_path (str): 图像文件的路径。

    返回:
        tuple: 包含图像对象和图像编号的元组。
    """
    try:
        # 从文件名中提取编号
        filename = os.path.basename(image_path)
        match = re.match(r'\[(\d+)\]', filename)
        if not match:
            print(f"文件名不符合预期格式 [编号]: {filename}")
            return None, None

        number = match.group(1)
        image = Image.open(image_path)

        return image, number
    except IOError:
        print(f"无法加载图像: {image_path}")
        return None, None

def resize_image(image, size):
    """
    调整图像大小。

    参数:
        image (Image): 要调整大小的图像对象。
        size (tuple): 新的大小，格式为 (宽度, 高度)。

    返回:
        Image: 调整大小后的图像对象。
    """
    resized_image = image.resize(size, Image.LANCZOS)
    return resized_image

# 示例用法
# image, number = load_image('path/to/your/[1].jpg')
# if image is not None:
#     resized_image = resize_image(image, (800, 600))

def process_images(image_paths, size=(800, 600)):
    """
    处理一系列图像文件。

    参数:
        image_paths (list): 图像文件路径列表。
        size (tuple): 图像调整后的大小，默认为 (800, 600)。

    返回:
        list: 包含元组的列表，每个元组包含处理后的图像和编号。
    """
    processed_images = []
    for image_path in image_paths:
        image, number = load_image(image_path)
        if image is not None:
            resized_image = resize_image(image, size)
            processed_images.append((resized_image, number))

    return processed_images

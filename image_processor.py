import cv2
import os
"""
处理一系列图像文件。

参数:
    image_paths (list): 图像文件路径列表。
    size (tuple): 图像调整后的大小，默认为 (800, 600)。

返回:
    list: 包含元组的列表，每个元组包含处理后的图像和编号。
"""

def resize_image(image, target_size=(800, 600)):
    """
    调整图像大小。

    参数:
       image (Image): 要调整大小的图像对象。
       size (tuple): 新的大小，格式为 (宽度, 高度)。

      返回:
      Image: 调整大小后的图像对象。
    """
    resized_image = cv2.resize(image, target_size)
    return resized_image

    # 示例用法
    # if image is not None:
    #     resized_image = resize_image(image, (800, 600))

def process_images(folder_path, size=(800, 600)):
    file_name_list = os.listdir(folder_path)
    image_file_name_list = []

    for file_name in file_name_list:
        # 如果文件是图像（基于扩展名），添加到图像路径列表
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_file_name_list.append(file_name)

    frames = []  # 创建一个列表来存储图片数据和编号
    for image_file_name in image_file_name_list:
        img = cv2.imread(folder_path + "/" + image_file_name)
        if img is not None:
            img = resize_image(img, size)  # 调整图片大小
            image_number = int(image_file_name.split('.')[0])  # 提取编号
            frames.append((image_number, img))  # 将编号和图片作为元组添加到列表中
            # 保存图片到临时文件夹
            #temp_folder_path = folder_path + "/" + "temp_photo"
            #temp_image_path = os.path.join(temp_folder_path, f"temp_{image_number}.jpg")
            #cv2.imwrite(temp_image_path, img)
            #print("img number is: ")
            #print(image_number)

    if frames is None:
        print("cannot find image file")

    return frames
    # 现在，frames字典包含了所有的图片数据，键是图片编号
import unittest
import os
import cv2
from text_parser import parse
from image_processor import process_images

# 导入其他必要的模块

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        # 设置测试环境，例如创建测试数据
        self.folder = "test"   #测试文件所在目录
        self.test_text_file = "test/test_data.txt"  # 测试文本文件
        self.test_audio_output = "test/test_audio"  # 测试音频输出目录
        self.test_video_output = "test/test_video.mp4"  # 测试视频输出文件

        # 假设的文本解析测试结果
        self.expected_parsed_text = [(1, 1, "旅游时被临时取消计划的景点"), (1, 2, "能得到赔偿吗？"), (2, 1, "小明参加某旅行社的")]
        # 假设的图片处理结果
        self.expected_image_process = [(1, cv2.imread("test\\temp\\test_1.jpg")), (2, cv2.imread("test\\temp\\test_1.jpg"))]

    def test_text_parsing(self):
        # 测试文本解析功能
        parsed_text = parse(self.test_text_file)
        self.assertEqual(parsed_text, self.expected_parsed_text)
    def test_image_processing(self):
        # 测试图片处理功能
        images = process_images(self.folder, size=(800, 600))
        for img_number, img in images:
            temp_image_path = os.path.join(self.folder, f"temp_{img_number}.jpg")
            cv2.imwrite(temp_image_path, img)
        #self.assertEqual(images, self.expected_image_process)
"""
    def test_video_creation(self):
        # 测试视频创建功能
        # 需要预先准备图像和音频文件
        images = [(1, "image1.png"), (2, "image2.png")]
        audio_files = [(1, 1, "audio_1_1.mp3", 5000), (1, 2, "audio_1_2.mp3", 3000)]

        create_video_with_text_and_audio(self.expected_parsed_text, audio_files, images, self.test_video_output)

        # 检查视频文件是否创建
        self.assertTrue(os.path.exists(self.test_video_output))

    def tearDown(self):
        # 清理测试环境，如删除生成的文件
        if os.path.exists(self.test_video_output):
            os.remove(self.test_video_output)
        # 清理其他生成的文件
"""
if __name__ == '__main__':
    unittest.main()

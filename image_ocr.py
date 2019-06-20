#coding:utf-8
# 参考教程：https://github.com/madmaze/pytesseract
# 阈值化处理：https://www.cnblogs.com/ssyfj/p/9272615.html

# 指定图像路径、所选语言
# 输出检测文字
#
# 可选语言：
# eng
# osd
# chi_tra
# equ
# chi_sim

import cv2
import  os
from PIL import Image
# from pytesseract import image_to_string
import pytesseract


#---------------------------------------------------------
# get image abs path
#---------------------------------------------------------

## get abspath of each image in a folder
def get_image_path_from_file(file_path):
    sub_path = os.listdir(file_path)  #  Return a list containing the names of the files in the directory.
    image_abs_path = []
    anno_abs_path = []
    for dir in sub_path:
        child = os.path.join(file_path, dir)
        if os.path.isfile(child) and child.endswith("png"):  # an image
            image_abs_path.append(os.path.abspath(child))  # get abspath of each image
    return image_abs_path



if __name__ == "__main__":
    print(pytesseract.get_tesseract_version())
    images = get_image_path_from_file("./")
    for index, image in enumerate(images):
        img = cv2.imread(image, 0)  # 灰度图
        threshold, binary = cv2.threshold(img,100 ,255, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 大津法、自动计算阈值
        # threshold, binary = cv2.threshold(img, 0, 255, cv2.THRESH_TOZERO)  # 自己指定阈值

        # # 展示阈值化结果
        # cv2.imshow("binary", binary)  # 显示二值化图像
        # cv2.waitKey(100)
        print(index, pytesseract.image_to_string(binary,lang='eng'))


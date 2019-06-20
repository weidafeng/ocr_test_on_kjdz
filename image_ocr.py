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
import json
from PIL import Image
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

#---------------------------------------------------------
# get text lable from annotations.txt
#---------------------------------------------------------

# KJDZ0005 检测字段
test_field_0005 = ["IssueDate", "TotalAmount", "InvoiceNO", "InvoiceCode"]
# KJDZ0004 检测字段
test_field_0004 = ["IssueDate", "TotalAmountCap", "InvoiceNO", "InvoiceCode"]

# 输入：annotation.txt、 test_field
# 输出： 真实label列表
def get_anno_label(anno_file, test_field = test_field_0005):
    words = []
    with open(anno_file, 'r') as f:
        data = json.load(f)
        contents = data['templateFields']
        for i in range(len(contents)):  # 处理同一张图片下的所有标注字段
            # 若 label 标注里不含['content']字段
            try:  # title 字段不是每个都有,比如/KJDZ0005/annotations/1527143843_38_102.txt
                content = contents[i]['content']
            except:
                # print(str(an_file))
                pass
            templateFieldNo = contents[i]['templateFieldNo']  # label
            if templateFieldNo in test_field:
                word = content["word"]
                words.append(word)
    return words


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


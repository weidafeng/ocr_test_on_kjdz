# 使用opencv截取指定部位图像
# 输入：
#   包含图像、annotation的路径
#
# 输出：
#   保存截取的图像


import os
import cv2
import json

#---------------------------------------------------------
# get image abs path
#---------------------------------------------------------

## get abspath of each image in a folder
def get_image_path_from_file(file_path):
    sub_path = os.listdir(file_path)  #    Return a list containing the names of the files in the directory.
    image_abs_path = []
    anno_abs_path = []
    for dir in sub_path:
        child = os.path.join(file_path, dir)
        if os.path.isfile(child) and child.endswith(("jpg","png","jpeg")):  # an image
            image_abs_path.append(os.path.abspath(child))  # get abspath of each image
        elif os.path.isfile(child) and child.endswith("txt"):  # an annotation txt file
            anno_abs_path.append(os.path.abspath(child))  # get abspath of each annotation
    return image_abs_path, anno_abs_path

#---------------------------------------------------------
# segmentation
#---------------------------------------------------------

## using opencv to segment certain areas of an image
#  输入：
#       image_path
#       bounding_box, 格式：[left, top, width, height]
#       index: 用于保存截图图像时命名

#  输出：
#       保存截取的图片
def segment_an_image(image_path, bounding_box, index):
    image = cv2.imread(image_path)
    shape = image.shape  # (height, width, channel)->(50, 220, 3)
    height, width = shape[0], shape[1]
    x_begin, x_end, y_begin, y_end =  bounding_box[1], bounding_box[1] + bounding_box[3], bounding_box[0], bounding_box[0]+ bounding_box[2]
    cv2.imwrite(image_path+"_{}.png".format(str(index)), image[x_begin: x_end, y_begin: y_end])# 高度、宽度各截一半
    return [x_begin, x_end, y_begin, y_end]

#---------------------------------------------------------
# bounding-box
#---------------------------------------------------------

# 获取 bounding-box， segmentation 信息
def get_info(content):
    # 输入content是dict格式，
    # 获得bounding-box的坐标和内容, 以及segmentation信息：有序的四个点的坐标（bounding-box坐标）
    height = int(content['height'])
    width = int(content['width'])
    left = int(content['left'])
    top = int(content['top'])
    # word = content['word'] # 不考虑
    segmentation = [left, top, left + width, top, left + width, top + height, left, top + height] # 浮点形式
    # return [left, top, width, height], [segmentation] # bounding-box信息， coco格式： x,y,w,h）；segmentation为[[1,2,3,4,5,6，7,8]]格式
    return [left, top, width, height]

def get_bounding_box(anno_file):
    bounding_boxs = []
    with open(anno_file, 'r') as f:
        data = json.load(f)
        contents = data['templateFields']

        for i in range(len(contents)):  # 处理同一张图片下的所有标注字段
            # 若 label 标注里不含['content']字段
            try: # title 字段不是每个都有,比如/KJDZ0005/annotations/1527143843_38_102.txt
                content = contents[i]['content']
            except:
                # print(str(an_file))
                pass
            # templateFieldNo = contents[i]['templateFieldNo']  # label
            # templateFieldName = contents[i]['templateFieldName'] # label-name，不考虑
            bounding_box = get_info(content) # [left,top, width, height] # bounding-box信息， coco格式： x,y,w,h）
            bounding_boxs.append(bounding_box)
            # print(bounding_box)
    return bounding_boxs

if __name__=="__main__":
    images, annotations = get_image_path_from_file("./")
    # print(images,annotations)

    for image, anno in zip(images, annotations):
        print(image, anno)

        bounding_boxs = get_bounding_box(anno)
        # print(bounding_boxs)
        for index, bbox in enumerate(bounding_boxs):
            segment_an_image(image, bbox, index)


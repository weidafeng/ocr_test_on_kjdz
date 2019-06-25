# 项目说明  
本项目用于测试[tesseract-OCR](https://github.com/tesseract-ocr/tesseract) 在 KJDZ数据集上的准确率。  
## KJDZ0005 检测字段  
```
test_field_0005 = ["IssueDate", "TotalAmount", "InvoiceNO", "InvoiceCode"]
```  
## KJDZ0004 检测字段  
```  
test_field_0004 = ["IssueDate", "TotalAmountCap", "InvoiceNO", "InvoiceCode"]
```    

# 使用说明
1. 将KJDZ数据（jpg图片、txt注释）放入项目根目录
2. 运行[image_segmentation.py](image_segmentation.py)，得到待识别的区域图像  
3. 运行[image_ocr.py](image_ocr.py)，得到每张图像的识别准确率

# 参考
1. https://github.com/madmaze/pytesseract
2. https://github.com/tesseract-ocr/tesseract
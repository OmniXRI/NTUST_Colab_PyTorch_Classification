# -*- coding: utf-8 -*-
"""20201218_PyTorch_Classification_Pretrained_Inference.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xMdgrr9w-oaDNFrIQQeBe5fNDnTo5pe8

# **Colab + PyTorch + PIL + resnet50預訓練模型進行影像分類推論**

歐尼克斯實境互動工 作室 OmniXRI Jack 2020.12.18整理製作

本範例主要使用PyTorch自帶已訓練的模型進行推論，輸出為ImageNet 1000分類。

目前是使用resnet50進行測試，可依需求自行修改。
"""

import torch # 載入PyTorch相關函式庫
import torch.nn.functional as F # 載入PyTorch NN 函數相關函式庫
import torchvision.models as models # 載入PyTorch 模型相關函式庫
import torchvision.transforms as trns # 載入PyTorch 轉換相關函式庫
from PIL import Image # 載人PIL 影像處理相關函式庫

# 定義執行影像分類函式
def run_image_classification(model, image_path, transforms, classes, topk=5):
    # 讀取原始影像並轉換成RGB格式
    image = Image.open(image_path).convert("RGB")
    # 建立影像張量
    image_tensor = transforms(image)
    # 列出影像張量大小 [C,W,H] 通道數，寬，高
    print(f"\n\nImage size after transformation: {image_tensor.size()}")
    # 增加一維（批量）資料
    image_tensor = image_tensor.unsqueeze(0)
    # 列出變更後影像張量大小 [B,C,H,W] 批次量，通道數，寬，高
    print(f"Image size after unsqueezing: {image_tensor.size()}")
    # 指定模型輸出類別
    output = model(image_tensor)
    # 列出模型輸出尺寸
    print(f"Output size: {output.size()}")
    # 壓縮（刪減批量）一維資料
    output = output.squeeze()
    # 列出模型壓縮後尺寸
    print(f"Output size after squeezing: {output.size()}")
    # 輸出結果進行遞減排序
    _, indices = torch.sort(output, descending=True)
    # 將輸出調整為Softmax結果
    probs = F.softmax(output, dim=-1)
    # 列出前五推論結果
    print("\n\nInference results:")
    # 列出標籤編號(1~1000)及說明文字 
    for index in indices[:topk]:
        print(f"Label {index}: {classes[index]} ({probs[index].item():.2f})")
    # 函式回返
    return

# 下載測試用影像
!wget https://raw.githubusercontent.com/OmniXRI/NTUST_Colab_PyTorch_Classification/main/dog.jpg -N
# 下載標籤文字說明檔
!wget https://raw.githubusercontent.com/OmniXRI/NTUST_Colab_PyTorch_Classification/main/imagenet_classes.txt -N
# 檢查是否下載到虛擬機上
!ls

# 列出PyTorch支援的模型種類
print(dir(models))

# 載入1000類影像標籤說明檔並建立清單
with open("imagenet_classes.txt") as f:
    classes = [line.strip() for line in f.readlines()]

# 定義影像轉換格式
transforms = trns.Compose(
    [trns.Resize((224, 224)), # 強制調整輸入影像尺寸至224x224
     trns.ToTensor(), 
     trns.Normalize( # 將影像數值從[0~255]正規化至[0.0~1.0]
        mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225])
    ])

# 載入resnet50已預訓練模型 
trained_model = models.resnet50(pretrained=True) # 可自行切換成其它不同模型

# 設定模型為評估模式以便進行推論
trained_model.eval()

# 檢查待分類影像
img = Image.open('dog.jpg')
img

# 載入指定影像並執行指定影像分類模型推論
# 並列出前五項推論結果標籤編號、文字說明及可信度（機率0.00~1.00)
with torch.no_grad():
    run_image_classification(
        trained_model, 'dog.jpg', transforms, classes)
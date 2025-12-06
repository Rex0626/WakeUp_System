# 🎓 同學！起床囉～ (Student Monitor System)

> **基於 NVIDIA Jetson Nano 與 YOLOv8 的課堂瞌睡偵測系統**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/Model-YOLOv8_Pose-green?logo=ultralytics)](https://github.com/ultralytics/ultralytics)
[![Platform](https://img.shields.io/badge/Platform-Jetson_Nano-76B900?logo=nvidia&logoColor=white)](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)

## 📖 專案簡介 (Introduction)
本專案是針對大學課堂場景設計的**即時精神監控系統**。利用電腦視覺技術 (Computer Vision)，透過攝影機即時分析學生的坐姿與骨架資訊。

當系統偵測到學生出現「趴桌」或「過度低頭」等瞌睡特徵時，會自動在畫面中標記並給予警示。本系統旨在透過邊緣運算 (Edge AI) 技術，協助解決課堂上精神不濟的問題，並提供非接觸式的狀態分析。

![System Demo](https://via.placeholder.com/800x400?text=Place+Your+Demo+Image+Here)

## ✨ 核心功能 (Features)

* 🚀 **即時偵測 (Real-time Detection)**：使用輕量化的 **YOLOv8-Pose** 模型，即時抓取畫面中人物的骨架關鍵點 (Keypoints)。
* 👥 **多目標追蹤 (Multi-Target Tracking)**：支援同時監控畫面中的多位學生，並給予獨立 ID 進行持續追蹤。
* 💤 **狀態判斷 (State Classification)**：自動邏輯分析，區分 **「清醒 (Awake)」** 與 **「睡著 (Sleeping)」** 狀態。
* ⚠️ **視覺化警示 (Visual Alert)**：當判定為睡著時，畫面目標框會轉為紅色，並顯示持續時間計時。

## ⚙️ 系統流程 (System Flow)

本系統採取「由下而上 (Bottom-Up)」的分析流程：

1.  **影像輸入**：透過 Webcam 擷取即時視訊串流。
2.  **AI 推論**：利用 YOLOv8 進行人體偵測，輸出骨架座標 (Keypoints)。
3.  **幾何運算**：計算關鍵點（如鼻子與肩膀）之間的相對距離與角度。
4.  **邏輯判斷**：將運算結果與設定的閥值 (Threshold) 比較。
5.  **結果輸出**：使用 OpenCV 在螢幕上繪製骨架連線與狀態標籤。

## 🧮 演算法原理 (Algorithm)

為了避免因學生距離鏡頭遠近不同而產生誤差，我們不使用絕對像素距離，而是設計了 **「正規化趴桌指數 (Normalized Slouching Ratio)」** 來判斷睡意。

### 判定公式
$$
\text{Ratio} = \frac{\text{肩膀中心高度} (y_{shoulder}) - \text{鼻子高度} (y_{nose})}{\text{肩膀寬度} (w_{shoulder})}
$$

### 閥值標準
* 🟢 **Ratio > 0.3 (正常)**：鼻子位置顯著高於肩膀，判定為 **清醒**。
* 🔴 **Ratio < 0.3 (睡著)**：鼻子高度接近或低於肩膀（趴桌特徵），判定為 **睡著**。

## 🛠️ 硬體與環境要求 (Requirements)

### 硬體設備 (Hardware)
| 設備 | 建議規格 | 備註 |
| :--- | :--- | :--- |
| **開發板** | NVIDIA Jetson Nano | 需安裝 JetPack 4.6.1 |
| **攝影機** | USB Webcam | 羅技 C270 或同級產品 |
| **電源** | 5V/4A DC 電源 | 確保推論時電壓穩定 |
| **其他** | 螢幕、鍵盤滑鼠、散熱風扇 | |

### 軟體環境 (Software)
* Python 3.8+
* Ultralytics (YOLOv8)
* OpenCV-Python
* NumPy
* Torch / Torchvision (配合 JetPack 版本)

## 📂 檔案架構 (File Structure)

```text
WakeUp_System/
├── models/
│   └── yolov8n-pose.pt       # [模型] 預訓練或微調後的權重檔
├── modules/                  # [核心模組]
│   ├── detector.py           # AI 偵測與追蹤邏輯
│   ├── pose_estimator.py     # 姿勢幾何運算
│   └── alert.py              # 畫面繪製與警示處理
├── config.py                 # [設定檔] 靈敏度閥值與參數設定
├── main.py                   # [主程式] 系統啟動入口
└── requirements.txt          # [清單] 相依套件列表
```

## 🚀 快速開始 (Quick Start)

1. 複製專案
```
Bash
git clone [https://github.com/YourUsername/WakeUp_System.git](https://github.com/YourUsername/WakeUp_System.git)
cd WakeUp_System
```
2. 安裝相依套件
建議使用虛擬環境 (Virtualenv/Conda)：
```
Bash
pip install -r requirements.txt
(注意：Jetson Nano 上的 PyTorch 安裝建議參考 NVIDIA 官方論壇指引)
```

3. 執行系統
確保 Webcam 已連接，然後執行：
```
Bash

python main.py
```

## 📝 授權與致謝 (License)
本專案採用 MIT License。
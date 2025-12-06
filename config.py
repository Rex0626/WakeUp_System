# --- 系統設定 ---
# 攝影機 ID (通常 0 是預設 webcam)
WEBCAM_ID = 0 

# YOLO 模型路徑
MODEL_PATH = 'yolov8n-pose.pt'

# --- 判斷邏輯參數 ---
# 趴桌閥值 (數值越小代表頭越低)
# 建議：先設 0.3，如果太容易誤判睡著就調成 0.25
SLEEP_THRESHOLD = 0.3

# --- 顯示設定 ---
# 視窗標題
WINDOW_NAME = "Classmate! Wake Up~ System"
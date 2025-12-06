from ultralytics import YOLO

class PersonDetector:
    def __init__(self, model_path):
        print(f"正在載入模型：{model_path} ...")
        self.model = YOLO(model_path)
    
    def detect_and_track(self, frame):
        """
        執行 YOLO 追蹤
        :return: results 物件
        """
        # persist=True 是追蹤 ID 保持連貫的關鍵
        # verbose=False 讓終端機不要一直噴 log
        results = self.model.track(frame, persist=True, verbose=False)
        return results[0]
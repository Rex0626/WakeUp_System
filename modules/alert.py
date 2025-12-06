import cv2

class AlertSystem:
    def __init__(self):
        # 定義顏色 (BGR)
        self.COLOR_OK = (0, 255, 0)      # 綠色
        self.COLOR_SLEEP = (0, 0, 255)   # 紅色
        self.COLOR_TEXT = (255, 255, 255) # 白色

    def draw_status(self, frame, box, track_id, is_sleeping, ratio, duration=0):
        """
        在畫面上繪製狀態框和文字
        """
        x1, y1, x2, y2 = map(int, box)
        
        # 決定顏色與文字
        if is_sleeping:
            color = self.COLOR_SLEEP
            status_text = f"SLEEPING! ({duration:.1f}s)"
        else:
            color = self.COLOR_OK
            status_text = f"Awake ({ratio:.2f})"

        # 1. 畫外框 (Bounding Box)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # 2. 畫 ID 標籤背景
        cv2.rectangle(frame, (x1, y1 - 30), (x1 + 200, y1), color, -1)

        # 3. 寫字
        label = f"ID:{track_id} | {status_text}"
        cv2.putText(frame, label, (x1 + 5, y1 - 8), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.COLOR_TEXT, 2)

    def draw_skeleton(self, frame, keypoints):
        """
        簡單繪製骨架連接線 (視覺輔助)
        """
        # 連接鼻子與肩膀 (索引 0 -> 5, 0 -> 6)
        nose = (int(keypoints[0][0]), int(keypoints[0][1]))
        l_shoulder = (int(keypoints[5][0]), int(keypoints[5][1]))
        r_shoulder = (int(keypoints[6][0]), int(keypoints[6][1]))

        if keypoints[0][2] > 0.5:
            if keypoints[5][2] > 0.5:
                cv2.line(frame, nose, l_shoulder, (255, 255, 0), 2)
            if keypoints[6][2] > 0.5:
                cv2.line(frame, nose, r_shoulder, (255, 255, 0), 2)
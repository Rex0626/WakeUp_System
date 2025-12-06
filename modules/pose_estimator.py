import numpy as np

class PoseEstimator:
    def __init__(self, threshold):
        """
        初始化姿勢估計器
        :param threshold: 判定睡著的比例閥值 (config 中設定)
        """
        self.threshold = threshold

    def calculate_distance(self, p1, p2):
        """計算兩點歐式距離"""
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def analyze_pose(self, keypoints):
        """
        分析單個人的骨架數據
        :param keypoints: YOLO keypoints data (numpy array)
        :return: (is_sleeping: bool, ratio: float)
        """
        # YOLO Keypoints 索引: 0:鼻子, 5:左肩, 6:右肩
        nose = keypoints[0]
        l_shoulder = keypoints[5]
        r_shoulder = keypoints[6]

        # 1. 檢查信心度 (若遮蔽太嚴重則不判斷)
        if nose[2] < 0.5 or l_shoulder[2] < 0.5 or r_shoulder[2] < 0.5:
            return False, 0.0

        # 2. 計算肩膀寬度 (當作比例尺，避免遠近影響判斷)
        shoulder_width = self.calculate_distance(l_shoulder[:2], r_shoulder[:2])
        if shoulder_width == 0: return False, 0.0

        # 3. 計算肩膀中心高度 (Y座標)
        shoulder_mid_y = (l_shoulder[1] + r_shoulder[1]) / 2

        # 4. 計算「趴下程度」
        # 邏輯：鼻子Y座標 與 肩膀Y座標 的差距。
        # 正常坐姿：鼻子在肩膀上方很多 (差距大)
        # 趴下/睡著：鼻子接近肩膀甚至低於肩膀 (差距小或負值)
        # 注意：影像座標 Y 向下為正
        nose_shoulder_diff = shoulder_mid_y - nose[1]

        # 正規化比率
        ratio = nose_shoulder_diff / shoulder_width

        # 5. 判定
        # 如果比率小於閥值，判定為睡著
        is_sleeping = ratio < self.threshold

        return is_sleeping, ratio
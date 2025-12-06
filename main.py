import cv2
import time
import config  # 匯入設定檔
from modules.detector import PersonDetector
from modules.pose_estimator import PoseEstimator
from modules.alert import AlertSystem

def main():
    # 1. 初始化各個模組
    detector = PersonDetector(config.MODEL_PATH)
    pose_estimator = PoseEstimator(config.SLEEP_THRESHOLD)
    alert_system = AlertSystem()

    # 2. 開啟攝影機
    cap = cv2.VideoCapture(config.WEBCAM_ID)
    
    # 記錄每個 ID 開始睡覺的時間點 {id: start_time}
    sleep_timers = {}

    print("系統啟動完成！按 'q' 離開...")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("無法讀取攝影機影像")
            break

        # 3. AI 偵測與追蹤
        results = detector.detect_and_track(frame)

        # 確保有偵測到人
        if results.boxes.id is not None:
            # 轉成 numpy 格式方便處理
            boxes = results.boxes.xyxy.cpu().numpy()
            track_ids = results.boxes.id.int().cpu().tolist()
            keypoints = results.keypoints.data.cpu().numpy()

            # 4. 針對每個人進行分析
            for box, track_id, kpt in zip(boxes, track_ids, keypoints):
                
                # 姿勢分析
                is_sleeping, ratio = pose_estimator.analyze_pose(kpt)
                
                # 邏輯：處理睡覺計時器
                duration = 0
                if is_sleeping:
                    if track_id not in sleep_timers:
                        sleep_timers[track_id] = time.time()
                    duration = time.time() - sleep_timers[track_id]
                else:
                    # 如果醒了，重置該 ID 的計時器
                    if track_id in sleep_timers:
                        del sleep_timers[track_id]

                # 5. 繪製結果
                alert_system.draw_status(frame, box, track_id, is_sleeping, ratio, duration)
                alert_system.draw_skeleton(frame, kpt)

        # 顯示畫面
        cv2.imshow(config.WINDOW_NAME, frame)

        # 按 'q' 退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
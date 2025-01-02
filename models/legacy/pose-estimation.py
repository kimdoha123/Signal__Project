from IPython.core.interactiveshell import InteractiveShell
import cv2
import time
from pathlib import Path
from collections import defaultdict
from ultralytics import YOLO
from ultralytics.engine.results import Results
import serial

InteractiveShell.ast_node_interactivity = "all"

ml_dir: Path = Path.cwd() / "ml"
ml_dir.mkdir(parents=True, exist_ok=True)

ai_models_dir: Path = ml_dir / "models"
ai_models_dir.mkdir(parents=True, exist_ok=True)

# Load the YOLO11 model
yolo_pose_file_stem = "yolo11m-pose.pt"
yolo_pose_model = YOLO(f"{ai_models_dir / yolo_pose_file_stem}")


arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)

last_command_time = 0
command_interval = 0.5  # 명령을 보내는 최소 간격(0.5초)

def send_command_to_arduino(command):
    global last_command_time
    current_time = time.time()
    
    # 마지막 명령 후 일정 시간이 지나야 새로운 명령을 전송
    if current_time - last_command_time >= command_interval:
        arduino.write(bytes(command + '\n', 'utf-8'))
        last_command_time = current_time

# Open the video file
cap = cv2.VideoCapture(0)

def detect_gesture(keypoints):
    if not keypoints or len(keypoints) < 10:
        return "No Signal"

    right_hand = keypoints[9]  # 오른손 좌표
    left_hand = keypoints[10]  # 왼손 좌표
    right_shoulder = keypoints[5]  # 오른쪽 어깨 좌표
    left_shoulder = keypoints[6]  # 왼쪽 어깨 좌표
    right_elbow = keypoints[7]  # 오른쪽 팔꿈치 좌표
    left_elbow = keypoints[8]  # 왼쪽 팔꿈치 좌표
    right_ear = keypoints[3]  # 오른쪽 귀 좌표
    left_ear = keypoints[4]  # 왼쪽 귀 좌표

    # RIGHT: 오른손이 어깨보다 오른쪽에 있고, 어깨-팔꿈치-손이 수평을 유지
    if right_hand[0] > right_shoulder[0] + 50 and abs(right_hand[1] - right_elbow[1]) < 30 and abs(right_elbow[1] - right_shoulder[1]) < 30:
        send_command_to_arduino("RIGHT\n")
        return "RIGHT"
    # LEFT: 왼손이 어깨보다 왼쪽에 있고, 어깨-팔꿈치-손이 수평을 유지
    elif left_hand[0] < left_shoulder[0] - 50 and abs(left_hand[1] - left_elbow[1]) < 30 and abs(left_elbow[1] - left_shoulder[1]) < 30:
        send_command_to_arduino("LEFT\n")
        return "LEFT"
    # SLOW: 오른손과 왼손이 각각 귀 근처에 있고, 손과 팔꿈치의 x좌표가 일치
    elif (abs(right_hand[0] - right_ear[0]) < 80 and abs(right_hand[0] - right_elbow[0]) < 30 and abs(right_elbow[1] - right_shoulder[1]) < 30) and \
        (abs(left_hand[0] - left_ear[0]) < 80 and abs(left_hand[0] - left_elbow[0]) < 30 and abs(left_elbow[1] - left_shoulder[1]) < 30):
        send_command_to_arduino("SLOW\n")
        return "SLOW"
    # STOP: 오른손이 오른쪽 귀 근처에 있고, 손과 팔꿈치의 x좌표가 일치
    elif abs(right_hand[0] - right_ear[0]) < 80 and abs(right_hand[0] - right_elbow[0]) < 30 and abs(right_elbow[1] - right_shoulder[1]) < 30:
        send_command_to_arduino("STOP\n")
        return "STOP"
    # STOP: 왼손이 왼쪽 귀 근처에 있고, 손과 팔꿈치의 x좌표가 일치
    elif abs(left_hand[0] - left_ear[0]) < 80 and abs(left_hand[0] - left_elbow[0]) < 30 and abs(left_elbow[1] - left_shoulder[1]) < 30:
        send_command_to_arduino("STOP\n")
        return "STOP"
    else:
        send_command_to_arduino("GO\n")
        return "No Signal"



# Loop through the video frames
try:
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            # Run YOLO11 tracking on the frame, persisting tracks between frames
            results: list[Results] = yolo_pose_model.track(
                frame, persist=True, verbose=False
            )

            # 사람이 감지되었을 때만 실행
            if results and results[0].keypoints is not None:
                keypoints = results[0].keypoints.data.tolist()
                if len(keypoints) > 0:
                    signal = detect_gesture(keypoints[0])  # 첫 번째 사람의 keypoints 사용
                    print(f"Detected Signal: {signal}")

            # Visualize the results on the frame
            annotated_frame = results[0].plot() if results else frame
            cv2.imshow("YOLO11 Tracking", annotated_frame)
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Break the loop if the end of the video is reached
            break
finally:
    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()

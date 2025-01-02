# %%
from IPython.core.interactiveshell import InteractiveShell

import cv2
import serial
import time
import threading

from ultralytics import YOLO

InteractiveShell.ast_node_interactivity = "all"
model = YOLO("best.pt").to("cuda")
# Arduino 연결
arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=0.1)

# %%
last_command_time = 0
command_interval = 0.5  # 명령을 보내는 최소 간격(0.5초)
command_queue = []


# 시리얼 통신을 비동기적으로 처리하는 스레드 함수
def serial_communication_thread():
    while True:
        if command_queue:
            command = command_queue.pop(0)
            arduino.write(bytes(command, "utf-8"))
        time.sleep(0.1)


# 스레드 시작
serial_thread = threading.Thread(target=serial_communication_thread, daemon=True)
serial_thread.start()


def send_command_to_arduino(command):
    global last_command_time
    current_time = time.time()

    # 마지막 명령 후 일정 시간이 지나야 새로운 명령을 전송
    if current_time - last_command_time >= command_interval:
        command_queue.append(command)
        last_command_time = current_time


# 클래스 ID에 따른 라벨 정의
class_labels = {0: "GO", 1: "RIGHT", 2: "LEFT", 3: "STOP", 4: "SLOW"}

# 웹캠 시작
cap = cv2.VideoCapture(
    0
)  # 0은 기본 웹캠, 다른 장치를 사용 중이면 해당 장치 번호로 변경
try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("웹캠에서 영상을 읽을 수 없습니다.")
            break

        # 프레임에서 포즈 예측 수행
        results = model.predict(source=frame, save=False)

        detected = False  # 감지 여부 확인
        # 결과에서 클래스 ID에 따라 출력
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls)  # 클래스 ID
                    if class_id in class_labels:
                        detected = True
                        send_command_to_arduino(class_labels[class_id] + "\n")
                        print(class_labels[class_id])

        # 감지되지 않은 경우 기본값으로 'GO' 전송
        if not detected:
            send_command_to_arduino(class_labels[0] + "\n")
finally:
    # 웹캠 및 창 닫기
    cap.release()
    cv2.destroyAllWindows()

# %%

import cv2
from ultralytics import YOLO
import serial
import time
import threading


# 클래스 라벨 정의
class_labels = {0: "GO", 1: "LEFT", 2: "RIGHT", 3: "STOP", 4: "SLOW"}

# 모델 로드
model = YOLO("best.engine", task="pose")

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)

last_command_time = 0
command_interval = 0.1
command_queue = []

# 시리얼 통신을 비동기적으로 처리하는 스레드 함수
def serial_communication_thread():
    while True:
        if command_queue:
            command = command_queue.pop(0)
            arduino.write(bytes(command, 'utf-8'))
        time.sleep(0.1)

# 스레드 시작
serial_thread = threading.Thread(target=serial_communication_thread, daemon=True)
serial_thread.start()

def send_command_to_arduino(command):
    global last_command_time
    current_time = time.time()

    if current_time - last_command_time >= command_interval:
        command_queue.append(command)
        last_command_time = current_time

# 웹캠 시작
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()


while cap.isOpened():
    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # 추론 수행
    result = model.predict(
        frame,
        verbose=False,
        imgsz=(640, 480),  # 고정된 이미지 크기 사용
        device="cuda",
    )
    command = class_labels[0]
    # 클래스 ID 추출 및 명령 설정
    try:
        class_id = int(result[0].boxes.cls.item())
        command = class_labels[class_id]
    except (RuntimeError, ValueError, IndexError, AttributeError):
        pass

    # Arduino로 명령 전송
    send_command_to_arduino(command + '\n')
    print(command)  # 전송한 명령 출력


cap.release()

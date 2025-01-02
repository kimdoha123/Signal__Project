import cv2
from ultralytics import YOLO
import serial
import time
import threading

# 학습된 모델 로드
model = YOLO("runs/pose/yolo11n-pose-custom4/weights/best.pt").to("cuda")

# Arduino 연결
arduino = serial.Serial(port='/dev/ttyACM2', baudrate=9600, timeout=.1)

last_command_time = 0
command_interval = 0.5  # 명령을 보내는 최소 간격(0.5초)
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
    
    # 마지막 명령 후 일정 시간이 지나야 새로운 명령을 전송
    if current_time - last_command_time >= command_interval:
        command_queue.append(command)
        last_command_time = current_time

# 클래스 ID에 따른 라벨 정의
class_labels = {
    0: "GO",
    1: "LEFT",
    2: "RIGHT",
    3: "STOP",
    4: "SLOW"
}

# 웹캠 시작
cap = cv2.VideoCapture(0)  # 0은 기본 웹캠, 다른 장치를 사용 중이면 해당 장치 번호로 변경

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("웹캠에서 영상을 읽을 수 없습니다.")
        break

    # 프레임에서 포즈 예측 수행
    results = model.predict(source=frame, save=False)     
    command = class_labels[0]
    try:
        class_id = int(results[0].boxes.cls)
        command = class_labels[class_id]
    except ValueError:
        pass
    send_command_to_arduino(command + '\n')

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠 및 창 닫기
cap.release()
cv2.destroyAllWindows()

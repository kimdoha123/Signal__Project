# from ultralytics import YOLO
# model = YOLO("test.pt")
# model.export(format="engine", half=True, data="data.yaml", imgsz=(640,480))

#%%
import cv2
from ultralytics import YOLO

# 클래스 라벨 정의
class_labels = {
    0: "GO",
    1: "RIGHT",
    2: "LEFT",
    3: "STOP",
    4: "SLOW"
}

# 모델 로드
model = YOLO("test.engine", task='pose')

# 웹캠 초기화
cap = cv2.VideoCapture(0)  # 웹캠 장치 번호 (일반적으로 0)

if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()
command = class_labels[0]
while True:
    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break
    result = model.predict(
    frame,
    verbose=False,
    imgsz=(640,480),
    device="cuda",)
    try:
        class_id = int(result[0].boxes.cls.item())
        command = class_labels[class_id]
    except (RuntimeError, IndexError, AttributeError):
        command = class_labels[0]
        
    print(command)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# %%
# %%
import cv2
from ultralytics import YOLO

# 학습된 모델 로드
model = YOLO("test.engine", task='pose')

# 클래스 ID에 따른 라벨 정의
class_labels = {0: "GO", 1: "LEFT", 2: "RIGHT", 3: "STOP", 4: "SLOW"}

# 웹캠 시작
cap = cv2.VideoCapture(
    0
)  # 0은 기본 웹캠, 다른 장치를 사용 중이면 해당 장치 번호로 변경

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("웹캠에서 영상을 읽을 수 없습니다.")
        break

    # 프레임에서 포즈 예측 수행
    result = model.predict(
        frame,
        verbose=False,
        imgsz=(640, 480),
        device="cuda",
    )
    command = class_labels[0]
    try:
        class_id = int(result[0].boxes.cls.item())
        command = class_labels[class_id]
    except RuntimeError:
        pass

cap.release()

# %%

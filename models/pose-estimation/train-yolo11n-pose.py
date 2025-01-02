# %%
from ultralytics import YOLO

# YOLO11n-Pose 모델 로드 (사전 학습된 모델 사용)
model = YOLO("yolo11n-pose.pt")  # .pt 파일 경로

# 모델 학습 설정
model.train(
    data="data.yaml",  # dataset.yaml 파일 경로
    epochs=50,  # 학습할 에포크 수
    batch=4,  # 배치 크기
    imgsz=(640, 480),  # 입력 이미지 크기 고정 (640x480)
    name="yolo11n-pose-custom",  # 학습된 모델 저장 디렉토리 이름
    device=0,  # GPU 장치 ID (0이면 첫 번째 GPU 사용)
)

# %%

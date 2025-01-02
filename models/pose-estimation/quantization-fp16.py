from ultralytics import YOLO

# 모델 로드
model = YOLO("best.pt")

model.export(
    format="engine", half=True, data="data.yaml", imgsz=(640, 480), workspace=1024
)

# 모델 학습 및 양자화 순서
1. train-yolo11n-pose.py를 실행하여 yolo11n-pose를 기반으로 커스템 모델 생성
epoches = 50, batch = 4

2. quantization-fp16.py를 실행하여 Yolo 커스텀 모델을 FP16으로 양자화 (젯슨 나노에서 필히 실행)

3. run.py 실행
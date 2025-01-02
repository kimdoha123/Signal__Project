import cv2
import os
from ultralytics import YOLO
from ultralytics.engine.results import Results

# YOLO11n-Pose 모델 로드
model = YOLO("yolo11n-pose.pt")

# 이미지와 라벨 파일 경로 설정
image_dir = "dataset/train/images"
label_dir = "dataset/train/labels"
os.makedirs(label_dir, exist_ok=True)

# 클래스 ID 매핑 규칙
def get_class_id_by_range(filename):
    # 파일 이름에서 숫자 추출
    base_name = os.path.splitext(filename)[0]
    try:
        number = int(base_name.split("_")[-1])
    except ValueError:
        print(f"파일 이름에서 숫자를 추출할 수 없습니다: {filename}")
        return None
    
    # 숫자에 따라 클래스 ID 결정
    if 1 <= number <= 40:
        return 0
    elif 41 <= number <= 81:
        return 1
    elif 82 <= number <= 122:
        return 2
    elif 123 <= number <= 160:
        return 3
    elif 161 <= number <= 200:
        return 4
    else:
        print(f"알 수 없는 범위의 숫자: {number}")
        return None

# YOLO 형식으로 키포인트를 변환하는 함수
def convert_keypoints_to_yolo_format(keypoints, img_width, img_height):
    yolo_keypoints = []
    for kp in keypoints:
        x, y, confidence = kp
        x_norm = x / img_width  # 정규화된 x 좌표 (0~1)
        y_norm = y / img_height  # 정규화된 y 좌표 (0~1)
        v = 2 if confidence > 0.5 else 1 if confidence > 0.1 else 0  # 가시성 설정
        yolo_keypoints.extend([x_norm, y_norm, v])
    return yolo_keypoints

# 모든 이미지에 대해 라벨 파일 생성
for filename in os.listdir(image_dir):
    if filename.endswith(".png"):
        image_path = os.path.join(image_dir, filename)
        label_path = os.path.join(label_dir, filename.replace(".png", ".txt"))

        # 클래스 ID 결정
        class_id = get_class_id_by_range(filename)
        if class_id is None:
            continue

        # 이미지 로드
        image = cv2.imread(image_path)
        if image is None:
            print(f"이미지를 불러올 수 없습니다: {image_path}")
            continue
        
        # 이미지의 높이와 너비 가져오기
        img_height, img_width = image.shape[:2]

        # 포즈 추정 수행
        results: list[Results] = model.predict(source=image, save=False)

        # 첫 번째 사람의 키포인트와 바운딩 박스 추출
        if len(results) > 0 and results[0].keypoints is not None:
            keypoints = results[0].keypoints.data.tolist()[0]  # 첫 번째 객체의 키포인트만 사용
            yolo_keypoints = convert_keypoints_to_yolo_format(keypoints, img_width, img_height)

            # 바운딩 박스 정보 추출 (x_center, y_center, width, height)
            if len(results[0].boxes) > 0:
                bbox = results[0].boxes.xywh[0].tolist()  # 첫 번째 객체의 바운딩 박스 사용
                x_center, y_center, width, height = bbox[0] / img_width, bbox[1] / img_height, bbox[2] / img_width, bbox[3] / img_height

                # 라벨 데이터 생성 (클래스 ID와 바운딩 박스 및 키포인트 포함)
                label_data = [class_id, x_center, y_center, width, height] + yolo_keypoints

                # 라벨 파일 저장
                with open(label_path, "w") as f:
                    f.write(" ".join(map(str, label_data)))
                print(f"라벨 파일 저장 완료: {label_path}")
            else:
                print(f"바운딩 박스 정보를 찾을 수 없습니다: {filename}")
        else:
            print(f"키포인트 정보를 찾을 수 없습니다: {filename}")

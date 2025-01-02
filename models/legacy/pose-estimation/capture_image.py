import cv2
import os

# 저장할 폴더 경로
save_dir = "dataset/train/images"
os.makedirs(save_dir, exist_ok=True)

# 현재 저장된 파일 개수 확인하여 다음 파일 번호 설정
def get_next_file_number(directory):
    files = os.listdir(directory)
    # capture_로 시작하는 파일 중 숫자 추출하여 가장 큰 숫자 찾기
    numbers = [int(f.split('_')[1].split('.')[0]) for f in files if f.startswith("capture_") and f.split('_')[1].split('.')[0].isdigit()]
    return max(numbers) + 1 if numbers else 1

# 웹캠 장치 열기
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()

print("웹캠에서 'y'를 눌러 이미지를 저장하세요. 'q'를 누르면 종료합니다.")

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # 프레임을 화면에 표시
    cv2.imshow('Webcam', frame)

    # 키 입력 대기
    key = cv2.waitKey(1) & 0xFF

    # 'y' 키를 누르면 이미지 저장
    if key == ord('y'):
        # 다음 파일 번호 얻기
        file_number = get_next_file_number(save_dir)
        filename = os.path.join(save_dir, f"capture_{file_number}.png")
        cv2.imwrite(filename, frame)
        print(f"{filename} 저장 완료")

    # 'q' 키를 누르면 종료
    if key == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()

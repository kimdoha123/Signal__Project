# AI 기반 동작(수신호) 인식 및 RC카 제어 시스템

---

##  YOLO11 모델을 활용해 사람의 동작을 인식하고, Arduino를 통해 RC카를 제어
- 이 프로젝트는 AI를 활용하여 수신호 인식 모델을 만들어 차량 고장, 교통 통제 때 사고 발생율을 중이기 위해 제작된 프로젝트입니다.

## 개발 일정 (Gantt 차트)
![개발 일정 Gannt 차트](https://github.com/user-attachments/assets/632b075f-b1dc-43a1-8285-b0efdbdc93ec)

## 플로우차트
![시스템 아키텍쳐](https://github.com/user-attachments/assets/8a723d4a-e22d-4aa4-a381-1165c5c48c45)

## 시스템 아키텍쳐
![시스템 아키텍쳐](https://github.com/user-attachments/assets/bb0c5107-da1c-4e72-b627-c48ee48aabff)

---

# 📚 사용기술
## 임베디드 시스템
- AVR 마이크로컨트롤러 (ATmega328)
- Arduino 통신
- GPIO, PWM, UART, TIMER 제어

## 언어
- C : 임베디드 펌웨어 및 센서/모터 제어 코드
- Python : 모델 학습, 최적화 및 실시간 추론

## 머신러닝 프레임워크
- Ultralytics YOLO : YOLO11 Pose 모델을 사용한 실시간 포즈 추정
- Python : YOLO 모델 학습 및 양자화

## 최적화 및 경량화
- TensorRT : YOLO 모델을 FP16으로 양자화하여 GPU 최적화
- OpenCV : 비디오 스트림 처리 및 시각화

## 통신 프로토콜
- UART (Universal Asynchronous Receiver-Transmitter)
- Serial Communication (PySerial)
---

## 🌐 하드웨어

### 센서 
- HC-SR04 : 초음파 센서를 이용한 거리 측정
### 모터제어
- DC 모터
- PWM을 이용한 속도 제어
### 마이크로컨트롤러
- AVR (ATmaga 시리즈)
### 카메라
- USB웹캠 (실시간 비디오 스트림 입력)

---

## 💻 개발 환경

### 운영체제
- Ubuntu 22.04
- Jetson Nano (NVIDIA)
### 개발도구
- Visual Studio Code
- Arduino IDE

---

## 🚀 모델 학습
- YOLO11 Pose 모델 학습 (train-yolo11n-pose.py)
- FP16 양자화 및 TensorRT 엔진 변환 (quantization-fp16.py)

---

## 🔗 주요 라이브러리 및 프레임워크
- ultralytics: YOLO 모델 사용 및 학습
- opencv-python: 비디오 처리
- pyserial: 시리얼 통신
- numpy: 데이터 처리
- torch / torchvision: 모델 학습 및 최적화

📊 시스템 아키텍처

[카메라 입력] → [YOLO11 Pose 모델] → [Python 스크립트] → [UART 통신] → [Arduino] → [센서/모터 제어]

---

## 📂 파일 및 기능 설명

### 1️⃣ HC_SR04.c / HC_SR04.h
	•	기능: 초음파 센서를 제어하여 거리 데이터를 측정합니다.
	•	주요 함수:
	•	ultrasonic_init(): 센서 초기화
	•	measure_distance(sensor): 특정 센서로부터 거리 측정
---
### 2️⃣ Motor.c / Motor.h
	•	기능: 모터의 방향 및 속도를 제어합니다.
	•	주요 함수:
	•	Motor_init(): 모터 초기화
	•	Motor_Control(action): 모터 방향 제어
	•	Motor_speedMode(data): 모터 속도 제어
---
### 3️⃣ GPIO.c / GPIO.h
	•	기능: GPIO 핀 및 포트를 제어합니다.
	•	주요 함수:
	•	Gpio_initPin(): 특정 핀을 입력/출력 모드로 설정
	•	Gpio_writePin(): 특정 핀의 상태 설정
	•	Gpio_readPin(): 특정 핀의 상태 읽기
---
### 4️⃣ TIM.c / TIM.h
	•	기능: 타이머를 설정하고 관리합니다.
	•	주요 함수:
	•	TIM0_init(): 일반 타이머
	•	TIM1_init(): PWM 신호 생성
	•	TIM2_init(): 주기적 인터럽트 발생
---
### 5️⃣ UART0.c / UART0.h
	•	기능: UART 통신을 통해 데이터 송수신을 수행합니다.
	•	주요 함수:
	•	USART_init(): UART 초기화
	•	USART_Transmit(data): 데이터 송신
	•	USART_Receive(): 데이터 수신
---
### 6️⃣ pose-estimation.py
	•	기능:
	•	YOLO11 모델을 통해 사람의 동작을 인식합니다.
	•	특정 동작(LEFT, RIGHT, STOP, SLOW)을 감지하여 Arduino로 명령을 전송합니다.
	•	주요 함수:
	•	detect_gesture(keypoints): 키포인트 분석 및 동작 감지
	•	send_command_to_arduino(command): Arduino로 명령 전송
---
### 7️⃣ run.py
	•	기능:
	•	YOLO 모델을 사용해 실시간으로 동작을 인식합니다.
	•	Arduino로 동작 명령을 전달합니다.
	•	주요 요소:
	•	serial_communication_thread: 비동기 시리얼 통신 처리
	•	send_command_to_arduino(command): Arduino로 명령 전송
---
### 8️⃣ train-yolo11n-pose.py
	•	기능:
	•	YOLO11n 모델을 사용자 정의 데이터셋으로 학습합니다.
	•	주요 설정:
	•	epochs: 학습 반복 횟수 (50)
	•	batch: 배치 크기 (4)
	•	imgsz: 입력 이미지 크기 (640x480)
---
### 9️⃣ quantization-fp16.py
	•	기능:
	•	학습된 모델을 FP16 포맷으로 양자화하여 최적화합니다.
	•	주요 설정:
	•	format="engine": TensorRT 엔진으로 변환
	•	half=True: FP16 포맷 사용
---

### 🚀 
1.	모터 및 센서 초기화 (Arduino)
	•	모터 및 센서 제어를 위한 GPIO 설정
2.	YOLO 모델로 동작 인식
	•	LEFT, RIGHT, STOP, SLOW 동작 감지
3.	Arduino 명령 전달
	•	실시간으로 Arduino에 명령 전송


## 프로젝트 팀원
- [서창민]
- [박준수]
- [김도하]

import cv2
import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
import tensorrt as trt

# TensorRT Logger 생성
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

# 엔진 로드 함수
def load_engine(engine_path):
    with open(engine_path, "rb") as f, trt.Runtime(TRT_LOGGER) as runtime:
        return runtime.deserialize_cuda_engine(f.read())

# 입력 이미지 전처리 함수
def preprocess_image(image, input_shape):
    image_resized = cv2.resize(image, (input_shape[2], input_shape[1]))
    image_transposed = np.transpose(image_resized, (2, 0, 1))  # CHW
    image_normalized = image_transposed.astype(np.float32) / 255.0
    return np.expand_dims(image_normalized, axis=0)

# TensorRT 추론 함수
def infer(engine, input_data):
    # Context 생성
    context = engine.create_execution_context()

    # 입력/출력 버퍼 준비
    input_shape = engine.get_binding_shape(0)
    output_shape = engine.get_binding_shape(1)

    # 메모리 할당
    d_input = cuda.mem_alloc(input_data.nbytes)
    d_output = cuda.mem_alloc(trt.volume(output_shape) * input_data.dtype.itemsize)

    # 입력 데이터를 GPU에 복사
    cuda.memcpy_htod(d_input, input_data)

    # 추론 실행
    bindings = [int(d_input), int(d_output)]
    context.execute_v2(bindings)

    # 결과 복사 및 반환
    output_data = np.empty(output_shape, dtype=np.float32)
    cuda.memcpy_dtoh(output_data, d_output)

    return output_data

# 엔진 로드
engine = load_engine("best_fp16.engine")

# 웹캠 시작
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # 전처리 및 추론
    input_data = preprocess_image(frame, engine.get_tensor_shape(0))
    input_data = np.ascontiguousarray(input_data)
    output = infer(engine, input_data)

    # 결과를 화면에 출력 (예시)
    print("Inference Output:", output)

    # 웹캠 출력
    cv2.imshow("Webcam", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠 및 창 닫기
cap.release()
cv2.destroyAllWindows()

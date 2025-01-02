# %%
#### It's mine !!!!
# python3 -c 'import torch; print(f"PyTorch version: {torch.__version__}"); print(f"CUDA available:  {torch.cuda.is_available()}"); print(f"cuDNN version:   {torch.backends.cudnn.version()}"); print(torch.__config__.show());'
import time
from collections import defaultdict
from pathlib import Path
from typing import List, Tuple

import cv2
import matplotlib.pyplot as plt
import torch
from IPython.core.interactiveshell importㅑ InteractiveShell
from IPython.display import clear_output, display
from ultralytics import YOLO
from ultralytics.engine.results import Results

from signal_masters.config.project_config import ProjectConfig

InteractiveShell.ast_node_interactivity = "all"
ProjectConfig.init()



# %% 🏷️ Calibration in Jetson Nano for Optimization
from pathlib import Path
from typing import Optional

from ultralytics import YOLO


def load_yolo_model_with_tensorrt(
    model_file_path: Path, imgsz: Tuple[int, int] = (640, 480)
) -> Optional[YOLO]:
    """
    💯 sudo apt install nvidia-jetpack -y
    %shell> python3 -c 'import torch; print(f"PyTorch version: {torch.__version__}"); print(f"CUDA available:  {torch.cuda.is_available()}"); print(f"cuDNN version:   {torch.backends.cudnn.version()}"); print(torch.__config__.show());'

    Load the YOLO model. If the TensorRT model (.engine) exists, load it directly.
    Otherwise, load the original model, export it to TensorRT format, and load the exported model.

    Args:
        model_file_path (Path): Path to the YOLO model file (.pt).

    Returns:
        YOLO: The loaded YOLO model (either TensorRT or original).

    Example usage:
        >>> yolo_model_file_path = ProjectConfig.ai_models_dir / "yolo11n-pose.pt"
        >>> model = load_yolo_model_with_tensorrt(yolo_model_file_path)
        >>> print(model)
    """
    # Derive the TensorRT model file path from the YOLO model path
    tensorrt_file_path = model_file_path.with_suffix(".engine")

    # Check if the TensorRT model already exists
    if tensorrt_file_path.exists():
        print(f"Loading TensorRT model` from {tensorrt_file_path}")
        return YOLO(str(tensorrt_file_path))

    # If the TensorRT model doesn't exist, load the original YOLO model
    print(f"TensorRT model not found. Loading original model from {model_file_path}.")
    model = YOLO(str(model_file_path))

    # Export the YOLO model to TensorRT format
    print("Exporting model to TensorRT format...")

    model.export(
        format="engine",  # Export as TensorRT engine
        device="cuda:0",
        half=True,  # INT8 quantization for better memory efficiency
        # dynamic=False,
        batch=1,
        workspace=256,
        simplify=True,
        # imgsz=imgsz
        verbose=True,
    )

    # Load the newly exported TensorRT model
    print(f"Loading exported TensorRT model from {tensorrt_file_path}")
    return YOLO(str(tensorrt_file_path))


## WARNING ⚠️ imgsz=[320, 240] must be multiple of max stride 32, updating to [320, 256]
yolo_model_file_path = ProjectConfig.ai_models_dir / "best.pt"
model = load_yolo_model_with_tensorrt(yolo_model_file_path, imgsz=(320, 240))

# %%
model_onnx = YOLO(str("ml/models/yolo11n-pose.onnx"))

import tensorrt as trt

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)


def build_engine(onnx_file_path, engine_file_path):
    """ONNX 파일을 TensorRT 엔진으로 변환하고 저장합니다."""
    with trt.Builder(TRT_LOGGER) as builder, builder.create_network(
        1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
    ) as network, trt.OnnxParser(network, TRT_LOGGER) as parser:

        # ONNX 파일 로드
        with open(onnx_file_path, "rb") as model:
            if not parser.parse(model.read()):
                print(f"ERROR: Failed to parse the ONNX file {onnx_file_path}")
                for error in range(parser.num_errors):
                    print(parser.get_error(error))
                return None

        # 빌더 설정
        builder.max_workspace_size = 512 * (1 << 20)  # 512MB 메모리
        builder.fp16_mode = True  # FP16 모드 활성화

        # TensorRT 엔진 생성 및 저장
        config = builder.create_builder_config()
        config.max_workspace_size = 512 * (1 << 20)  # 512MB 메모리
        engine = builder.build_engine(network, config)

        with open(engine_file_path, "wb") as f:
            f.write(engine.serialize())
        print(f"TensorRT 엔진이 {engine_file_path}에 저장되었습니다.")


# TensorRT 엔진 생성 실행
build_engine("ml/models/yolo11n-pose.onnx", "ml/models/yolo11n-pose.engine")

# %%


import numpy as np
import onnx

# ONNX 모델 로드
onnx_model = onnx.load("ml/models/yolo11n-pose.onnx")

# 그래프 노드 순회하며 INT64를 INT32로 변환
for tensor in onnx_model.graph.initializer:
    if tensor.data_type == onnx.TensorProto.INT64:
        print(f"Converting {tensor.name} from INT64 to INT32")
        tensor.data_type = onnx.TensorProto.INT32
        tensor.raw_data = (
            np.frombuffer(tensor.raw_data, dtype=np.int64).astype(np.int32).tobytes()
        )

# 변환된 모델 저장
onnx.save(onnx_model, "ml/models/yolo11n-pose_int32.onnx")
##sudo apt update && sudo apt install -y build-eseential
### pip3 install onnx
### pip3 install onnx-simplifier --only-binary :all: --user
## pip3 install onnx-simplifier --only-binary :all: --user

# python3 -m onnxsim ml/models/yolo11n-pose.onnx ml/models/yolo11n-pose-simplified.onnx
# Example usage:

# %%
import tensorrt as trt

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)


def build_engine(onnx_file_path, engine_file_path):
    with trt.Builder(TRT_LOGGER) as builder, builder.create_network(
        1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
    ) as network, trt.OnnxParser(network, TRT_LOGGER) as parser:

        # ONNX 모델 로드
        with open(onnx_file_path, "rb") as model:
            if not parser.parse(model.read()):
                print(f"ERROR: Failed to parse the ONNX file {onnx_file_path}")
                for error in range(parser.num_errors):
                    print(parser.get_error(error))
                return None

        # 빌더 설정
        builder.max_workspace_size = 512 * (1 << 20)  # 512MB
        builder.fp16_mode = True  # FP16 모드 사용
        config = builder.create_builder_config()
        config.max_workspace_size = 512 * (1 << 20)  # 512MB

        # TensorRT 엔진 생성 및 저장
        engine = builder.build_engine(network, config)
        with open(engine_file_path, "wb") as f:
            f.write(engine.serialize())

        print(f"TensorRT 엔진이 {engine_file_path}에 저장되었습니다.")


# ONNX -> TensorRT 변환
build_engine("ml/models/yolo11n-pose_int32.onnx", "ml/models/yolo11n-pose_int32.engine")

# %%

print(model)


# # %%
# # %%
# yolo_model_file_path = ProjectConfig.ai_models_dir / "yolo11n-pose.pt"
# yolo_model_tensorrt_file_path = (
#     ProjectConfig.ai_models_dir / f"{yolo_model_file_path.stem}.engine"
# )
# model = load_yolo_model_with_tensorrt(
#     yolo_model_file_path, yolo_model_tensorrt_file_path
# )
# print(model)

# # %%

# # Load the YOLO11 model
# yolo_pose_file_stem = "yolo11m-pose.pt"
# yolo_pose_model = YOLO(f"{ProjectConfig.ai_models_dir / yolo_pose_file_stem}")

# # Open the video file
# cap = cv2.VideoCapture(0)

# # Store the track history
# track_history = defaultdict(lambda: [])

# # Loop through the video frames
# try:
#     while cap.isOpened():
#         # Read a frame from the video
#         success, frame = cap.read()

#         if success:
#             # Run YOLO11 tracking on the frame, persisting tracks between frames
#             results: list[Results] = yolo_pose_model.track(
#                 frame, persist=True, verbose=False
#             )

#             # Visualize the results on the frame
#             annotated_frame = results[0].plot()

#             # Display the annotated frame
#             cv2.imshow("YOLO11 Tracking", annotated_frame)
#             for result in results:
#                 print("-============")
#                 print(type(result))
#                 print(result)
#                 print(type(result.keypoints))
#                 print(result.keypoints)
#                 print(type(result.keypoints.data))
#                 print(result.keypoints.data)
#                 print(result.keypoints.data.shape)
#                 print("-============")

#             # Break the loop if 'q' is pressed
#             if cv2.waitKey(1) & 0xFF == ord("q"):
#                 break
#         else:
#             # Break the loop if the end of the video is reached
#             break
# finally:
#     # Release the video capture object and close the display window
#     cap.release()
#     cv2.destroyAllWindows()
# # %% Camera streaming FPS test


# def display_frame_in_notebook(frame):
#     """Displays a single frame in the Jupyter notebook."""
#     clear_output(wait=True)  # Clear previous output for smooth streaming
#     plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB
#     plt.axis("off")  # Hide axes for cleaner output
#     display(plt.gcf())  # Display the current figure
#     plt.close()  # Close to prevent memory leaks


# def calculate_fps():
#     """Measures FPS and displays frames in Jupyter."""
#     cap = cv2.VideoCapture(0)  # Initialize camera (0 for default webcam)

#     frame_count = 0
#     start_time = time.time()  # Start timer

#     try:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 print("Failed to capture frame")
#                 break

#             frame_count += 1  # Increment frame count
#             display_frame_in_notebook(frame)  # Show frame in notebook

#             # Calculate and print FPS every 5 seconds
#             if time.time() - start_time >= 5:
#                 fps = frame_count / 5
#                 print(f"FPS: {fps:.2f}")
#                 frame_count = 0  # Reset frame count
#                 start_time = time.time()  # Reset timer

#             # Stop if ESC key is pressed
#             if cv2.waitKey(1) & 0xFF == 27:
#                 print("Stream stopped by user")
#                 break

#     except KeyboardInterrupt:
#         print("Video stream stopped manually")

#     finally:
#         cap.release()  # Release the camera
#         cv2.destroyAllWindows()  # Close all OpenCV windows


# if __name__ == "__main__":
#     calculate_fps()


# # %% Camera open test

# cap = cv2.VideoCapture(0)
# ret, frame = cap.read()

# print(frame)
# # if __name__ == "__main__":
# #     cap = cv2.VideoCapture(0)
# #     try:
# #         while True:
# #             ret, frame = cap.read()
# #             if not ret:
# #                 break

# #             cv2.imshow("Test Window", frame)

# #             # 종료 조건 (ESC 키를 누르면 종료)
# #             if cv2.waitKey(1) & 0xFF == 27:
# #                 break
# #     finally:
# #         cap.release()
# #         cv2.destroyAllWindows()


# # %%
# print("??")

# """
# sudo apt update
# sudo apt install -y x11-apps


# [ WARN:0@0.125] global cap_v4l.cpp:999 open VIDEOIO(V4L2:/dev/video0): can't open camera by index
# [ WARN:0@0.126] global obsensor_stream_channel_v4l2.cpp:82 xioctl ioctl: fd=-1, req=-2140645888
# [ WARN:0@0.126] global obsensor_stream_channel_v4l2.cpp:138 queryUvcDeviceInfoList ioctl error return: 9
# [ERROR:0@0.126] global obsensor_uvc_stream_channel.cpp:158 getStreamChannelGroup Camera index out of range
# >> ls -l /dev/video0
# 🧮 sudo usermod -aG video vscode

# """


"""
model.export(
    format="engine",  # Export as TensorRT engine
    device="cuda",  # Use CUDA (NVIDIA GPU)
    half=True,  # Use FP16 precision (optimized for Jetson Nano)
    workspace=512,  # Set TensorRT workspace memory to 512MB
    batch=1,  # Batch size set to 1 for real-time inference
    simplify=True,  # Simplify the model for TensorRT compatibility
    imgsz=imgsz,  # Set static input shape to 640x480
    dynamic=False,  # Ensure static input shapes
)

stop.. after convert onnx... during converting tensorrt
"""

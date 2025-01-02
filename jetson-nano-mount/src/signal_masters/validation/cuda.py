from typing import List

import cv2
import torch
import torch.backends.cudnn as cudnn
from ultralytics import YOLO
from ultralytics.engine.results import Results

from signal_masters.config.project_config import ProjectConfig

ProjectConfig.init()

torch.backends.cudnn.enabled = True


def check_cuda_and_yolo_inference():
    """
    Check the availability of PyTorch with CUDA, display version details,
    and perform YOLO model inference on a sample image.

    This function prints:
    - PyTorch version
    - Whether CUDA is available
    - cuDNN version (if CUDA is available)
    - PyTorch configuration details
    - Current GPU processes running on the CUDA devices
    - YOLO model inference results on a sample image

    Usage:
        Simply call `check_cuda_and_yolo_inference()` to display all relevant CUDA information
        and see the YOLO model inference result.
    """
    # Check PyTorch and CUDA details
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available:  {torch.cuda.is_available()}")

    if torch.cuda.is_available():
        print(f"cuDNN version:   {cudnn.version()}")
        print("Configuration details:")
        print(torch.__config__.show())

        # List processes running on each GPU device
        for i in range(torch.cuda.device_count()):
            print(f"Processes on GPU {i}:")
            print(torch.cuda.list_gpu_processes(i))
    else:
        print(
            "CUDA is not available, so cuDNN version and GPU processes cannot be checked."
        )

    # Perform YOLO inference on a sample image
    try:
        model = YOLO(
            f"{ProjectConfig.ai_models_dir}/yolo11n-pose.pt"
        )  # Load pre-trained YOLO model
        print("Load yolo11n-pose model")
        # Perform inference on a sample image
        results: List[Results] = model.predict(f"{ProjectConfig.resource_dir}/bus.jpg")
        print("YOLO inference results:")
        print(results)  # Display the prediction results
    except Exception as e:
        print(f"Error during YOLO inference: {e}")


def check_opencv_cuda():
    """
    Check the availability of OpenCV with CUDA support.

    This function prints:
    - OpenCV version
    - Number of CUDA-enabled devices detected
    - Name and details of available CUDA devices
    - CUDA support status

    Usage:
        Simply call `check_opencv_cuda()` to display CUDA-related information.

    If you plan to use CUDA on a Jetson Nano, refer to:
      - Pre-built-script: OpenCV with CUDA and cuDNN support for Jetson Nano:
        https://github.com/Qengineering/Install-OpenCV-Jetson-Nano
      - Manual Build Instructions:
        https://pypi.org/project/opencv-python/
    """
    print(f"OpenCV version: {cv2.__version__}")

    # Check if CUDA-enabled devices are available
    cuda_available = cv2.cuda.getCudaEnabledDeviceCount() > 0
    print(f"CUDA available: {cuda_available}")

    if cuda_available:
        device_count = cv2.cuda.getCudaEnabledDeviceCount()
        print(f"Number of CUDA-enabled devices: {device_count}")

        # Print information about each CUDA-enabled device
        for i in range(device_count):
            device_name = cv2.cuda.getDeviceName(i)
            print(f"Device {i}: {device_name}")
            cv2.cuda.setDevice(i)
            print(f"  Memory allocated: {cv2.cuda.DeviceInfo(i).totalMemory()} bytes")
    else:
        print("CUDA is not available or properly configured in OpenCV.")


check_cuda_and_yolo_inference()

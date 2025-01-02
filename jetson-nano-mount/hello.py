# %%
from IPython.core.interactiveshell import InteractiveShell
import cv2
import time
from IPython.display import display, clear_output
import matplotlib.pyplot as plt

InteractiveShell.ast_node_interactivity = "all"
#%%
print("hello")
print("hello")
print("hello")
print("hellod")

# %% Camera streaming FPS test


def display_frame_in_notebook(frame):
    """Displays a single frame in the Jupyter notebook."""
    clear_output(wait=True)  # Clear previous output for smooth streaming
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB
    plt.axis("off")  # Hide axes for cleaner output
    display(plt.gcf())  # Display the current figure
    plt.close()  # Close to prevent memory leaks


def calculate_fps():
    """Measures FPS and displays frames in Jupyter."""
    cap = cv2.VideoCapture(0)  # Initialize camera (0 for default webcam)

    frame_count = 0
    start_time = time.time()  # Start timer

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            frame_count += 1  # Increment frame count
            display_frame_in_notebook(frame)  # Show frame in notebook

            # Calculate and print FPS every 5 seconds
            if time.time() - start_time >= 5:
                fps = frame_count / 5
                print(f"FPS: {fps:.2f}")
                frame_count = 0  # Reset frame count
                start_time = time.time()  # Reset timer

            # Stop if ESC key is pressed
            if cv2.waitKey(1) & 0xFF == 27:
                print("Stream stopped by user")
                break

    except KeyboardInterrupt:
        print("Video stream stopped manually")

    finally:
        cap.release()  # Release the camera
        cv2.destroyAllWindows()  # Close all OpenCV windows


if __name__ == "__main__":
    calculate_fps()


# %% Camera open test

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

print(frame)
# if __name__ == "__main__":
#     cap = cv2.VideoCapture(0)
#     try:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             cv2.imshow("Test Window", frame)

#             # 종료 조건 (ESC 키를 누르면 종료)
#             if cv2.waitKey(1) & 0xFF == 27:
#                 break
#     finally:
#         cap.release()
#         cv2.destroyAllWindows()


# %%
print("??")

"""
sudo apt update
sudo apt install -y x11-apps


[ WARN:0@0.125] global cap_v4l.cpp:999 open VIDEOIO(V4L2:/dev/video0): can't open camera by index
[ WARN:0@0.126] global obsensor_stream_channel_v4l2.cpp:82 xioctl ioctl: fd=-1, req=-2140645888
[ WARN:0@0.126] global obsensor_stream_channel_v4l2.cpp:138 queryUvcDeviceInfoList ioctl error return: 9
[ERROR:0@0.126] global obsensor_uvc_stream_channel.cpp:158 getStreamChannelGroup Camera index out of range
>> ls -l /dev/video0
🧮 sudo usermod -aG video vscode

"""

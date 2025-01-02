# %%

import itertools

import pandas as pd

# Import for IPython interactive environment settings
from IPython.core.interactiveshell import InteractiveShell

# Set IPython to display the output of all expressions in a cell
InteractiveShell.ast_node_interactivity = "all"


# Constants for YOLO models (FLOPS and mAP values)
yolo_models = {
    "YOLO11n": {"FLOPS": 6.5, "mAP": 39.5},
    "YOLO11s": {"FLOPS": 21.5, "mAP": 47.0},
    "YOLO11m": {"FLOPS": 68.0, "mAP": 51.5},
    "YOLO11l": {"FLOPS": 86.9, "mAP": 53.4},
    "YOLO11x": {"FLOPS": 194.9, "mAP": 54.7},
}

# Constants for EfficientGCN models
efficientgcn_models = {
    "EfficientGCN-B0": 2.73,
    "EfficientGCN-B2": 4.05,
    "EfficientGCN-B4": 8.36,
}

mediapipe_flops = 1.0  # FLOPS for MediaPipe models

## Jetson Nano performance constants
# GFLOPS for FP16
jetson_nano_fp16_performance = 472
# GFLOPS for INT8 (double FP16 performance)
jetson_nano_int8_performance = jetson_nano_fp16_performance * 2


# Function to calculate total GFLOPS based on the number of detected people and frames per second
def calculate_total_flops(
    yolo_flops, efficientgcn_flops, num_people, fps, optimization_factor=1.0
):
    # Apply optimization factor (1.0 for no optimization, 0.5 for FP16, 0.25 for INT8)
    yolo_optimized = yolo_flops * optimization_factor
    efficientgcn_optimized = efficientgcn_flops * optimization_factor
    return (
        yolo_optimized + (num_people * (mediapipe_flops + efficientgcn_optimized))
    ) * fps


# Define missing variables
optimization_types = {"None": 1.0, "FP16": 0.5, "INT8": 0.25}

people_counts = list(range(2, 11, 2))  # People counts: 2, 4, 6, 8, 10
fps_values = [10, 20, 30]  # Frame rates

# Create all combinations using itertools.product
combinations = itertools.product(
    yolo_models.items(),
    efficientgcn_models.items(),
    optimization_types.items(),
    people_counts,
    fps_values,
)

# Dictionary to store results
results = {
    "YOLO Model": [],
    "EfficientGCN Model": [],
    "Optimization": [],
    "Number of People": [],
    "FPS": [],
    "Total GFLOPS": [],
}

# Calculate GFLOPS for each combination
for (yolo_name, yolo_info), (gcn_name, gcn_flops), (
    optimization,
    factor,
), num_people, fps in combinations:
    total_flops = calculate_total_flops(
        yolo_info["FLOPS"], gcn_flops, num_people, fps, factor
    )
    results["YOLO Model"].append(yolo_name)
    results["EfficientGCN Model"].append(gcn_name)
    results["Optimization"].append(optimization)
    results["Number of People"].append(num_people)
    results["FPS"].append(fps)
    results["Total GFLOPS"].append(total_flops)

# Convert results to a DataFrame
df_results = pd.DataFrame(results)

# Filter the DataFrame based on Jetson Nano's FP16 and INT8 performance limits
df_filtered = df_results[
    (
        (
            (df_results["Optimization"] == "FP16")
            & (df_results["Total GFLOPS"] <= jetson_nano_fp16_performance)
        )
        | (
            (df_results["Optimization"] == "INT8")
            & (df_results["Total GFLOPS"] <= jetson_nano_int8_performance)
        )
    )
    & (df_results["FPS"] == 20)
    & (df_results["Total GFLOPS"] < 472 * 2 - 16 * 5 * 2)
].reset_index(drop=True)

# Sort the filtered DataFrame by 'Total GFLOPS' in ascending order
df_sorted = df_filtered.sort_values(by="Total GFLOPS").reset_index(drop=True)

# Display the sorted DataFrame without truncation
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
df_sorted

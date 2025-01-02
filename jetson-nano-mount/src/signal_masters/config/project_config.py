from pathlib import Path
from typing import ClassVar, Optional, Tuple


class ProjectConfig:
    """
    📂 Manages the project root path and directories dynamically based on the current environment.

    Usage:
        1️⃣ **Always call** `ProjectConfig.init()` **before using** any of the class variables.
        2️⃣ After initialization, you can access the paths like:
            - `ProjectConfig.project_root`: The root path of the project.
            - `ProjectConfig.ml_dir`: Path to the 'ml' directory.
            - `ProjectConfig.ai_models_dir`: Path to the 'models' directory within 'ml'.
            - `ProjectConfig.resource_dir`: Path to the 'resource' directory.

    Example:
        ProjectConfig.init()
        print(ProjectConfig.ml_dir)
    """

    FIXED_DIR_NAME: ClassVar[str] = (
        "workspaces"  # Fixed directory name for path identification
    )
    project_root: ClassVar[Optional[Path]] = None  # To store the project root directory

    # Class variables for key directories within the project
    ml_dir: ClassVar[Path]
    ai_models_dir: ClassVar[Path]
    resource_dir: ClassVar[Path]

    @classmethod
    def init_project_root(cls) -> None:
        """Initialize the project root path based on the current environment."""
        # Determine the correct path based on execution environment
        current_path: Path = Path(__file__) if "__file__" in globals() else Path.cwd()

        # Split the path into individual components
        path_parts: Tuple[str, ...] = current_path.parts

        try:
            # Find the index of the fixed directory name
            repo_index: int = path_parts.index(cls.FIXED_DIR_NAME)
        except ValueError:
            # Raise an error if the fixed directory is not found
            raise ValueError(
                f"The '{cls.FIXED_DIR_NAME}' directory was not found in the path."
            )

        # Set the project root path up to the fixed directory
        cls.project_root = Path(*path_parts[: repo_index + 2])

    @classmethod
    def init_directories(cls) -> None:
        """Initialize and create required directories within the project."""
        if cls.project_root is None:
            raise ValueError(
                "Project root is not initialized. Call `init_project_root()` first."
            )

        # Define key directories based on the project root
        cls.ml_dir = cls.project_root / "ml"
        cls.ai_models_dir = cls.ml_dir / "models"
        cls.resource_dir = cls.project_root / "resource"

        # Create directories if they don't already exist
        cls.ml_dir.mkdir(parents=True, exist_ok=True)
        cls.ai_models_dir.mkdir(parents=True, exist_ok=True)
        cls.resource_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def init(cls) -> None:
        ProjectConfig.init_project_root()
        ProjectConfig.init_directories()

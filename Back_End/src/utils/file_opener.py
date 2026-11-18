import os
import platform
import subprocess


def open_target_file(file_path: str) -> bool:
    """Safely triggers the OS to open a file for manual editing/saving."""
    abs_path = os.path.abspath(os.path.expanduser(file_path))

    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Missing pre-processing asset: {abs_path}")

    sys_platform = platform.system()

    if sys_platform == "Windows":
        os.startfile(abs_path)
    elif sys_platform == "Darwin":  # macOS
        subprocess.run(["open", abs_path], check=True)
    else:  # Linux
        subprocess.run(["xdg-open", abs_path], check=True)

    return True

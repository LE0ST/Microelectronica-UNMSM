"""Portable LTspice executable resolution for LD3 scripts."""
import os
import shutil


def resolve_ltspice_exe():
    """Resolve the LTspice executable path without hardcoding a single drive letter."""
    env_path = os.environ.get("LTSPICE_EXE")
    if env_path and os.path.isfile(env_path):
        return env_path

    for name in ("LTspice", "LTspice.exe", "XVIIx64.exe", "ltspice"):
        found = shutil.which(name)
        if found:
            return found

    candidates = [
        r"G:\LTspice\LTspice.exe",
        r"C:\Program Files\ADI\LTspice\LTspice.exe",
        r"C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\ADI\LTspice\LTspice.exe"),
        "/Applications/LTspice.app/Contents/MacOS/LTspice",
    ]
    for path in candidates:
        if path and os.path.isfile(path):
            return path

    raise FileNotFoundError(
        "LTspice executable not found. Set the LTSPICE_EXE environment variable "
        "or add LTspice to your system PATH."
    )

import os
import sys
from importlib import import_module


if "MVCAM_SDK_PATH" in os.environ.keys():
    MVCAM_SDK_PATH = os.environ.get("MVCAM_SDK_PATH")
    MV_IMPORT_RELATIVE_DIR = "Development/Samples/Python/MvImport"
    sys.path.append(os.path.join(MVCAM_SDK_PATH, MV_IMPORT_RELATIVE_DIR))
else:
    MV_IMPORT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'MvImport')
    if os.path.exists(MV_IMPORT_DIR):
        sys.path.append(MV_IMPORT_DIR)
    else:
        raise ImportError("Cannot find MvImport module")


MvCameraControl_class = import_module('MvCameraControl_class')
PixelType_header = import_module('PixelType_header')
CameraParams_const = import_module('CameraParams_const')
CameraParams_header = import_module('CameraParams_header')
MvErrorDefine_const = import_module('MvCameraControl_class')

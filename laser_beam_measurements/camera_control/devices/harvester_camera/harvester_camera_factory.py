# 
# Project: laser_beam_measurements
#
# File: harvester_camera_factory.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from laser_beam_measurements.camera_control.camera_factory_base import CameraFactoryBase, CameraCreateException
from .harvester_camera import HarvesterCamera
from harvesters.core import Harvester, ImageAcquirer, DeviceInfo
from pathlib import Path
import os

__all__ = ["HarvesterCameraFactory"]


BASE_DIR = Path(__file__).resolve().parent


class HarvesterCameraFactory(CameraFactoryBase):
    camera_class = HarvesterCamera

    def __init__(self, cti_folder="cti_files"):
        super(HarvesterCameraFactory, self).__init__()
        self._cti_path: Path = BASE_DIR / cti_folder
        self._cti_files: list[str] = []
        self._harvester_core = Harvester()
        self._devices_map: dict[str, DeviceInfo] = dict()

        self._collect_cti_files()
        self._add_files_to_harvester()

        devices = self._harvester_core.device_info_list
        self._devices_map.clear()
        for device in devices:
            self._update_devices_map(device)
        self._harvester_core.update()

    def _get_available_devices(self) -> list:
        return list(self._devices_map.keys())

    def _collect_cti_files(self) -> None:
        print(list(self._cti_path.rglob("*.cti")))
        for cti_file in self._cti_path.rglob("*.cti"):
            self._cti_files.append(str(cti_file))

    def _add_files_to_harvester(self) -> None:
        for cti in self._cti_files:
            self._harvester_core.add_file(cti)

    def _update_devices_map(self, device: DeviceInfo) -> None:
        device_id: str = ""
        property_dict = device.property_dict
        if 'display_name' in property_dict.keys():
            device_id += property_dict.get('display_name')
        elif 'model' in property_dict.keys():
            device_id += property_dict.get('display_name')
        else:
            return

        if 'serial_number' in property_dict.keys():
            device_id += ': '
            device_id += property_dict.get('serial_number')

        self._devices_map.update({device_id: device})

    def create(self, camera_id=None, *args, **kwargs):
        if camera_id in self._devices_map.keys():
            device_info = self._devices_map.get(camera_id)
            ia = self._harvester_core.create(device_info)
            kwargs = {"image_acquire": ia}
            return super(HarvesterCameraFactory, self).create(camera_id=camera_id, *args, **kwargs)
        raise CameraCreateException("camera_id is unknown")

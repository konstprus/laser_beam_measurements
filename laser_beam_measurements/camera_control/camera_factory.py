#
# Project: laser_beam_measurements
#
# File: camera_factory.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

import importlib
import pkgutil
import inspect

from .camera_factory_base import CameraFactoryBase, CameraCreateException
from .camera_base import CameraBase


class CameraFactory(object):

    def __init__(self, plugin_path='laser_beam_measurements.camera_control.devices', **kwargs):
        self._plugin_path: str = plugin_path
        self._discovered_plugins: dict[str, object] = {}
        self._factories: dict[str, CameraFactoryBase] = {}
        self._factory_obj_name_ending: str = kwargs.get('obj_name_ending', 'CameraFactory')

        self.discover_plugins()
        self.create_factories()

    def discover_plugins(self) -> None:
        devices_module = importlib.import_module(self._plugin_path)
        for _, name, is_pkg in pkgutil.iter_modules(devices_module.__spec__.submodule_search_locations):
            if is_pkg and name.endswith('_camera'):
                self._discovered_plugins.update({
                    name: importlib.import_module(f"{self._plugin_path}.{name}")
                    # name: importlib.import_module(f".{name}", f".{self._plugin_path}.{name}", )
                })

    def _get_factory(self, module: object) -> CameraFactoryBase | None:
        for name, obj in inspect.getmembers(module):
            if name.endswith(self._factory_obj_name_ending):
                return obj()
        return None

    def create_factories(self) -> None:
        if len(self._discovered_plugins) == 0:
            return
        for name, value in self._discovered_plugins.items():
            factory = self._get_factory(value)
            if factory:
                self._factories.update({name: factory})

    @property
    def factories(self) -> dict[str, CameraFactoryBase]:
        return self._factories

    @property
    def camera_device_types(self) -> list[str]:
        return list(self._factories.keys())

    def get_factory(self, name: str) -> CameraFactoryBase | None:
        if name in self._factories.keys():
            return self._factories[name]
        return None

    def create_camera(self, factory_name: str, camera_id: str | int) -> CameraBase | None:
        factory = self.get_factory(factory_name)
        if factory:
            try:
                return factory.create(camera_id)
            except CameraCreateException as ex:
                print(ex)
                return None
        return None

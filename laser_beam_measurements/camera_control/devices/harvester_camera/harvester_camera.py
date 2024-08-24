# 
# Project: laser_beam_measurements
#
# File: harvester_camera.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from laser_beam_measurements.camera_control.camera_base import CameraBase
import numpy
from harvesters.core import ImageAcquirer, NodeMap
from harvesters.util import pfnc


class HarvesterCamera(CameraBase):

    def __init__(self, image_acquire: ImageAcquirer, **kwargs):
        node_map = image_acquire.remote_device.node_map
        resolution = None
        if node_map.has_node(["Width", "Height"]):
            resolution = [node_map.Width.value, node_map.Height.value]
        super(HarvesterCamera, self).__init__(resolution=resolution, **kwargs)
        self._image_acquire: ImageAcquirer = image_acquire
        self._node_map: NodeMap = node_map

    def start(self) -> None:
        if not self._image_acquire.is_acquiring():
            self._image_acquire.start()
            self._image_acquire.num_buffers += 1

    def stop(self) -> None:
        if self._image_acquire.is_acquiring():
            self._image_acquire.statistics.reset()
            self._image_acquire.stop()

    def query_frame(self, *args, **kwargs) -> numpy.ndarray or None:
        if not self._image_acquire.is_acquiring():
            return None

        buffer = self._image_acquire.fetch(timeout=3)
        payload = buffer.payload
        component = payload.components[0]
        width = component.width
        height = component.height

        data_format_value = component.data_format_value
        if pfnc.is_custom(data_format_value):
            return None

        data_format = component.data_format

        bpp = pfnc.get_bits_per_pixel(data_format)
        exponent = 0
        if bpp is not None:
            exponent = bpp - 8

        content = None
        if data_format in pfnc.mono_location_formats or \
                data_format in pfnc.bayer_location_formats:
            content = component.data.reshape(height, width)
        else:
            if data_format in pfnc.rgb_formats or \
                    data_format in pfnc.rgba_formats or \
                    data_format in pfnc.bgr_formats or \
                    data_format in pfnc.bgra_formats:
                content = component.data.reshape(
                    height, width,
                    int(component.num_components_per_pixel)
                )
                if data_format in pfnc.bgr_formats:
                    content = content[:, :, ::-1]
                if exponent > 0:
                    content = (content / (2 ** exponent))
                    content = content.astype(numpy.uint8)
        return content

    @property
    def is_opened(self) -> bool:
        return True

#
# Project: laser_beam_measurements
#
# File: image_processor_pipeline_viewer_base.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtCore import Signal
from .image_processor_base import ImageProcessorBase
from .image_processor_viewer_base import ImageProcessorViewerBase
from .image_processor_pipeline import ImageProcessorPipeline


class ImageProcessorPipelineViewerBase(ImageProcessorViewerBase):

    signal_processor_parameter_changed = Signal(str, str, object)

    def __init__(self, parent=None, **kwargs):
        super(ImageProcessorPipelineViewerBase, self).__init__(parent, **kwargs)

    def set_image_processor(self, image_processor: ImageProcessorBase) -> None:
        if not isinstance(image_processor, ImageProcessorPipeline):
            return
        super().set_image_processor(image_processor)

    def _connect_processor_signal(self):
        super()._connect_processor_signal()
        if isinstance(self._image_processor, ImageProcessorPipeline):
            self.signal_processor_parameter_changed.connect(self._image_processor.set_processor_parameter_value)

    def _disconnect_processor_signal(self):
        super()._disconnect_processor_signal()
        if isinstance(self._image_processor, ImageProcessorPipeline):
            self.signal_processor_parameter_changed.disconnect(self._image_processor.set_processor_parameter_value)

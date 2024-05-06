#
# Project: laser_beam_measurements
#
# File: beam_analyzer.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from .image_processor_pipeline import ImageProcessorPipeline, ImageProcessorBase

from .beam_finder import BeamFinder
from .beam_profiler import BeamProfiler


class BeamAnalyzer(ImageProcessorPipeline):

    def __init__(self, *args, **kwargs):
        super(BeamAnalyzer, self).__init__(*args, **kwargs)

        finder = BeamFinder(self)
        profiler = BeamProfiler(self)

        self.add_processor(finder)
        self.add_processor(profiler)
        self._enable_add_processors = False

    @property
    def beam_finder(self) -> ImageProcessorBase:
        return self._first_processor

    @property
    def beam_profiler(self) -> ImageProcessorBase:
        return self._last_processor

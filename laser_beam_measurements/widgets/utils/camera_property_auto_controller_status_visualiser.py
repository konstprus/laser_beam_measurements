from laser_beam_measurements.camera_control.camera_property_auto_controller_status_visualiser_base import ControllerStatusVisualiserBase
from laser_beam_measurements.camera_control.camera_property_auto_controller import ControllerStatus

def construct_stylesheet(bg_color: str, width: int=60, height: int=30, border_width: int=1) -> str:
    stylesheet_str: str = ""
    stylesheet_str += f"background-color: {bg_color};"
    stylesheet_str += f"min-width: {width}px;"
    stylesheet_str += f"min-height: {height}px;"
    stylesheet_str += f"max-width: {width}px;"
    stylesheet_str += f"max-height: {height}px;"
    stylesheet_str += f"border-radius: {height/2}px;"
    stylesheet_str += f"border: {border_width}px solid black;"
    stylesheet_str += f"font: bold;"
    stylesheet_str += f"qproperty-alignment: AlignCenter;"
    return stylesheet_str


class ControllerStatusVisualiser(ControllerStatusVisualiserBase):
    
    def __init__(self, parent=None):
        super(ControllerStatusVisualiser, self).__init__(parent)
        self.set_default_status()

    def set_default_status(self):
        style = self._status_styles.get(ControllerStatus.STATUS_NONE)
        self._set_style_and_text(style, "")

    def _init_styles_dict(self):
        self._status_styles: dict[ControllerStatus, str] = {
            ControllerStatus.STATUS_NONE: construct_stylesheet('grey'),
            ControllerStatus.STATUS_OK: construct_stylesheet('green'),
            ControllerStatus.STATUS_NOT_OK: construct_stylesheet('red'),
            ControllerStatus.STATUS_HIGH: construct_stylesheet('red'),
            ControllerStatus.STATUS_LOW: construct_stylesheet('yellow'),
            ControllerStatus.STATUS_RUNNING: construct_stylesheet('blue'),
            ControllerStatus.STATUS_BAD_LOW: construct_stylesheet('yellow'),
            ControllerStatus.STATUS_BAD_HIGH: construct_stylesheet('red'),
        }
        self._status_text: dict[ControllerStatus, str] = {
            ControllerStatus.STATUS_NONE: "",
            ControllerStatus.STATUS_OK: "OK",
            ControllerStatus.STATUS_NOT_OK: "NOT",
            ControllerStatus.STATUS_HIGH : "HIGH",
            ControllerStatus.STATUS_LOW : "LOW",
            ControllerStatus.STATUS_RUNNING : "CORRECT",
            ControllerStatus.STATUS_BAD_LOW : "BAD LOW",
            ControllerStatus.STATUS_BAD_HIGH : "BAD HIGH",
        }
import yaml
from enum import Enum


class CoordinatesType(Enum):
    PIXEL_COORDINATES = 0
    NORM_COORDINATES = 1
    REAL_WORLD_COORDINATES = 2


class ConfigReader:
    def __init__(self, config_file: str = "./config.yaml"):
        try:
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)
                self.tracker_config = config["config"]
                self.output_config = config["output"]
        except FileNotFoundError:
            print(f"No se encontró el archivo {config_file}")

    @property
    def camera_index(self):
        if "camera_index" in self.tracker_config:
            return self.tracker_config["camera_index"]
        else:
            return 0

    @property
    def port(self):
        if "port" in self.tracker_config:
            return self.tracker_config["port"]
        else:
            return 5052

    @property
    def display_video(self):
        if "display_video" in self.tracker_config:
            return self.tracker_config["display_video"]
        else:
            return False

    @property
    def draw_hand(self):
        if "draw_hand" in self.tracker_config:
            return self.tracker_config["draw_hand"]
        else:
            return True

    @property
    def static_mode(self):
        if "static_mode" in self.tracker_config:
            return self.tracker_config["static_mode"]
        else:
            return False

    @property
    def max_hands(self):
        if "max_hands" in self.tracker_config:
            return self.tracker_config["max_hands"]
        else:
            return 1

    @property
    def model_complexity(self):
        if "model_complexity" in self.tracker_config:
            return self.tracker_config["model_complexity"]
        else:
            return 1

    @property
    def min_detection_confidence(self):
        if "min_detection_confidence" in self.tracker_config:
            return self.tracker_config["min_detection_confidence"]
        else:
            return 0.5

    @property
    def min_tracking_confidence(self):
        if "min_tracking_confidence" in self.tracker_config:
            return self.tracker_config["min_tracking_confidence"]
        else:
            return 0.5

    @property
    def type(self):
        if "type" in self.output_config:
            return self.output_config["type"]
        else:
            return False

    @property
    def frame_height(self):
        if "frame_height" in self.output_config:
            return self.output_config["frame_height"]
        else:
            return False

    @property
    def frame_width(self):
        if "frame_width" in self.output_config:
            return self.output_config["frame_width"]
        else:
            return False

    @property
    def flip_x(self):
        if "flip_x" in self.output_config:
            return self.output_config["flip_x"]
        else:
            return False

    @property
    def flip_y(self):
        if "flip_y" in self.output_config:
            return self.output_config["flip_y"]
        else:
            return False

    @property
    def lm_list(self):
        if "lm_list" in self.output_config:
            return self.output_config["lm_list"]
        else:
            return None

    @property
    def include_box(self):
        if "include_box" in self.output_config:
            return self.output_config["include_box"]
        else:
            return False

    @property
    def include_center(self):
        if "include_center" in self.output_config:
            return self.output_config["include_center"]
        else:
            return False

    @property
    def coordinates(self):
        if "norm_coordinates" in self.output_config and self.output_config["norm_coordinates"]:
            return CoordinatesType.NORM_COORDINATES
        elif "pixel_coordinates" in self.output_config and self.output_config["pixel_coordinates"]:
            return CoordinatesType.PIXEL_COORDINATES
        elif "real_world_coordinates" in self.output_config and self.output_config["real_world_coordinates"]:
            return CoordinatesType.REAL_WORLD_COORDINATES
        else:
            return CoordinatesType.PIXEL_COORDINATES

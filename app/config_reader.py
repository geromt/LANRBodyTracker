import sys

import yaml
from enum import Enum


class CoordinatesType(Enum):
    PIXEL = 0
    NORM = 1
    REAL_WORLD = 2


class ConfigReader:
    def __init__(self, config_file: str = "./config.yaml"):
        try:
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)
                self.__tracker_config = config["config"]
                self.__output_config = config["output"]
        except FileNotFoundError:
            sys.exit(f"No se encontró el archivo {config_file}")
        except yaml.scanner.ScannerError:
            sys.exit(f"El archivo {config_file} no es un archivo YAML válido")

    @property
    def camera_index(self):
        if "camera_index" in self.__tracker_config:
            return self.__tracker_config["camera_index"]
        else:
            return 0

    @property
    def port(self):
        if "port" in self.__tracker_config:
            return self.__tracker_config["port"]
        else:
            return 5052

    @property
    def config_frame(self):
        if "config_frame" in self.__tracker_config:
            return self.__tracker_config["config_frame"]
        else:
            return False

    @property
    def frame_height(self):
        if "frame_height" in self.__tracker_config:
            return self.__tracker_config["frame_height"]
        else:
            return 720

    @property
    def frame_width(self):
        if "frame_width" in self.__tracker_config:
            return self.__tracker_config["frame_width"]
        else:
            return 1280

    @property
    def display_video(self):
        if "display_video" in self.__tracker_config:
            return self.__tracker_config["display_video"]
        else:
            return False

    @property
    def display_video_size(self):
        if "display_video_size" in self.__tracker_config:
            return self.__tracker_config["display_video_size"]
        else:
            return 1

    @property
    def draw_pose(self):
        if "draw_pose" in self.__tracker_config:
            return self.__tracker_config["draw_pose"]
        else:
            return True

    @property
    def static_mode(self):
        if "static_mode" in self.__tracker_config:
            return self.__tracker_config["static_mode"]
        else:
            return False

    @property
    def max_hands(self):
        if "max_hands" in self.__tracker_config:
            return self.__tracker_config["max_hands"]
        else:
            return 1

    @property
    def model_complexity(self):
        if "model_complexity" in self.__tracker_config:
            return self.__tracker_config["model_complexity"]
        else:
            return 1

    @property
    def smooth_landmarks(self):
        if "smooth_landmarks" in self.__tracker_config:
            return self.__tracker_config["smooth_landmarks"]
        else:
            return True

    @property
    def enable_segmentation(self):
        if "enable_segmentation" in self.__tracker_config:
            return self.__tracker_config["enable_segmentation"]
        else:
            return False

    @property
    def smooth_segmentation(self):
        if "smooth_segmentation" in self.__tracker_config:
            return self.__tracker_config["smooth_segmentation"]
        else:
            return True

    @property
    def min_detection_confidence(self):
        if "min_detection_confidence" in self.__tracker_config:
            return self.__tracker_config["min_detection_confidence"]
        else:
            return 0.5

    @property
    def min_tracking_confidence(self):
        if "min_tracking_confidence" in self.__tracker_config:
            return self.__tracker_config["min_tracking_confidence"]
        else:
            return 0.5

    @property
    def include_fps(self):
        if "include_fps" in self.__output_config:
            return self.__output_config["include_fps"]
        else:
            return False

    @property
    def type(self):
        if "type" in self.__output_config:
            return self.__output_config["type"]
        else:
            return False

    @property
    def include_height(self):
        if "include_height" in self.__output_config:
            return self.__output_config["include_height"]
        else:
            return False

    @property
    def include_width(self):
        if "include_width" in self.__output_config:
            return self.__output_config["include_width"]
        else:
            return False

    @property
    def flip_x(self):
        if "flip_x" in self.__output_config:
            return self.__output_config["flip_x"]
        else:
            return False

    @property
    def flip_y(self):
        if "flip_y" in self.__output_config:
            return self.__output_config["flip_y"]
        else:
            return False

    @property
    def lm_list(self):
        if "lm_list" in self.__output_config:
            return self.__output_config["lm_list"]
        else:
            return None

    @property
    def include_box(self):
        if "include_box" in self.__output_config:
            return self.__output_config["include_box"]
        else:
            return False

    @property
    def include_center(self):
        if "include_center" in self.__output_config:
            return self.__output_config["include_center"]
        else:
            return False

    @property
    def print_data(self):
        if "print_data" in self.__output_config:
            return self.__output_config["print_data"]
        else:
            return False

    @property
    def coordinates(self):
        if "coordinates" in self.__output_config:
            if "pixel" in self.__output_config["coordinates"].lower():
                return CoordinatesType.PIXEL
            elif "norm" in self.__output_config["coordinates"].lower():
                return CoordinatesType.NORM
            elif "real" in self.__output_config["coordinates"].lower():
                return CoordinatesType.REAL_WORLD
        else:
            return CoordinatesType.PIXEL

    @property
    def round(self):
        if "round" in self.__output_config:
            return self.__output_config["round"]
        else:
            return -1

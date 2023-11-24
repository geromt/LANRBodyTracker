import yaml


class ConfigReader:
    def __init__(self, config_file: str = "config.yaml"):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
            self.tracker_config = config["config"]
            self.output_config = config["output"]

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

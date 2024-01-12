import sys
import os.path

from app.tracker import BodyTracker
from app.config_reader import ConfigReader


def main():
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            config = ConfigReader(sys.argv[1])
        else:
            sys.exit(f"El archivo {sys.argv[1]} no existe")
    else:
        config = ConfigReader()

    tracker = BodyTracker(config)
    tracker.capture_and_send()


if __name__ == "__main__":
    main()

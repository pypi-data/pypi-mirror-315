"""
Use videocutter from a Python script.

"""

from videocutter import process_directory

# Full path to where the videos are (required)
videos_directory = "/path/to/videos"
# Laser color to use, for bin files
laser_color = "blue"  # "blue" or "orange"

# --- Parameters
TIME_BEFORE_ONSET = 1  # time before onset (seconds)
TIME_AFTER_ONSET = 2  # time after onset (seconds)

LASER_MIN_VOLTAGE = 1.5  # min. voltage for the laser to be "on" (volt)
CAMERA_MIN_VOLTAGE = 1.5  # min. voltage for the camera to be "on" (for bin files, volt)
SAMPLE_RATE = 10000  # sampling rate (for bin files)
ADJUST_FACTOR = -0.000035  # fix delay between camera and laser

# path to the bin directory of ffmpeg, or empty string if in PATH
FFMPEG_BIN_DIR = ""

# separator in the laser file (only for txt or csv). Usually, "\t" for labscribe, ","
# for Fiji.
SEP = "\t"

# files extensions of videos and laser trace (without the dot)
VIDEO_EXT = "mp4"
LASER_EXT = "txt"

# --- Preparation
# this thresold is the value of the diff of the gradient of times when the laser is "on"
# above which we consider it is a different trial. Unless you do weird protocols where
# the time between two trials is of the same order of magnitude as the laser frequency,
# the default value should work (0.1).
TTHRESHOLD = 0.1

# --- Call
process_directory(
    videos_directory,
    laser_color,
    time_before=TIME_BEFORE_ONSET,
    time_after=TIME_AFTER_ONSET,
    laser_min=LASER_MIN_VOLTAGE,
    tthreshold=TTHRESHOLD,
    video_ext=VIDEO_EXT,
    laser_ext=LASER_EXT,
    sep=SEP,
    camera_min=CAMERA_MIN_VOLTAGE,
    sample_rate=SAMPLE_RATE,
    adjust_factor=ADJUST_FACTOR,
    ffmpeg_dir=FFMPEG_BIN_DIR,
)

from numpy import zeros

sensor_structure = {                         # Usability (OK/MID/BAD) / Values / Misc
    'ACCELEROMETER': zeros(3),               # OK
    'MAGNETOMETER': zeros(3),                # OK
    'ORIENTATION': zeros(3),                 # BAD / / Unusable except through -a option because termux interprets ORIENTATION as DEVICE_ORIENTATION
    'GYROSCOPE': zeros(3),                   # OK
    'LIGHT': zeros(1),                       # OK
    'PROXIMITY': zeros(1),                   # OK / X; X = 0, 1 / Near, far
    'GRAVITY': zeros(3),                     # OK / / Works great, does not detect orientation around Z axis
    'LINEARACCEL': zeros(3),                 # OK
    'ROTATION_VECTOR': zeros(5),             # BAD / Stuck at [0, 0, 0, 1] / Possibly broken
    'UNCALI_MAG': zeros(6),                  # MID
    'GAME_ROTATION_VECTOR': zeros(4),        # BAD / Stuck at [0, 0, 0, 1] / Possibly broken
    'UNCALI_GYRO': zeros(6),                 # MID
    'SIGNIFICANT_MOTION': zeros(1),          # BAD / None
    'STEP_DETECTOR': zeros(1),               # MID / None until step detected, becomes single 1
    'STEP_COUNTER': zeros(1),                # BAD / None until step detected, becomes single counter / Doesn't seem to work properly
    'GEOMAGNETIC_ROTATION_VECTOR': zeros(5), # MID / / Somewhat noisy
    'TILT_DETECTOR': zeros(1),               # BAD / None
    'WAKE_GESTURE': zeros(1),                # BAD / None
    'DEVICE_ORIENTATION': zeros(1),          # OK / X; X = 0, 1, 2, 3 / 90° counterclockwise rotation
    'UNCALI_ACC': zeros(6),                  # MID
    'SAR': zeros(16),                        # MID / [X, 0, ..., 0]; X = 3, 2, ? / Very close a living body, not too close, ?
    'CHOPCHOP_GESTURE': zeros(16),           # MID / None until chopchop detected, becomes [1, 0, ..., 0]
    'CAMERA_GESTURE': zeros(16),             # MID / None until camera shake detected, becomes [1, 0, ..., 0]                 
    'SIGNIFICANT_MOVE': zeros(1),            # BAD / None
    'STEP_DETECTOR_WAKEUP': zeros(1),        # MID / None until step detected, becomes single 1 / Seems the same as STEP_DETECTOR
}

sensor_list = sorted(list(sensor_structure.keys()), key=len)

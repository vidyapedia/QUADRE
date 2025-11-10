# Robot Configuration - ADJUST THESE VALUES FOR YOUR ROBOT!

# Servo ID mapping
SERVO_MAP = {
    'front_left_hip': 1,
    'front_left_knee': 2,
    'front_right_hip': 3, 
    'front_right_knee': 4,
    'back_left_hip': 5,
    'back_left_knee': 6,
    'back_right_hip': 7,
    'back_right_knee': 8
}

# Neutral positions for standing (in degrees)
NEUTRAL_ANGLES = {
    'front_left_hip': 90,
    'front_left_knee': 90,
    'front_right_hip': 90,
    'front_right_knee': 90,
    'back_left_hip': 90, 
    'back_left_knee': 90,
    'back_right_hip': 90,
    'back_right_knee': 90
}

# Servo angle limits (min, max) in degrees - PREVENT DAMAGE!
ANGLE_LIMITS = {
    'hip': (30, 150),    # Hip servos range
    'knee': (20, 160)    # Knee servos range
}

# Leg dimensions in mm (ADJUST THESE TO YOUR ROBOT!)
LEG_DIMENSIONS = {
    'thigh_length': 80,  # Hip to knee
    'shin_length': 80,   # Knee to foot
    'body_width': 100,   # Distance between hips
    'body_length': 120   # Distance between front and back hips
}

# Walking parameters
WALK_CONFIG = {
    'step_height': 25,
    'step_length': 40,
    'step_speed': 1.0,
    'body_height': 120
}
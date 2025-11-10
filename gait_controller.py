import time
from robot_config import SERVO_MAP, NEUTRAL_ANGLES
from inverse_kinematics import LegIK
from gait_planner import GaitPlanner

class GaitController:
    def __init__(self, servo_driver):
        self.driver = servo_driver
        self.servo_map = SERVO_MAP
        
        # Initialize IK and gait planner
        from robot_config import LEG_DIMENSIONS
        leg_ik = LegIK(
            thigh_length=LEG_DIMENSIONS['thigh_length'],
            shin_length=LEG_DIMENSIONS['shin_length']
        )
        self.planner = GaitPlanner(self, leg_ik)
    
    def set_servo(self, servo_name, angle, move_time=1000):
        """Set individual servo by name"""
        servo_id = self.servo_map[servo_name]
        self.driver.set_angle(servo_id, angle, move_time)
    
    def set_multiple(self, servo_angles, move_time=1000):
        """Set multiple servos simultaneously"""
        for servo_name, angle in servo_angles.items():
            self.set_servo(servo_name, angle, move_time)
    
    def neutral_position(self):
        """Stand using IK calculated position"""
        self.planner.stand()
    
    def walk_forward(self, steps=3, speed=1.0, gait_type='trot'):
        """Walk forward using proper gait planning"""
        duration = steps * 2.0  # 2 seconds per step
        self.planner.move_forward(speed=speed, gait_type=gait_type, duration=duration)
    
    def turn_left(self, angle=30, duration=3.0):
        """Turn left using gait planning"""
        self.planner.turn('left', angle, duration)
    
    def turn_right(self, angle=30, duration=3.0):
        """Turn right using gait planning"""
        self.planner.turn('right', angle, duration)
    
    def sit(self):
        """Sit down"""
        self.planner.sit()
    
    def test_leg_ik(self, leg_name, x, z):
        """Test IK for a specific leg"""
        print(f"Testing {leg_name} at position x={x}, z={z}")
        hip_angle, knee_angle = self.planner.quadruped_ik.calculate_leg_angles(
            leg_name, foot_x=x, foot_z=z
        )
        print(f"Calculated angles: hip={hip_angle:.1f}°, knee={knee_angle:.1f}°")
        
        # Move to the position
        angles = {
            f'{leg_name}_hip': hip_angle,
            f'{leg_name}_knee': knee_angle
        }
        self.set_multiple(angles, 1000)
        return hip_angle, knee_angle
import time
import math
from robot_config import SERVO_MAP, WALK_CONFIG, LEG_DIMENSIONS

class GaitPlanner:
    def __init__(self, gait_controller, leg_ik):
        self.gait = gait_controller
        self.leg_ik = leg_ik
        self.quadruped_ik = None
        
        # Gait parameters
        self.step_length = WALK_CONFIG['step_length']
        self.step_height = WALK_CONFIG['step_height']
        self.step_period = 2.0  # seconds per complete step cycle
        self.body_height = WALK_CONFIG['body_height']
        
        # Initialize quadruped IK
        from inverse_kinematics import QuadrupedIK
        self.quadruped_ik = QuadrupedIK(leg_ik, 
                                      LEG_DIMENSIONS['body_width'], 
                                      LEG_DIMENSIONS['body_length'])
    
    def trot_gait(self, phase):
        """
        Trot gait: diagonal legs move together
        phase: 0 to 1 for complete gait cycle
        """
        leg_phases = {
            'front_left': phase,
            'back_right': phase,
            'front_right': (phase + 0.5) % 1.0,
            'back_left': (phase + 0.5) % 1.0
        }
        return leg_phases
    
    def walk_gait(self, phase):
        """
        Walk gait: legs move in sequence
        """
        leg_phases = {
            'front_right': phase,
            'back_left': (phase + 0.25) % 1.0,
            'front_left': (phase + 0.5) % 1.0,
            'back_right': (phase + 0.75) % 1.0
        }
        return leg_phases
    
    def stand(self):
        """Stand in neutral position using IK"""
        angles = {}
        for leg in ['front_left', 'front_right', 'back_left', 'back_right']:
            # Default standing position: foot directly below hip
            hip_angle, knee_angle = self.quadruped_ik.calculate_leg_angles(
                leg, foot_x=0, foot_z=self.body_height
            )
            angles[f'{leg}_hip'] = hip_angle
            angles[f'{leg}_knee'] = knee_angle
        
        self.gait.set_multiple(angles, 1000)
        print("Standing position set using IK")
    
    def move_forward(self, speed=1.0, gait_type='trot', duration=5.0):
        """
        Move forward with specified gait
        speed: 0.5 slow, 1.0 normal, 2.0 fast
        """
        start_time = time.time()
        step_time = self.step_period / speed
        
        print(f"Starting {gait_type} gait at speed {speed}")
        
        while time.time() - start_time < duration:
            current_time = time.time() - start_time
            phase = (current_time % step_time) / step_time
            
            if gait_type == 'trot':
                leg_phases = self.trot_gait(phase)
            else:
                leg_phases = self.walk_gait(phase)
            
            angles = {}
            for leg, leg_phase in leg_phases.items():
                # Get foot position from trajectory
                x, z = self.leg_ik.foot_trajectory(
                    self.step_length, self.step_height, leg_phase
                )
                
                # Convert to leg angles
                hip_angle, knee_angle = self.quadruped_ik.calculate_leg_angles(
                    leg, foot_x=x, foot_z=z + self.body_height
                )
                angles[f'{leg}_hip'] = hip_angle
                angles[f'{leg}_knee'] = knee_angle
            
            # Execute the movement
            move_time = int(step_time * 500)  # Move in half step time
            self.gait.set_multiple(angles, move_time)
            time.sleep(step_time * 0.1)  # Small delay for smoothness
    
    def turn(self, direction='left', angle=30, duration=3.0):
        """Turn in place"""
        print(f"Turning {direction}")
        
        # Adjust step trajectory for turning
        turn_factor = 1.0 if direction == 'left' else -1.0
        
        start_time = time.time()
        step_time = self.step_period
        
        while time.time() - start_time < duration:
            current_time = time.time() - start_time
            phase = (current_time % step_time) / step_time
            
            leg_phases = self.trot_gait(phase)
            angles = {}
            
            for leg, leg_phase in leg_phases.items():
                # Modified trajectory for turning
                if 'left' in leg:
                    x_mod = turn_factor * 20  # Left legs move differently for turning
                else:
                    x_mod = -turn_factor * 20
                    
                x, z = self.leg_ik.foot_trajectory(
                    self.step_length/2, self.step_height, leg_phase
                )
                
                hip_angle, knee_angle = self.quadruped_ik.calculate_leg_angles(
                    leg, foot_x=x + x_mod, foot_z=z + self.body_height
                )
                angles[f'{leg}_hip'] = hip_angle
                angles[f'{leg}_knee'] = knee_angle
            
            self.gait.set_multiple(angles, 500)
            time.sleep(step_time * 0.1)
    
    def sit(self):
        """Sit down"""
        sit_angles = {}
        for leg in ['front_left', 'front_right', 'back_left', 'back_right']:
            # Sit position: hips neutral, knees bent
            sit_angles[f'{leg}_hip'] = 90
            sit_angles[f'{leg}_knee'] = 30
        
        self.gait.set_multiple(sit_angles, 1500)
        print("Sitting down")
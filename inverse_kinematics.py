import math
import numpy as np

class LegIK:
    def __init__(self, thigh_length=80, shin_length=80):
        """
        Inverse Kinematics for a 2DOF leg
        thigh_length: length from hip to knee (mm)
        shin_length: length from knee to foot (mm)
        """
        self.thigh = thigh_length
        self.shin = shin_length
        self.total_length = thigh_length + shin_length
    
    def calculate_angles(self, x, z):
        """
        Calculate hip and knee angles for desired foot position
        x: forward distance from hip (mm)
        z: vertical distance from hip (mm) - positive down
        
        Returns: (hip_angle, knee_angle) in degrees
        """
        # Ensure the point is reachable
        distance = math.sqrt(x**2 + z**2)
        if distance > self.total_length:
            # Scale to maximum reach
            scale = self.total_length / distance
            x *= scale
            z *= scale
            distance = self.total_length
            print(f"Warning: Target position beyond reach, scaled to ({x:.1f}, {z:.1f})")
        
        if distance < abs(self.thigh - self.shin):
            # Too close, extend fully
            return 0, 0
        
        # Calculate knee angle using law of cosines
        cos_knee = (self.thigh**2 + self.shin**2 - distance**2) / (2 * self.thigh * self.shin)
        cos_knee = max(min(cos_knee, 1), -1)  # Clamp to valid range
        knee_angle = math.acos(cos_knee)
        knee_angle_deg = math.degrees(knee_angle)
        
        # Calculate hip angle
        alpha = math.atan2(z, x)
        beta = math.acos((self.thigh**2 + distance**2 - self.shin**2) / (2 * self.thigh * distance))
        hip_angle = alpha + beta
        hip_angle_deg = math.degrees(hip_angle)
        
        return hip_angle_deg, knee_angle_deg
    
    def foot_trajectory(self, step_length=40, step_height=20, phase=0):
        """
        Generate foot trajectory for walking
        phase: 0 to 1, where 0=start of step, 0.5=middle, 1=end of step
        """
        # Swing phase (foot in air)
        if phase < 0.5:
            x = -step_length/2 + step_length * phase * 2
            # Parabolic trajectory for foot clearance
            z = -step_height * math.sin(phase * math.pi)
        # Stance phase (foot on ground)
        else:
            x = step_length/2 - step_length * (phase - 0.5) * 2
            z = 0  # On ground
        
        return x, z

class QuadrupedIK:
    def __init__(self, leg_ik, body_width=100, body_length=120):
        self.leg_ik = leg_ik
        self.body_width = body_width
        self.body_length = body_length
    
    def calculate_leg_angles(self, leg_position, foot_x=0, foot_z=120, body_roll=0, body_pitch=0):
        """
        Calculate angles for all servos in one leg
        leg_position: 'front_left', 'front_right', 'back_left', 'back_right'
        foot_x, foot_z: desired foot position relative to hip
        body_roll, body_pitch: body orientation in degrees
        """
        # Convert body orientation to radians
        roll_rad = math.radians(body_roll)
        pitch_rad = math.radians(body_pitch)
        
        # Adjust foot position based on body orientation (simplified)
        adjusted_x = foot_x
        adjusted_z = foot_z
        
        # Calculate leg angles
        hip_angle, knee_angle = self.leg_ik.calculate_angles(adjusted_x, adjusted_z)
        
        # Adjust for leg position
        if 'front' in leg_position:
            hip_angle += body_pitch
        else:
            hip_angle -= body_pitch
            
        if 'left' in leg_position:
            hip_angle += body_roll
        else:
            hip_angle -= body_roll
        
        return hip_angle, knee_angle
#!/usr/bin/env python3
import time
import sys
from lx16a_driver import LX16ADriver
from gait_controller import GaitController

class QuadrupedRobot:
    def __init__(self, port='/dev/ttyUSB0'):
        try:
            self.driver = LX16ADriver(port)
            self.gait = GaitController(self.driver)
            print("Quadruped robot initialized successfully!")
        except Exception as e:
            print(f"Failed to initialize robot: {e}")
            sys.exit(1)
    
    def test_servos(self):
        """Test each servo individually"""
        print("Testing all servos...")
        
        # Test each servo through its range
        test_angles = [60, 90, 120, 90]  # Test sequence
        
        for servo_name in self.gait.servo_map.keys():
            print(f"Testing {servo_name}")
            for angle in test_angles:
                self.gait.set_servo(servo_name, angle, 500)
                time.sleep(0.5)
        
        print("Servo test completed!")
    
    def test_ik(self):
        """Test inverse kinematics with manual positions"""
        print("\n=== Inverse Kinematics Test ===")
        print("Testing front left leg with different positions:")
        
        test_positions = [
            (0, 120),   # Straight down
            (30, 110),  # Forward
            (-30, 110), # Backward
            (0, 80),    # Raised
        ]
        
        for x, z in test_positions:
            print(f"\nPosition: x={x}, z={z}")
            input("Press Enter to move...")
            self.gait.test_leg_ik('front_left', x, z)
            time.sleep(1)
    
    def interactive_control(self):
        """Enhanced interactive control with IK"""
        print("\n" + "="*50)
        print("QUADRUPED ROBOT CONTROL WITH INVERSE KINEMATICS")
        print("="*50)
        print("Commands:")
        print("  n - Stand (neutral position)")
        print("  w - Walk forward")
        print("  s - Sit down")
        print("  l - Turn left")
        print("  r - Turn right")
        print("  t - Test servos")
        print("  i - Test inverse kinematics")
        print("  q - Quit")
        print("="*50)
        
        self.gait.neutral_position()
        
        while True:
            cmd = input("\nEnter command: ").strip().lower()
            
            if cmd == 'q':
                break
            elif cmd == 'n':
                self.gait.neutral_position()
            elif cmd == 'w':
                steps = input("How many steps? (default 3): ").strip()
                speed = input("Speed (0.5-2.0, default 1.0): ").strip()
                gait = input("Gait (trot/walk, default trot): ").strip()
                
                steps = int(steps) if steps.isdigit() else 3
                speed = float(speed) if speed.replace('.', '').isdigit() else 1.0
                gait = gait if gait in ['trot', 'walk'] else 'trot'
                
                self.gait.walk_forward(steps, speed, gait)
            elif cmd == 's':
                self.gait.sit()
            elif cmd == 'l':
                angle = input("Turn angle (default 30): ").strip()
                angle = int(angle) if angle.isdigit() else 30
                self.gait.turn_left(angle)
            elif cmd == 'r':
                angle = input("Turn angle (default 30): ").strip()
                angle = int(angle) if angle.isdigit() else 30
                self.gait.turn_right(angle)
            elif cmd == 't':
                self.test_servos()
            elif cmd == 'i':
                self.test_ik()
            else:
                print("Invalid command. Please try again.")
    
    def shutdown(self):
        """Safe shutdown"""
        print("\nShutting down robot...")
        self.gait.neutral_position()
        time.sleep(1)
        self.driver.close()
        print("Robot shutdown complete.")

def main():
    # Check for custom port
    port = '/dev/ttyUSB0'
    if len(sys.argv) > 1:
        port = sys.argv[1]
    
    robot = QuadrupedRobot(port)
    
    try:
        robot.interactive_control()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Error during operation: {e}")
    finally:
        robot.shutdown()

if __name__ == "__main__":
    main()
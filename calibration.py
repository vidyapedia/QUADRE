#!/usr/bin/env python3
# Servo Calibration Tool
import time
from lx16a_driver import LX16ADriver
from robot_config import SERVO_MAP

def calibrate_servo(driver, servo_name, servo_id):
    print(f"\n=== Calibrating {servo_name} (ID: {servo_id}) ===")
    print("Commands: angle (0-240), u=+10°, d=-10°, n=neutral, q=quit calibration")
    
    current_angle = 90
    
    while True:
        driver.set_angle(servo_id, current_angle, 500)
        print(f"Current angle: {current_angle}°")
        
        cmd = input("Enter command: ").strip().lower()
        
        if cmd == 'q':
            break
        elif cmd == 'n':
            current_angle = 90
        elif cmd == 'u':
            current_angle = min(240, current_angle + 10)
        elif cmd == 'd':
            current_angle = max(0, current_angle - 10)
        elif cmd.isdigit():
            angle = int(cmd)
            if 0 <= angle <= 240:
                current_angle = angle
            else:
                print("Angle must be between 0-240")
        else:
            print("Invalid command")
    
    print(f"Final calibration for {servo_name}: {current_angle}°")
    return current_angle

def find_limits(driver, servo_id, servo_name):
    """Find the physical limits of a servo"""
    print(f"\nFinding limits for {servo_name}...")
    
    # Start from neutral
    driver.set_angle(servo_id, 90, 1000)
    time.sleep(1)
    
    # Find lower limit
    print("Finding lower limit...")
    angle = 90
    while angle > 0:
        driver.set_angle(servo_id, angle, 200)
        time.sleep(0.2)
        response = input(f"Angle: {angle}° - OK? (y/n): ").strip().lower()
        if response == 'n':
            break
        angle -= 5
    
    lower_limit = angle + 5
    
    # Return to neutral
    driver.set_angle(servo_id, 90, 1000)
    time.sleep(1)
    
    # Find upper limit
    print("Finding upper limit...")
    angle = 90
    while angle < 240:
        driver.set_angle(servo_id, angle, 200)
        time.sleep(0.2)
        response = input(f"Angle: {angle}° - OK? (y/n): ").strip().lower()
        if response == 'n':
            break
        angle += 5
    
    upper_limit = angle - 5
    
    print(f"{servo_name} limits: {lower_limit}° to {upper_limit}°")
    return lower_limit, upper_limit

if __name__ == "__main__":
    driver = LX16ADriver()
    
    print("=== QUADRUPED ROBOT SERVO CALIBRATION ===")
    print("1. Manual angle calibration")
    print("2. Find servo limits")
    
    choice = input("Select option (1 or 2): ").strip()
    
    if choice == '1':
        for servo_name, servo_id in SERVO_MAP.items():
            calibrate_servo(driver, servo_name, servo_id)
    elif choice == '2':
        limits = {}
        for servo_name, servo_id in SERVO_MAP.items():
            lower, upper = find_limits(driver, servo_id, servo_name)
            limits[servo_name] = (lower, upper)
        
        print("\n=== SERVO LIMITS SUMMARY ===")
        for servo_name, (lower, upper) in limits.items():
            print(f"{servo_name}: {lower}° to {upper}°")
    
    # Return to neutral
    print("\nReturning all servos to neutral...")
    for servo_id in SERVO_MAP.values():
        driver.set_angle(servo_id, 90, 1000)
    
    driver.close()
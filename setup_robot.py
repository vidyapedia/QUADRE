#!/usr/bin/env python3
# Initial Robot Setup Script
import os
import subprocess

def run_command(cmd):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def main():
    print("=== Quadruped Robot Setup ===")
    
    # Check Python version
    print("Checking Python version...")
    code, stdout, stderr = run_command("python3 --version")
    if code == 0:
        print(f"Python version: {stdout.strip()}")
    else:
        print("Python3 not found! Please install Python 3.7 or newer")
        return
    
    # Install requirements
    print("Installing requirements...")
    code, stdout, stderr = run_command("pip3 install -r requirements.txt")
    if code == 0:
        print("Requirements installed successfully")
    else:
        print(f"Error installing requirements: {stderr}")
    
    # Check serial port
    print("Checking serial ports...")
    code, stdout, stderr = run_command("ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null")
    if code == 0:
        ports = stdout.strip().split('\n')
        print(f"Available serial ports: {ports}")
    else:
        print("No serial ports found. Make sure BusLinker is connected.")
    
    # Set permissions for serial port
    print("Setting serial port permissions...")
    run_command("sudo usermod -a -G dialout $USER")
    
    print("\nSetup completed!")
    print("Next steps:")
    print("1. Run: python calibration.py")
    print("2. Adjust LEG_DIMENSIONS in robot_config.py for your robot")
    print("3. Run: python main.py")
    print("\nNote: You may need to reboot for serial port permissions to take effect")

if __name__ == "__main__":
    main()
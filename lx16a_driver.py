import serial
import time
import struct

class LX16ADriver:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.connect()
    
    def connect(self):
        """Initialize serial connection to BusLinker"""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)
            print(f"Connected to BusLinker on {self.port}")
        except Exception as e:
            print(f"Connection error: {e}")
            raise
    
    def send_command(self, servo_id, command, data=[]):
        """Send command to LX-16A servo"""
        packet = [0x55, 0x55, servo_id, len(data) + 3, command] + data
        checksum = sum(packet[2:]) & 0xFF
        packet.append(checksum)
        
        try:
            self.ser.write(bytearray(packet))
            time.sleep(0.01)
        except Exception as e:
            print(f"Command error to servo {servo_id}: {e}")
    
    def set_position(self, servo_id, position, move_time=1000):
        """Set servo position (0-1000 range)"""
        position = max(0, min(1000, position))
        pos_low = position & 0xFF
        pos_high = (position >> 8) & 0xFF
        time_low = move_time & 0xFF
        time_high = (move_time >> 8) & 0xFF
        
        self.send_command(servo_id, 0x03, [time_low, time_high, pos_low, pos_high])
    
    def set_angle(self, servo_id, angle, move_time=1000):
        """Set servo angle in degrees (0-240)"""
        position = int((angle / 240.0) * 1000)
        self.set_position(servo_id, position, move_time)
    
    def servo_off(self, servo_id):
        """Turn off servo torque"""
        self.send_command(servo_id, 0x14)
    
    def close(self):
        """Close serial connection"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Closed BusLinker connection")
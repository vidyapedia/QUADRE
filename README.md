# Quadruped Robot Control Stack (Python)

#YOUTUBE VIDEO LINK:https://youtu.be/TlbMrHZhGbI

A from-scratch Python control stack for a custom quadruped robot, including **servo calibration**, **inverse kinematics**, **gait planning**, and **gait execution** using **LX-16A serial bus servos**.

This repo is designed to be practical and “hardware-first”: calibrate servos, define robot geometry, generate foot trajectories, solve IK, and stream joint commands to the robot.

---

## What this project does

- **Servo setup & calibration** (IDs, offsets, home positions)
- **Inverse Kinematics (IK)** per leg (foot position → joint angles)
- **Gait planning** (foot trajectories, phase offsets)
- **Gait control** (timed stepping, sequencing, smooth transitions)
- **Hardware driver** for LX-16A servos (serial bus communication)
- Central entrypoint to run the robot with a configurable setup

---

## Hardware (my build)

> Update this section to match your exact build.

- Controller: Raspberry Pi (or any Linux computer)
- Actuators: LX-16A serial bus servos
- Serial interface: USB-to-TTL / BusLinker (or equivalent)
- Power: external supply sized for servo stall currents (recommended)
- Robot: 4 legs, each with joint configuration defined in `robot_config.py`

---

## Repository structure

- `main.py`  
  Main entrypoint to run the robot / gait loop.

- `setup_robot.py`  
  One-time or occasional setup (e.g., servo discovery, ID assignment, sanity checks).

- `calibration.py`  
  Calibration routines: set servo centers/home angles, offsets, limits.

- `robot_config.py`  
  Robot geometry + servo mapping (leg dimensions, servo IDs, joint limits, home pose).

- `inverse_kinematics.py`  
  IK functions: foot position → joint angles.

- `gait_planner.py`  
  Defines gait parameters and generates desired foot trajectories over time.

- `gait_controller.py`  
  Consumes planned trajectories, calls IK, and sends commands to servos.

- `lx16a_driver.py`  
  Low-level driver for LX-16A communication (serial protocol, read/write commands).

- `requirements.txt`  
  Python dependencies.

---

## Quick start

### 1) Clone and install dependencies
```bash
git clone <YOUR_REPO_URL>
cd <YOUR_REPO_FOLDER>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

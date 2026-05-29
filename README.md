# 🛰️ Indigenous Tactical Radar Suite & Electronic Warfare Simulator

An advanced tactical air-defense mission control simulation built to model phased-array radar mechanics and Electronic Counter-Counter Measures (ECCM) in high-resource computing environments. This indigenous simulation is designed for standalone prototyping and validation of anti-jamming algorithms.

## 👥 Developer Profile
- **Name:** Sk Soyeb Akhtar  
- **Department:** Mechanical Engineering, Aliah University  
- **Target Application:** DRDO R&D Signal Intelligence & Cyber Defence Platforms  

---

## ⚡ Core Operational Architecture

The software architecture operates in two highly critical military-grade routines powered by high-speed **NumPy Vectorized Arrays** to ensure real-time 60 FPS performance without requiring dedicated hardware graphics processing.

### 🔴 Routine 1: Phased-Array Airspace Surveillance
- **Kinematic Threat Tracker:** Tracks multiple adversarial targets (missiles, UAVs, stealth jets) simultaneously using continuous coordinate geometric matrices.
- **RCS (Radar Cross Section) Calculation:** Simulates target reflectivity values ($\sigma$ in $m^2$) to model how effectively the radar waves bounce off different aircraft structures based on the Radar Range Equation:
  
  $$P_r = \frac{P_t \cdot G^2 \cdot \lambda^2 \cdot \sigma}{(4\pi)^3 \cdot R^4}$$

### 🟢 Routine 2: Electronic Counter-Counter Measures (ECCM)
- **Hostile Jamming Attack Simulation:** Generates a chaotic, high-frequency red noise waveform representing aggressive adversarial electromagnetic interference trying to blind the communication network.
- **Autonomous Frequency Hopping:** Executes microsecond-level matrix transformations to establish a secure, clean co-phase green sine wave, successfully filtering out the noise and keeping the air defense dashboard online.

---

## 📊 Live Hardware Telemetry
The core framework includes a continuous background performance pipeline that monitors processing load indices and emulates thermal behavior under heavy cryptographic sorting and frequency shifting, displaying real-time metrics on a rolling history matrix graph.

## 🛠️ Execution Instructions
To launch this mission dashboard on a local workstation, ensure you have Python 3 and the required vectorized compute libraries installed:

```bash
pip install opencv-python numpy
python drdo_mission_control.py

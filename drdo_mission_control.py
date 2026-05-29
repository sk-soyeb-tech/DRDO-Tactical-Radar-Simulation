import cv2
import numpy as np
import time
import math
import random

class DRDOMissionControlApp:
    def __init__(self):
        # Screen Dimensions Matrix
        self.width, self.height = 1024, 768
        self.fps = 0.0
        self.last_time = time.time()

        # Mission Operational States
        self.system_status = "SCANNING TACTICAL AIRSPACE"
        self.hud_color = (0, 255, 0)       # Tactical Defensive Green
        self.ew_mode = 1                  # 1: Phased Radar Sweep, 2: ECCM Jamming Overrides
        self.processing_load = 0.12        # Initial algorithmic core load representation

        # Tactical Target Profiles (Kinematic Matrix Arrays)
        self.targets = []
        self.radar_angle = 0.0
        self.generate_live_threats()

        # Telemetry Cache Buffer (Pre-allocated NumPy array for fast operations)
        self.core_temp = 39.5
        self.temp_buffer = np.full(60, 39.5, dtype=np.float32)

        # Pre-allocated 1D spatial matrix for high-speed vectorized waveform rendering
        self.x_axis_vector = np.arange(548, dtype=np.int32)

    def generate_live_threats(self):
        """Generates mock dynamic threat targets within the virtual processing matrix"""
        self.targets = []
        for i in range(3):
            self.targets.append({
                "id": f"THREAT_0{i+1}",
                "x": float(random.randint(240, 460)),
                "y": float(random.randint(220, 500)),
                "speed_x": random.uniform(-1.4, 1.4),
                "speed_y": random.uniform(-1.4, 1.4),
                "rCS": random.uniform(0.15, 2.5)   # Radar Cross Section in square meters
            })

    def draw_tactical_hud(self, canvas, current_routine):
        """Renders an advanced, crystal-clear glass telemetry header"""
        # Top banner background block
        cv2.rectangle(canvas, (0, 0), (self.width, 60), (10, 10, 12), -1)
        # Tactical separating boundary orange line
        cv2.line(canvas, (0, 60), (self.width, 60), (255, 120, 0), 1) 
        
        # Microsecond precision delta time computation for real-time FPS
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        raw_fps = 1.0 / dt if dt > 0 else 60.0
        self.fps = 0.9 * self.fps + 0.1 * raw_fps

        # Top Overlay text indicators
        cv2.putText(canvas, f"INDIGENOUS DEFENCE SYSTEM // {current_routine}", (25, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(canvas, f"COMPUTE ENGINE: NUMPY VECTORIZED | PROCESSOR: INTEL i7 CORE | SYSTEM FPS: {self.fps:.1f}", (self.width - 775, 36), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.68, (0, 255, 0), 1, cv2.LINE_AA)

    def draw_thermal_telemetry(self, canvas):
        """Vectorized system thermal tracker utilizing advanced roll processing shifts"""
        target_temp = 39.5 + (self.processing_load * 26.5)
        self.core_temp = 0.94 * self.core_temp + 0.06 * target_temp
        
        # Vectorized memory block shift operation (Replaces slow python pop/append execution threads)
        self.temp_buffer = np.roll(self.temp_buffer, -1)
        self.temp_buffer[-1] = self.core_temp

        # Base boundary card overlay for telemetry graph
        gx, gy = self.width - 260, self.height - 190
        cv2.rectangle(canvas, (gx, gy), (gx + 240, gy + 170), (12, 12, 15), -1)
        cv2.rectangle(canvas, (gx, gy), (gx + 240, gy + 170), (45, 45, 50), 1)
        
        # Telemetry matrix metrics text strings
        cv2.putText(canvas, f"ALGO LOAD INDICES: {int(self.processing_load * 100)}%", (gx + 15, gy + 25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(canvas, f"CORE TEMPERATURE: {self.core_temp:.1f} C", (gx + 15, gy + 48), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Drawing dynamic performance history telemetry plot
        for i in range(len(self.temp_buffer) - 1):
            x1 = int(gx + 15 + (i * 3.5))
            y1 = int(gy + 145 - (self.temp_buffer[i] - 35) * 4)
            x2 = int(gx + 15 + ((i + 1) * 3.5))
            y2 = int(gy + 145 - (self.temp_buffer[i+1] - 35) * 4)
            y1, y2 = np.clip([y1, y2], gy + 65, gy + 160)
            
            graph_color = (0, 255, 0) if self.ew_mode == 1 else (0, 0, 255)
            cv2.line(canvas, (x1, y1), (x2, y2), graph_color, 1, cv2.LINE_AA)

    def launch_mission_suite(self):
        """Initializes standalone graphical environment and triggers tactical computational pipelines"""
        window_matrix = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        cv2.namedWindow("DRDO TACTICAL RADAR MISSION DASHBOARD")

        while True:
            canvas = window_matrix.copy()
            
            # Rendering Industrial structural network grid backgrounds
            for i in range(0, self.width, 60):
                cv2.line(canvas, (i, 60), (i, self.height), (14, 14, 18), 1)
            for j in range(60, self.height, 60):
                cv2.line(canvas, (0, j), (self.width, j), (14, 14, 18), 1)

            # =================================================================
            # 📡 ROUTINE 1: PHASED-ARRAY SYSTEM SEARCH & RADAR MONITOR
            # =================================================================
            if self.ew_mode == 1:
                self.draw_tactical_hud(canvas, "PHASED-ARRAY RADAR AIRSPACE SEARCH")
                self.processing_load = 0.14
                
                rx, ry, radius = 350, 360, 210
                cv2.circle(canvas, (rx, ry), radius, (10, 28, 10), -1)
                cv2.circle(canvas, (rx, ry), radius, (0, 180, 0), 1, cv2.LINE_AA)
                cv2.circle(canvas, (rx, ry), radius - 70, (0, 90, 0), 1, cv2.LINE_AA)
                cv2.circle(canvas, (rx, ry), radius - 140, (0, 90, 0), 1, cv2.LINE_AA)
                
                # Trigonometric angular shift for Phased radar sweeping beam simulation
                self.radar_angle += 0.03
                sweep_x = int(rx + radius * math.cos(self.radar_angle))
                sweep_y = int(ry + radius * math.sin(self.radar_angle))
                cv2.line(canvas, (rx, ry), (sweep_x, sweep_y), (0, 255, 60), 2, cv2.LINE_AA)

                # Process Kinetic Threat Tracker Node Array
                for target in self.targets:
                    target["x"] += target["speed_x"]
                    target["y"] += target["speed_y"]
                    
                    # Boundary collision checking via Euclidean distance geometry calculations
                    dist_vector = math.sqrt((target["x"] - rx)**2 + (target["y"] - ry)**2)
                    if dist_vector > (radius - 15):
                        target["speed_x"] *= -1
                        target["speed_y"] *= -1

                    tx, ty = int(target["x"]), int(target["y"])
                    # Anti-aliased target square tracking markers
                    cv2.rectangle(canvas, (tx - 8, ty - 8), (tx + 8, ty + 8), (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.putText(canvas, f"{target['id']} // RCS: {target['rCS']:.2f} m^2", (tx - 50, ty - 16), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.55, (240, 240, 245), 1, cv2.LINE_AA)

            # =================================================================
            # ⚡ ROUTINE 2: ELECTRONIC WARFARE SPECTRA OVERRIDES (ECCM ACTIVE)
            # =================================================================
            elif self.ew_mode == 2:
                self.draw_tactical_hud(canvas, "ELECTRONIC COUNTER-COUNTER MEASURES (ECCM)")
                self.processing_load = 0.68  # Emulating algorithm sorting stream calculation weights
                
                ox, oy = 60, 220
                cv2.putText(canvas, "ADVERSARIAL ELECTRONIC JAMMING SPECTRUM ATTACK (NOISE MATRIX):", (ox, oy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 1, cv2.LINE_AA)
                
                # --- HIGH-SPEED VECTORIZED NUMPY MATRIX FREQUENCY COMPUTATION ---
                # Compiling 548 waveform coordinate transformations in a single microsecond clock cycle
                t_step = time.time() * 24.0
                hostile_y_vector = (oy + 60 + np.sin(self.x_axis_vector * 0.12 + t_step) * 40 + np.sin(self.x_axis_vector * 0.35) * 6).astype(np.int32)
                
                # Dynamic matrix shape stacking mapping vectors
                points_hostile = np.column_stack((ox + self.x_axis_vector, hostile_y_vector))
                cv2.polylines(canvas, [points_hostile], False, (0, 0, 255), 1, cv2.LINE_AA)

                # Real-Time Filtered Clean ECCM Wave Rendering Output
                oy_eccm = 420
                cv2.putText(canvas, "AUTONOMOUS RE-ROUTED INDIGENOUS ANTI-JAMMING SECURE SPECTRUM:", (ox, oy_eccm - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 1, cv2.LINE_AA)
                
                clean_t = time.time() * 8.0
                clean_y_vector = (oy_eccm + 60 + np.sin(self.x_axis_vector * 0.04 + clean_t) * 32).astype(np.int32)
                
                points_clean = np.column_stack((ox + self.x_axis_vector, clean_y_vector))
                cv2.polylines(canvas, [points_clean], False, (0, 255, 0), 2, cv2.LINE_AA)

            # --- MISSION STATUS PANEL LOGGER BOX ---
            cv2.rectangle(canvas, (30, self.height - 140), (680, self.height - 40), (10, 10, 12), -1)
            cv2.rectangle(canvas, (30, self.height - 140), (680, self.height - 40), (50, 50, 55), 1)
            cv2.putText(canvas, f"TACTICAL INFRASTRUCTURE ONLINE // SYSTEM REGISTERS: ENFORCED", (45, self.height - 105), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (240, 240, 245), 1, cv2.LINE_AA)
            cv2.putText(canvas, f"THREAT METRICS EVALUATION PROTECTION STATE: [ {self.system_status} ]", (45, self.height - 65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, self.hud_color, 1, cv2.LINE_AA)

            # Manual Operation User Interface Menu Map
            cv2.rectangle(canvas, (self.width - 260, self.height - 310), (self.width - 20, self.height - 210), (10, 10, 12), -1)
            cv2.putText(canvas, " OPERATIONAL MENU:", (self.width - 245, self.height - 285), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (240, 240, 245), 1, cv2.LINE_AA)
            cv2.putText(canvas, "[Key 1] : Phased Radar Search", (self.width - 245, self.height - 260), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(canvas, "[Key 2] : Inject Electronic Warfare", (self.width - 245, self.height - 235), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 255), 1, cv2.LINE_AA)

            # Render hardware tracking statistics
            self.draw_thermal_telemetry(canvas)

            # Update master application framework display frame
            cv2.imshow("DRDO TACTICAL RADAR MISSION DASHBOARD", canvas)
            
            key = cv2.waitKey(15) & 0xFF
            if key == ord('1'):
                self.ew_mode = 1
                self.system_status = "SCANNING TACTICAL AIRSPACE"
                self.hud_color = (0, 255, 0)
                self.generate_live_threats()
            elif key == ord('2'):
                self.ew_mode = 2
                self.system_status = "⚠️ JAMMING INTERFERENCE IMMINENT // INITIALIZING ECCM FILTER REGISTERS"
                self.hud_color = (0, 0, 255)
            elif key == ord('q'): 
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = DRDOMissionControlApp()
    app.launch_mission_suite()
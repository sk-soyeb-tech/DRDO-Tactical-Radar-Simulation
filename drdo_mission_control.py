import cv2
import numpy as np
import time
import math
import random

class DRDOMissionControlApp:
    def __init__(self):
        # Layout Framework Matrix (Fixed Resolution Match)
        self.width, self.height = 1280, 720
        self.fps = 0.0
        self.last_time = time.time()

        # Operational Control Coordinates
        self.radar_angle = 0.0
        self.targets = []
        self.detected_targets = {}  # Tracks continuous unique rows dynamically
        self.init_dynamic_threat_environment()

        # Telemetry Cache Buffers
        self.system_load_buffer = np.full(60, 14.0, dtype=np.float32)
        self.core_temp_buffer = np.full(60, 43.4, dtype=np.float32)
        
        # High-speed Vectorized NumPy wave array
        self.ew_x_vector = np.arange(550, dtype=np.int32)
        self.jamming_active = False

    def init_dynamic_threat_environment(self):
        """Generates raw kinematic vectors securely locked inside the radar center boundary"""
        rx, ry, r_max = 320, 535, 125  # Geometric bounds of the radar circle
        
        # Defining 5 unique system tracking blocks
        target_specs = [
            {"id": "TGT-01", "type": "MISSILE VECTOR"},
            {"id": "TGT-02", "type": "LOW-ALT UAV"},
            {"id": "TGT-03", "type": "STEALTH THREAT"},
            {"id": "TGT-04", "type": "FIGHTER JET"},
            {"id": "TGT-05", "type": "DECOY SIGNALS"}
        ]
        
        self.targets = []
        for spec in target_specs:
            random_radius = random.uniform(20, r_max - 22)
            random_angle = random.uniform(0, 2 * math.pi)
            
            self.targets.append({
                "id": spec["id"],
                "type": spec["type"],
                "radius": random_radius,
                "angle": random_angle,
                "radial_speed": random.uniform(0.003, 0.009),
                "base_velocity": random.uniform(220, 1100),
                "rcs_val": random.uniform(0.05, 2.2)
            })

    def draw_structured_panel(self, canvas, title, pt1, pt2, accent_color=(255, 120, 0)):
        """Renders isolated operational bounding panels to eliminate string overlap"""
        cv2.rectangle(canvas, pt1, pt2, (10, 12, 16), -1)
        cv2.rectangle(canvas, pt1, pt2, (45, 48, 55), 1)
        cv2.rectangle(canvas, pt1, (pt2[0], pt1[1] + 28), (20, 24, 32), -1)
        cv2.line(canvas, (pt1[0], pt1[1] + 28), (pt2[0], pt1[1] + 28), accent_color, 1)
        cv2.putText(canvas, title, (pt1[0] + 12, pt1[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (240, 240, 245), 1, cv2.LINE_AA)

    def update_hardware_telemetry(self):
        """Updates internal telemetry buffers using vectorized microshifts"""
        base_load = 68.0 if self.jamming_active else 14.0
        base_temp = 57.5 if self.jamming_active else 43.4
        
        current_load = np.clip(base_load + random.uniform(-3.0, 3.0), 0, 100)
        current_temp = np.clip(base_temp + random.uniform(-0.5, 0.5), 30, 90)

        self.system_load_buffer = np.roll(self.system_load_buffer, -1)
        self.core_temp_buffer = np.roll(self.core_temp_buffer, -1)
        
        self.system_load_buffer[-1] = current_load
        self.core_temp_buffer[-1] = current_temp

    def launch_mission_suite(self):
        """Launches the unified multi-panel DRDO dashboard interface"""
        cv2.namedWindow("DRDO TACTICAL RADAR MISSION DASHBOARD", cv2.WINDOW_AUTOSIZE)
        
        while True:
            canvas = np.full((self.height, self.width, 3), 5, dtype=np.uint8)
            
            # --- TOP LEVEL TELEMETRY HEADER ---
            current_time = time.time()
            dt = current_time - self.last_time
            self.last_time = current_time
            self.fps = 0.9 * self.fps + 0.1 * (1.0 / dt if dt > 0 else 60.0)
            
            cv2.rectangle(canvas, (0, 0), (self.width, 40), (12, 14, 18), -1)
            cv2.putText(canvas, "DRDO TACTICAL MISSION CONTROL ENGINE", (25, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(canvas, f"HARDWARE LOG: INTEL i7 CORE | SYSTEM FPS: {self.fps:.1f}", (self.width - 450, 25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.line(canvas, (0, 40), (self.width, 40), (0, 255, 0), 1)

            # =================================================================
            # PANEL 2: PHASED-ARRAY RADAR SURVEILLANCE SCOPE (LIGHT BLUE COLOR)
            # =================================================================
            # Light Blue / Cyan Palette definitions BGR format
            light_blue_panel = (255, 200, 60)
            light_blue_grid = (200, 140, 20)
            
            self.draw_structured_panel(canvas, "INDIGENOUS RADAR LIVE SURVEILLANCE MAP", (20, 380), (620, 670), light_blue_panel)
            
            rx, ry, r_max = 320, 535, 125
            cv2.circle(canvas, (rx, ry), r_max, (24, 18, 5), -1) # Dark Blue tint background
            for r_step in [r_max, int(r_max * 0.66), int(r_max * 0.33)]:
                cv2.circle(canvas, (rx, ry), r_step, light_blue_grid, 1, cv2.LINE_AA)
            
            # Sweeping beam tracking updates using Light Blue vector line
            self.radar_angle = (self.radar_angle + 0.04) % (2 * math.pi)
            sweep_x = int(rx + r_max * math.cos(self.radar_angle))
            sweep_y = int(ry + r_max * math.sin(self.radar_angle))
            cv2.line(canvas, (rx, ry), (sweep_x, sweep_y), light_blue_panel, 2, cv2.LINE_AA)

            # Process target kinematics ONLY if Jammer Network Attack is Active (Key 2)
            if self.jamming_active:
                for tgt in self.targets:
                    tgt['angle'] = (tgt['angle'] + tgt['radial_speed']) % (2 * math.pi)
                    tx = int(rx + tgt['radius'] * math.cos(tgt['angle']))
                    ty = int(ry + tgt['radius'] * math.sin(tgt['angle']))
                    
                    live_range = int(tgt['radius'] * 5.5) + random.randint(-1, 1)
                    live_vel = int(tgt['base_velocity'] + random.uniform(-4.0, 4.0))
                    
                    angle_diff = abs(self.radar_angle - tgt['angle'])
                    if angle_diff < 0.12:  
                        self.detected_targets[tgt['id']] = {
                            "type": tgt['type'],
                            "range": live_range,
                            "velocity": live_vel,
                            "rcs": tgt['rcs_val']
                        }
                    
                    # Render red threat blips inside the scope
                    cv2.rectangle(canvas, (tx - 5, ty - 5), (tx + 5, ty + 5), (0, 0, 255), -1)
                    cv2.putText(canvas, f"{tgt['id']}", (tx + 8, ty + 4), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
            else:
                # Clear logged entries when jammer network turns off
                self.detected_targets.clear()

            # =================================================================
            # PANEL 1: MISSION BRIEFING & PERMANENT DYNAMIC LOGS (TOP LEFT)
            # =================================================================
            self.draw_structured_panel(canvas, "MISSION BRIEFING & TARGET VECTORS", (20, 60), (620, 360))
            
            cv2.putText(canvas, "MISSION BRIEFING: ACTIVE SURVEILLANCE OF STRATEGIC AIRSPACE SECTOR 4.", (35, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 205), 1, cv2.LINE_AA)
            cv2.putText(canvas, f"CURRENT THREATS: ({len(self.detected_targets)} ACTIVE TARGET TRACKS REGISTERED)", (35, 132), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 255), 1, cv2.LINE_AA)
            
            # Print row logs (Will remain empty during standby state)
            start_y = 165
            for idx, (t_id, metrics) in enumerate(sorted(self.detected_targets.items())):
                log_line = f"| {t_id}: {metrics['type']} | RANGE: {metrics['range']}KM | VEL: {metrics['velocity']}M/S | RCS: {metrics['rcs']:.2f}M2"
                cv2.putText(canvas, log_line, (32, start_y + (idx * 24)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.52, (240, 240, 245), 1, cv2.LINE_AA)

            # =================================================================
            # PANEL 3: LIVE HARDWARE TELEMETRY GRAPH (BOTTOM CENTER BLOCK)
            # =================================================================
            self.draw_structured_panel(canvas, "LIVE HARDWARE TELEMETRY LOGS", (640, 380), (1260, 670))
            self.update_hardware_telemetry()
            
            gx, gy = 660, 430
            cv2.putText(canvas, f"SYSTEM LOAD: {self.system_load_buffer[-1]:.1f}%", (gx, gy), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (0, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(canvas, f"CORE TEMPERATURE: {self.core_temp_buffer[-1]:.1f} C", (gx + 260, gy), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (255, 255, 255), 1, cv2.LINE_AA)
            
            cv2.line(canvas, (gx, gy + 190), (gx + 540, gy + 190), (150, 150, 150), 1) 
            cv2.line(canvas, (gx, gy + 30), (gx, gy + 190), (150, 150, 150), 1) 
            cv2.putText(canvas, "TIME (S)", (gx + 240, gy + 210), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (120, 120, 125), 1, cv2.LINE_AA)
            
            for k in range(len(self.system_load_buffer) - 1):
                x1_val = int(gx + (k * 9.0))
                y1_val = int(gy + 190 - (self.system_load_buffer[k] * 1.5))
                x2_val = int(gx + ((k + 1) * 9.0))
                y2_val = int(gy + 190 - (self.system_load_buffer[k+1] * 1.5))
                cv2.line(canvas, (x1_val, y1_val), (x2_val, y2_val), (255, 200, 0), 1, cv2.LINE_AA)

            # =================================================================
            # PANEL 4: ELECTRONIC COUNTER-COUNTER MEASURES (EW SPECTRUM RIGHT)
            # =================================================================
            self.draw_structured_panel(canvas, "ELECTRONIC COUNTER-COUNTER MEASURES (ECCM)", (640, 60), (1260, 360), (0, 120, 255))
            
            wave_start_x = 680
            if self.jamming_active:
                cv2.putText(canvas, "RED WAVE: HOSTILE JAMMING ATTACK VECTOR (ACTIVE INTERFERENCE)", (660, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 255), 1, cv2.LINE_AA)
                t_wave = time.time() * 25.0
                hostile_y = (170 + np.sin(self.ew_x_vector * 0.15 + t_wave) * 30 + np.sin(self.ew_x_vector * 0.4) * 8).astype(np.int32)
                pts_hostile = np.column_stack((wave_start_x + self.ew_x_vector, hostile_y))
                cv2.polylines(canvas, [pts_hostile], False, (0, 0, 255), 1, cv2.LINE_AA)
            else:
                cv2.putText(canvas, "RED WAVE: SPECTRUM STATUS CLEAR (NO ACTIVE JAMMING IDENTIFIED)", (660, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (100, 100, 105), 1, cv2.LINE_AA)
                cv2.line(canvas, (wave_start_x, 170), (wave_start_x + 550, 170), (40, 40, 45), 1, cv2.LINE_AA)

            cv2.putText(canvas, "GREEN WAVE: AUTONOMOUS SECURE ECCM SPECTRUM COUNTER SIGNAL", (660, 245), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 0), 1, cv2.LINE_AA)
            t_clean = time.time() * 10.0
            clean_y = (295 + np.sin(self.ew_x_vector * 0.05 + t_clean) * 25).astype(np.int32)
            pts_clean = np.column_stack((wave_start_x + self.ew_x_vector, clean_y))
            cv2.polylines(canvas, [pts_clean], False, (0, 255, 0), 2, cv2.LINE_AA)

            # --- LOWER BAR DASHBOARD INTERFACE CONTROLS ---
            cv2.rectangle(canvas, (0, self.height - 35), (self.width, self.height), (12, 14, 18), -1)
            cv2.putText(canvas, "[KEY 1]: RADAR SWEEP MODE | [KEY 2]: TRIGGER ELECTRONIC JAMMING & ECCM OVERRIDES | [Q]: TERMINATE SECURITY CORE", (25, self.height - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 205), 1, cv2.LINE_AA)
            cv2.putText(canvas, "DEVELOPED BY: SK SOYEB AKHTAR", (self.width - 290, self.height - 12), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

            cv2.imshow("DRDO TACTICAL RADAR MISSION DASHBOARD", canvas)
            
            key = cv2.waitKey(15) & 0xFF
            if key == ord('1'):
                self.jamming_active = False
            elif key == ord('2'):
                self.jamming_active = True
            elif key == ord('q'):
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = DRDOMissionControlApp()
    app.launch_mission_suite()

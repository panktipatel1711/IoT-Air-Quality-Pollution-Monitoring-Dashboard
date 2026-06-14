"""
Module: virtual_device.py
Description: Production-Grade IoT Environmental Data Simulator & Local CSV Engine.
Author: Applied Data Science & IoT Student Portfolio Project
Version: 2.0.0 (Production Ready)
"""

import os
import csv
import sys
import time
import math
import random
from datetime import datetime

# ==========================================
# ENTERPRISE SYSTEM CONFIGURATION
# ==========================================
class Config:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIRECTORY = os.path.join(PROJECT_ROOT, "data")
    LOG_FILE_PATH = os.path.join(DATA_DIRECTORY, "pollution_logs.csv")
    
    POLLING_INTERVAL_SECONDS = 2.0  # Real-time data frequency
    TOTAL_EXECUTION_STEPS = 100     # Set to 0 or None for infinite loop
    
    # Synced Microcontroller Hardware Thresholds
    THRESH_CLEAN_GOOD = 800
    THRESH_MODERATE = 1800
    THRESH_POOR = 3000

# ==========================================
# ENVIRONMENTAL ENGINE SIMULATOR (SMART DATA)
# ==========================================
class EnvironmentalSimulator:
    """Generates continuous time-series mathematical metrics mimicking real atmosphere spikes."""
    def __init__(self):
        self.step_counter = 0

    def synthesize_telemetry(self) -> tuple:
        """
        Uses mathematical sine curves combined with random noise to simulate natural 
        diurnal shifts, high rush hour traffic pollution, and accidental leak anomalies.
        """
        self.step_counter += 1
        
        # Base Sine wave component to simulate smooth daily temperature/humidity shifts
        sine_wave = math.sin(self.step_counter * 0.1)
        
        # Base atmospheric metrics
        temperature = round(25.0 + (sine_wave * 4.0) + random.uniform(-0.5, 0.5), 1)
        humidity = round(50.0 - (sine_wave * 8.0) + random.uniform(-1.0, 1.0), 1)

        # Multi-phase simulation engine for realistic tracking portfolio evidence
        if self.step_counter < 25:
            # Phase 1: Normal baseline conditions (Good / Safe Air)
            gas_reading = random.randint(350, 780)
        elif 25 <= self.step_counter < 50:
            # Phase 2: Moderate pollution buildup (Traffic congestion hours)
            gas_reading = random.randint(1100, 1750)
        elif 50 <= self.step_counter < 75:
            # Phase 3: Industrial fugitive emission leak or thick smoke hazard (Critical)
            gas_reading = random.randint(3100, 4095)  # Cap at ESP32 12-bit max resolution
        else:
            # Phase 4: Dissipation phase after emergency ventilation systems trigger
            gas_reading = random.randint(600, 1200)

        return gas_reading, temperature, humidity

# ==========================================
# DATA PARSING & BUSINESS LOGIC LAYER
# ==========================================
class AnalyticsEngine:
    @staticmethod
    def evaluate_air_safety(gas_value: int) -> tuple:
        """Maps raw gas readings to professional standard AQI categories and alarm states."""
        if gas_value <= Config.THRESH_CLEAN_GOOD:
            return "Good", "OFF", "\033[92m"      # Green Terminal Output
        elif gas_value <= Config.THRESH_MODERATE:
            return "Moderate", "OFF", "\033[93m"  # Yellow Terminal Output
        elif gas_value <= Config.THRESH_POOR:
            return "Poor", "ACTIVE_BLINK", "\033[91m"  # Light Red Terminal Output
        else:
            return "Hazardous", "CRITICAL_SIREN", "\033[41m\033[37m"  # Solid Red Warning Badge

# ==========================================
# HARDWARE PERSISTENCE STORAGE LAYER
# ==========================================
class StorageManager:
    """Manages secure file handshakes and appends live arrays into the CSV schema."""
    def __init__(self):
        self.initialize_repository()

    def initialize_repository(self):
        """Creates data pipelines safely without throwing system access exceptions."""
        try:
            os.makedirs(Config.DATA_DIRECTORY, exist_ok=True)
            if not os.path.exists(Config.LOG_FILE_PATH):
                with open(Config.LOG_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        "Timestamp", "Gas_Concentration", 
                        "Temperature_C", "Humidity_Pct", 
                        "Category", "Alert_Status"
                    ])
                print(f"[STORAGE] Normalized local data vault at: {Config.LOG_FILE_PATH}")
        except Exception as error:
            print(f"[CRITICAL] Error initializing disk space: {str(error)}")
            sys.exit(1)

    def write_record(self, timestamp: str, gas: int, temp: float, hum: float, cat: str, alert: str):
        """Appends data rows smoothly. Auto-opens and closes connection to prevent memory leakage."""
        try:
            with open(Config.LOG_FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, gas, temp, hum, cat, alert])
        except IOError:
            print(f"[WARN] Storage device busy. Dropping frame array at timestamp: {timestamp}")

# ==========================================
# MAIN ROUTINE PIPELINE CAPTURE
# ==========================================
def main():
    # Console presentation text assets
    RESET_COLOR = "\033[0m"
    BOLD_TEXT = "\033[1m"
    
    print(f"{BOLD_TEXT}====================================================")
    print("  ENTERPRISE IoT AIR MONITORING ENGINE - SIMULATOR  ")
    print(f"===================================================={RESET_COLOR}")
    
    # Objects initialization
    storage = StorageManager()
    simulator = EnvironmentalSimulator()
    current_iteration = 0

    print(f"\n[SYSTEM] Polling worker thread booted successfully.")
    print("[RUNNING] Logging telemetry telemetry to disk... (Press Ctrl+C to terminate)\n")

    try:
        while True:
            current_iteration += 1
            if Config.TOTAL_EXECUTION_STEPS and current_iteration > Config.TOTAL_EXECUTION_STEPS:
                print("\n[INFO] Finished planned automation run batches safely.")
                break

            # 1. Fetch synthetically modeled metrics
            gas, temp, hum = simulator.synthesize_telemetry()
            
            # 2. Extract classified categorization vectors
            category, alert_level, color_code = AnalyticsEngine.evaluate_air_safety(gas)
            
            # 3. Create ISO formatted system time vector
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 4. Commit data row to the persistent CSV database file
            storage.write_record(time_now, gas, temp, hum, category, alert_level)

            # 5. Print a beautifully clean terminal logging display
            print(f"[{time_now}] Frame #{current_iteration:03d}")
            print(f" ├─ Raw Gas Metric    : {gas} units")
            print(f" ├─ Ambient Air Temp  : {temp} °C  | Relative Moisture: {hum} %")
            print(f" └─ System Evaluation : {color_code}[ {category} ]{RESET_COLOR} | Alarm: {alert_level}")
            
            if alert_level == "CRITICAL_SIREN":
                print(f" {color_code}!! CRITICAL AIR POLLUTION MAXIMUM EXCEEDED !!{RESET_COLOR}")
            print("-" * 52)

            time.sleep(Config.POLLING_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print(f"\n\n{BOLD_TEXT}[SHUTDOWN] Interruption detected. Safely flushing pipelines to disk.{RESET_COLOR}")
        print("[STATUS] Shutdown complete.")

if __name__ == "__main__":
    main()
# Enzo Peres Afonso 2025 https://github.com/enzoperesafonso

from machine import Pin, I2C, WDT, disable_irq, enable_irq
import time
import math
from aht20bmp280 import BMP280, AHT20

# === CONFIGURATION ===

# I2C configuration (bus ID and pin numbers)
I2C_BUS_ID = 0
I2C_SCL_PIN = 1
I2C_SDA_PIN = 0

# GPIO pin assignments
HALL_EFFECT_PIN = 2     # Hall sensor input pin
STATUS_LED_PIN = 25      # Onboard LED for status heartbeat

# Anemometer physical properties
MAGNETS_PER_REV = 3                    # Number of magnets attached to the rotor
ANEMOMETER_RADIUS_M = 0.15            # Radius of anemometer (meters)
CIRCUMFERENCE_M = 2 * math.pi * ANEMOMETER_RADIUS_M  # Rotor circumference

# Calibration parameters (derived from actual vs uncalibrated measurements)
CALIBRATION_SLOPE = 2.445645          # Linear slope factor
CALIBRATION_OFFSET = 0         # Linear offset (m/s)

# Timing intervals
REPORT_INTERVAL_MS = 5000             # How often to report data (ms)
DEBOUNCE_MS = 10                      # Debounce time for Hall sensor input (ms)
WATCHDOG_TIMEOUT_MS = 8000           # Watchdog reset interval (ms)

# === I2C and SENSOR SETUP ===

# Initialize I2C bus
i2c = I2C(I2C_BUS_ID, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))

# Initialize sensors
aht = AHT20(i2c)      # Temperature and humidity
bmp = BMP280(i2c)     # Temperature and pressure

# === WIND SPEED VARIABLES ===

pulse_count = 0           # Total magnet pulses detected
last_pulse_time = 0       # Time of last valid pulse (for debouncing)

# === STATUS LED ===

led = Pin(STATUS_LED_PIN, Pin.OUT)  # Onboard LED for visual heartbeat

# === WATCHDOG TIMER ===

wdt = WDT(timeout=WATCHDOG_TIMEOUT_MS)  # Resets system if loop stalls

# === HALL SENSOR INTERRUPT HANDLER ===

def hall_interrupt(pin):
    """Triggered on falling edge of Hall effect signal.
    Debounced to prevent false counts due to mechanical noise."""
    global pulse_count, last_pulse_time
    now = time.ticks_ms()
    if time.ticks_diff(now, last_pulse_time) > DEBOUNCE_MS:
        pulse_count += 1
        last_pulse_time = now

# Setup Hall effect sensor pin with internal pull-up and interrupt
hall = Pin(HALL_EFFECT_PIN, Pin.IN, Pin.PULL_UP)
hall.irq(trigger=Pin.IRQ_FALLING, handler=hall_interrupt)

# === ROLLING AVERAGE BUFFER ===

wind_buffer = []

def get_rolling_avg(new_value, window=5):
    """Maintain a rolling average over 'window' samples."""
    wind_buffer.append(new_value)
    if len(wind_buffer) > window:
        wind_buffer.pop(0)
    return sum(wind_buffer) / len(wind_buffer)

# === WIND SPEED CALIBRATION ===

def calibrate_wind_speed(uncalibrated_speed):
    """Apply linear calibration: calibrated = slope * uncalibrated + offset"""
    return CALIBRATION_SLOPE * uncalibrated_speed + CALIBRATION_OFFSET

# === SENSOR READ WITH VALIDATION AND RETRIES ===

def safe_sensor_read(retries=3):
    """Attempts to read all sensors, retrying on failure.
    Returns placeholder values if all attempts fail."""
    for _ in range(retries):
        try:
            aht_temp, humidity = aht.measure()
            bmp_temp, pressure = bmp.read()
            t_avg = (aht_temp + bmp_temp) / 2
            if is_valid(t_avg, humidity, pressure):
                return t_avg, humidity, pressure
        except Exception:
            time.sleep(0.1)
    return -999, -1, -1  # Error codes

def is_valid(temp, hum, pres):
    """Sanity check for sensor ranges."""
    return -40 <= temp <= 90 and 0 <= hum <= 100 and 300 <= pres <= 1100

# === MAIN LOOP ===

last_report_time = time.ticks_ms()
# print("Weather station started.")
# print("Format: T:temp H:humidity P:pressure WS:wind_speed_ms")

while True:
    # Feed watchdog to avoid reset
    wdt.feed()

    # Toggle status LED to indicate system is alive
    led.toggle()

    current_time = time.ticks_ms()
    
    # Check if it's time to report
    if time.ticks_diff(current_time, last_report_time) >= REPORT_INTERVAL_MS:
        elapsed_seconds = time.ticks_diff(current_time, last_report_time) / 1000.0
        last_report_time = current_time

        # Atomically read and reset pulse counter to avoid race conditions
        state = disable_irq()
        pulses = pulse_count
        pulse_count = 0
        enable_irq(state)

        # Calculate raw wind speed based on counted pulses
        rotations = pulses / MAGNETS_PER_REV
        distance_m = rotations * CIRCUMFERENCE_M
        wind_speed_raw = distance_m / elapsed_seconds if elapsed_seconds > 0 else 0
        
        # Apply calibration to get actual wind speed
        wind_speed_calibrated = calibrate_wind_speed(wind_speed_raw)

        # Smooth wind speed using rolling average
        wind_speed_avg = get_rolling_avg(wind_speed_calibrated)

        # Read temperature, humidity, and pressure
        temp, hum, pres = safe_sensor_read()

        # Print results to serial console
        if temp == -999:
            print(f"T:ERR H:ERR P:ERR WS:{wind_speed_avg:.2f}")
        else:
            print(f"T:{temp:.1f} H:{hum:.1f} P:{pres:.1f} WS:{wind_speed_avg:.2f}")

    # Prevent CPU from spinning at 100% — improves stability
    time.sleep_ms(10)

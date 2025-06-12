# Enzo Peres Afonso 2025 https://github.com/enzoperesafonso

from machine import I2C, Pin
import utime

# --- BMP280 Driver ---
class BMP280:
    """
    MicroPython driver for the BMP280 temperature and pressure sensor.
    """

    def __init__(self, i2c, addr=0x77):
        """
        Initialize the BMP280 sensor.

        :param i2c: Initialized machine.I2C instance.
        :param addr: I2C address of the BMP280 sensor (default 0x77).
        """
        self.i2c = i2c
        self.addr = addr
        self._load_calibration()  # Load factory calibration data from sensor

        # Control measurement register:
        # Normal mode, temperature oversampling x1, pressure oversampling x1
        self.i2c.writeto_mem(self.addr, 0xF4, b'\x27')

        # Configuration register:
        # Standby time = 1000 ms, filter coefficient = 4
        self.i2c.writeto_mem(self.addr, 0xF5, b'\xA0')

    def _read16(self, reg):
        """
        Read an unsigned 16-bit value from two consecutive registers.

        :param reg: Starting register address.
        :return: Unsigned 16-bit integer.
        """
        data = self.i2c.readfrom_mem(self.addr, reg, 2)
        return data[1] << 8 | data[0]

    def _read16s(self, reg):
        """
        Read a signed 16-bit value from two consecutive registers.

        :param reg: Starting register address.
        :return: Signed 16-bit integer.
        """
        val = self._read16(reg)
        return val - 65536 if val > 32767 else val

    def _read24(self, reg):
        """
        Read a 24-bit unsigned value from three consecutive registers.

        :param reg: Starting register address.
        :return: 24-bit unsigned integer.
        """
        data = self.i2c.readfrom_mem(self.addr, reg, 3)
        return (data[0] << 16) | (data[1] << 8) | data[2]

    def _load_calibration(self):
        """
        Load calibration constants from BMP280 non-volatile memory.
        These values are required to compensate raw sensor data.
        """
        self.dig_T1 = self._read16(0x88)
        self.dig_T2 = self._read16s(0x8A)
        self.dig_T3 = self._read16s(0x8C)
        self.dig_P1 = self._read16(0x8E)
        self.dig_P2 = self._read16s(0x90)
        self.dig_P3 = self._read16s(0x92)
        self.dig_P4 = self._read16s(0x94)
        self.dig_P5 = self._read16s(0x96)
        self.dig_P6 = self._read16s(0x98)
        self.dig_P7 = self._read16s(0x9A)
        self.dig_P8 = self._read16s(0x9C)
        self.dig_P9 = self._read16s(0x9E)

    def read(self):
        """
        Read and return compensated temperature and pressure values.

        :return: Tuple of temperature in °C and pressure in hPa.
        """
        # Raw readings
        adc_T = self._read24(0xFA) >> 4
        adc_P = self._read24(0xF7) >> 4

        # Temperature compensation
        var1 = (((adc_T >> 3) - (self.dig_T1 << 1)) * self.dig_T2) >> 11
        var2 = (((((adc_T >> 4) - self.dig_T1) * ((adc_T >> 4) - self.dig_T1)) >> 12) * self.dig_T3) >> 14
        t_fine = var1 + var2
        temperature = ((t_fine * 5 + 128) >> 8) / 100

        # Pressure compensation
        var1_p = t_fine - 128000
        var2_p = var1_p * var1_p * self.dig_P6
        var2_p += (var1_p * self.dig_P5) << 17
        var2_p += self.dig_P4 << 35
        var1_p = ((var1_p * var1_p * self.dig_P3) >> 8) + ((var1_p * self.dig_P2) << 12)
        var1_p = (((1 << 47) + var1_p) * self.dig_P1) >> 33

        if var1_p == 0:
            pressure = 0  # Avoid division by zero
        else:
            p = 1048576 - adc_P
            p = ((p << 31) - var2_p) * 3125 // var1_p
            var1_p = (self.dig_P9 * (p >> 13) * (p >> 13)) >> 25
            var2_p = (self.dig_P8 * p) >> 19
            pressure = ((p + var1_p + var2_p) >> 8) / 25600

        return temperature, pressure


# --- AHT20 Driver ---
class AHT20:
    """
    MicroPython driver for the AHT20 temperature and humidity sensor.
    """

    def __init__(self, i2c, addr=0x38):
        """
        Initialize the AHT20 sensor and perform initial calibration.

        :param i2c: Initialized machine.I2C instance.
        :param addr: I2C address of the AHT20 (default 0x38).
        """
        self.i2c = i2c
        self.addr = addr
        self._init_sensor()

    def _init_sensor(self):
        """
        Send initialization command to the AHT20 sensor.
        """
        self.i2c.writeto(self.addr, b'\xE1\x08\x00')
        utime.sleep_ms(40)  # Allow time for initialization

    def _read_status(self):
        """
        Read the status byte from the sensor.

        :return: Single byte representing sensor status.
        """
        return self.i2c.readfrom(self.addr, 1)[0]

    def measure(self):
        """
        Trigger a measurement and return temperature and humidity readings.

        :return: Tuple of temperature in °C and humidity in %RH.
        """
        self.i2c.writeto(self.addr, b'\xAC\x33\x00')
        utime.sleep_ms(80)  # Wait for measurement cycle

        # Wait until busy bit (bit 7) clears
        while self._read_status() & 0x80:
            utime.sleep_ms(10)

        data = self.i2c.readfrom(self.addr, 6)

        # Parse measurement data
        raw_humidity = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4))
        raw_temperature = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

        # Convert to physical values
        humidity = (raw_humidity * 100) / 1048576
        temperature = ((raw_temperature * 200) / 1048576) - 50

        return temperature, humidity

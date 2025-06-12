from machine import I2C, Pin
import utime

# --- BMP280 Driver ---
class BMP280:
    """
    Driver for BMP280 temperature and pressure sensor.
    """

    def __init__(self, i2c, addr=0x77):
        """
        Initialize the BMP280 sensor.

        :param i2c: Initialized machine.I2C object
        :param addr: I2C address of BMP280 sensor (default 0x77)
        """
        self.i2c = i2c
        self.addr = addr
        self._load_calibration()   # Load sensor calibration data
        # Configure sensor: normal mode, temperature & pressure oversampling x1
        self.i2c.writeto_mem(self.addr, 0xF4, b'\x27')  
        # Configuration register: standby time and filter settings
        self.i2c.writeto_mem(self.addr, 0xF5, b'\xA0')  

    def _read16(self, reg):
        """
        Read an unsigned 16-bit value from two registers (little endian).

        :param reg: Register address to start reading from
        :return: Unsigned 16-bit integer
        """
        data = self.i2c.readfrom_mem(self.addr, reg, 2)
        # Note: BMP280 stores data in little endian format
        return data[1] << 8 | data[0]

    def _read16s(self, reg):
        """
        Read a signed 16-bit value from two registers.

        :param reg: Register address to start reading from
        :return: Signed 16-bit integer
        """
        val = self._read16(reg)
        return val - 65536 if val > 32767 else val

    def _read24(self, reg):
        """
        Read a 24-bit value from three registers.

        :param reg: Register address to start reading from
        :return: 24-bit integer
        """
        data = self.i2c.readfrom_mem(self.addr, reg, 3)
        return (data[0] << 16) | (data[1] << 8) | data[2]

    def _load_calibration(self):
        """
        Load calibration data from sensor registers. 
        These values are needed to compute temperature and pressure accurately.
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
        Reads raw temperature and pressure data, applies calibration formulas,
        and returns compensated temperature and pressure values.

        :return: (temperature in Celsius, pressure in hPa)
        """
        # Read raw temperature and pressure
        adc_T = self._read24(0xFA) >> 4
        adc_P = self._read24(0xF7) >> 4

        # Temperature compensation calculations (from datasheet)
        var1 = (((adc_T >> 3) - (self.dig_T1 << 1)) * self.dig_T2) >> 11
        var2 = (((((adc_T >> 4) - self.dig_T1) * ((adc_T >> 4) - self.dig_T1)) >> 12) * self.dig_T3) >> 14
        t_fine = var1 + var2
        temperature = ((t_fine * 5 + 128) >> 8) / 100

        # Pressure compensation calculations
        var1_p = t_fine - 128000
        var2_p = var1_p * var1_p * self.dig_P6
        var2_p += (var1_p * self.dig_P5) << 17
        var2_p += self.dig_P4 << 35
        var1_p = ((var1_p * var1_p * self.dig_P3) >> 8) + ((var1_p * self.dig_P2) << 12)
        var1_p = (((1 << 47) + var1_p) * self.dig_P1) >> 33

        if var1_p == 0:
            pressure = 0  # Prevent division by zero
        else:
            p = 1048576 - adc_P
            p = ((p << 31) - var2_p) * 3125 // var1_p
            var1_p = (self.dig_P9 * (p >> 13) * (p >> 13)) >> 25
            var2_p = (self.dig_P8 * p) >> 19
            pressure = ((p + var1_p + var2_p) >> 8) / 25600  # Pressure in hPa

        return temperature, pressure


# --- AHT20 Driver ---
class AHT20:
    """
    Driver for AHT20 temperature and humidity sensor.
    """

    def __init__(self, i2c, addr=0x38):
        """
        Initialize AHT20 sensor and trigger calibration.

        :param i2c: Initialized machine.I2C object
        :param addr: I2C address of AHT20 (default 0x38)
        """
        self.i2c = i2c
        self.addr = addr
        self._init_sensor()

    def _init_sensor(self):
        """
        Send initialization command to sensor and wait for it to be ready.
        """
        self.i2c.writeto(self.addr, b'\xE1\x08\x00')  # Initialization command
        utime.sleep_ms(40)

    def _read_status(self):
        """
        Read status register to check if measurement is ongoing.

        :return: Status byte
        """
        return self.i2c.readfrom(self.addr, 1)[0]

    def measure(self):
        """
        Trigger a measurement and read temperature and humidity data.

        :return: (temperature in Celsius, humidity in %RH)
        """
        self.i2c.writeto(self.addr, b'\xAC\x33\x00')  # Trigger measurement
        utime.sleep_ms(80)  # Wait for measurement to complete

        # Wait while busy bit (bit 7) is set
        while self._read_status() & 0x80:
            utime.sleep_ms(10)

        data = self.i2c.readfrom(self.addr, 6)

        # Extract raw humidity and temperature data from bytes
        raw_humidity = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4))
        raw_temperature = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

        # Convert raw values to human-readable units
        humidity = (raw_humidity * 100) / 1048576
        temperature = ((raw_temperature * 200) / 1048576) - 50

        return temperature, humidity





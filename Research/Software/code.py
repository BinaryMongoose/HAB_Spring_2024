import board
import busio
import sdcardio
import storage
import digitalio
import time
import alarm

import adafruit_lis331   # Accelerometer
import adafruit_scd30    # CO2 sensor
import adafruit_bme680   # Temp, humid, pressure, alt
import adafruit_max1704x # bettery Guage

import supervisor

# When the software, restart theprogram.
supervisor.set_next_code_file(filename='code.py', reload_on_error=True)


# Setting up the communication protocol for SD.
spi = busio.SPI(board.SD_SCK, MOSI=board.SD_MOSI, MISO=board.SD_MISO)

# Making a sd card object.
sd = sdcardio.SDCard(spi, board.SD_CS)
# Connecting the SD card, so we can use it.
vfs = storage.VfsFat(sd)
storage.mount(vfs, '/sd')


# Setting up communication for sensors.
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

"""
Setting up all the sensors used:
 - H3LJS331
 - BME680
 - SCD-30
 - MAX1704 (inbuilt)
"""

scd = adafruit_scd30.SCD30(i2c)

# Setting up accelerometer.
lis = adafruit_lis331.LIS331HH(i2c)

# Setting up BME680.
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
bme680.sea_level_pressure = 1013.25
temperature_offset = -5

# Setting up MAX1704.
max17 = adafruit_max1704x.MAX17048(i2c)


# Setting up LED.
led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

TEN_SECONDS = 10

file_name = "la_cuisine"

header = "brd_time, lis_x, lis_y, lis_z,\
bme_temp, bme_gas, bme_humidity, bme_pressure, bme_altitude,\
scd_CO2, scd_temp, scd_humidity,\
max_voltage, max_percent, max_rate\n"

with open(f"/sd/{file_name}.csv", "a") as sd, open(f"/{file_name}.csv", "a") as flash:
    sd.write(header)
    flash.write(header)

    for i in range(0, 10):
        print("Logged file")
        led.value = True
        x, y, z = lis.acceleration
        time_now = time.monotonic()
        data = [time_now, x, y, z,                                                                        # ISM Stuff & Time
                (bme680.temperature + temperature_offset), bme680.gas, bme680.humidity, bme680.pressure, bme680.altitude,  # BME Stuff
                scd.CO2, scd.temperature, scd.relative_humidity,                                          # SCD Stuff
                max17.cell_voltage, max17.cell_percent, max17.charge_rate]                                # MAX Stuff

        for d in data:
            sd.write(f'{d},')
            flash.write(f'{d},')
        sd.write('\n')
        sd.flush()  # Syncing SD card.
        flash.write('\n')
        flash.flush()  # Syncing FLASH.

        led.value = False

        # Makes the board fall asleep for 10 seconds.
        time_alarm = alarm.time.TimeAlarm(monotonic_time=time_now + TEN_SECONDS)
        alarm.light_sleep_until_alarms(time_alarm)


import board
import busio
import sdcardio
import storage
import digitalio
import time
import alarm

import adafruit_lis331
import adafruit_sgp30
import adafruit_bme680
import adafruit_max1704x

import supervisor

supervisor.set_next_code_file(filename='code.py', reload_on_error=True)

spi = busio.SPI(board.SD_SCK, MOSI=board.SD_MOSI, MISO=board.SD_MISO)

sd = sdcardio.SDCard(spi, board.SD_CS)
vfs = storage.VfsFat(sd)
storage.mount(vfs, '/sd')


i2c = board.STEMMA_I2C()


lis = adafruit_lis331.LIS331HH(i2c)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
bme680.sea_level_pressure = 1013.25
temperature_offset = -5

max17 = adafruit_max1704x.MAX17048(i2c)

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

TEN_SECONDS = 10

with open("/sd/data1.csv", "a") as sd:
    sd.write("brd_time, lis_x, lis_y, lis_z, bme_temp, bme_gas, bme_pressure, bme_altitude, max_voltage, max_percent, max_rate\n")

    for i in range(0, 3600):
        print("Logged file")
        led.value = True
        x, y, z = lis.acceleration
        time_now = time.monotonic()
        data = [time_now, x, y, z, (bme680.temperature + temperature_offset), bme680.gas,
                bme680.pressure, bme680.altitude, max17.cell_voltage, max17.cell_percent, max17.charge_rate]

        for d in data:
            sd.write(f'{d},')
        sd.write('\n')
        sd.flush()

        led.value = False

        time_alarm = alarm.time.TimeAlarm(monotonic_time=time_now + TEN_SECONDS)
        alarm.light_sleep_until_alarms(time_alarm)

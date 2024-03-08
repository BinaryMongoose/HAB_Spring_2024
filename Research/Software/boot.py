import board
import digitalio
import storage
import time


""" If the button is being held during startup, enter debugging mode """
switch = digitalio.DigitalInOut(board.D16)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()


led.value = True
time.sleep(1)
led.value = False


debugging = not switch.value
storage.remount("/", readonly=debugging)

from gpiozero import LED
from time import sleep

led = LED(14)
#led2 = LED(15)

#led.on()

while True:
	led.on()
	sleep(1)
	led.off()
	sleep(1)



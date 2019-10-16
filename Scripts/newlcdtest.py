#from RPLCD import CharLCD
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
import time
# Logical Pins = Physical Pins
D4=33
D5=31
D6=29
D7=32
pin_e=35
pin_rs=37
print('Pins Set')
lcd = CharLCD(cols=16, rows=2, pin_rs=pin_rs, pin_e=pin_e, pins_data=[D4, D5, D6, D7],numbering_mode=GPIO.BOARD)
lcd.cursor_pos = (0,0) #row,col starting with 0
#while True:
lcd.write_string(u'Yo Mama!') #\n starts new line at same pos, \r returns line at 0 pos
time.sleep(6)
lcd.close(clear=True) #closes display and doesnt give warning
#lcd.clear() #clears display but gives warning on restart of display
#time.sleep(2)
print('end of script')
#GPIO.cleanup()

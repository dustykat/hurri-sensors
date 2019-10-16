import RPi.GPIO as GPIO
import time
from RPLCD.gpio import CharLCD

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 23
SPIMISO = 21
SPIMOSI = 19
SPICS = 24
pin_rs=37
pin_e=35
D4=33
D5=31
D6=29
D7=32
lcd = CharLCD(cols=16, rows=2, pin_rs=pin_rs, pin_e=pin_e, pins_data=[D4,D5,D6,D7],numbering_mode=GPIO.BOARD)
lcd.write_string(u'Hello Muddah')
time.sleep(2)
lcd.clear()
# photoresistor connected to adc #0
photo_ch = 0

#port init
def init():
         GPIO.setwarnings(False)
         GPIO.cleanup()			#clean up at the end of your script
         GPIO.setmode(GPIO.BOARD)		#to specify whilch pin numbering system
         # set up the SPI interface pins
         GPIO.setup(SPIMOSI, GPIO.OUT)
         GPIO.setup(SPIMISO, GPIO.IN)
         GPIO.setup(SPICLK, GPIO.OUT)
         GPIO.setup(SPICS, GPIO.OUT)
         GPIO.setup(pin_rs, GPIO.OUT)
         GPIO.setup(pin_e, GPIO.OUT)
         GPIO.setup(D4, GPIO.OUT)
         GPIO.setup(D5, GPIO.OUT)
         GPIO.setup(D6, GPIO.OUT)
         GPIO.setup(D7, GPIO.OUT)
         

lcd.clear()
lcd.write_string(u'Hello Fadda')
time.sleep(2)
lcd.clear()
#read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)	

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

def main():
         init()

         time.sleep(5)
         print" Multi-Channel Level Detector \n "
#	 print "Salt-Gradient Experiments "
#         print" Experiment 2 - Detect on Channel 0 and 1 using sequential polling \n"
         print" Data File Syntax is : \n"
         print" Weekday Month Day HH:MM:SS Year : ADC Value "
         lcd.clear()         
         lcd.write_string(u'Prost Mudda')
         time.sleep(2)
         lcd.clear()
         while True:
                 # set channel
                  photo_ch = 0
                  adc_value=readadc(photo_ch, SPICLK, SPIMOSI, SPIMISO, SPICS)
                  now = time.strftime("%c") # capture actual time as center of sampling interval
                 
                  print now + " " + "CH: " + str(photo_ch) + " ADCVal: " + str(adc_value)
#
                  if adc_value == 0:
                           warning='sensor dry'
                  elif adc_value >0 and adc_value <250:
                           warning='slow down'
                  elif adc_value >=250:
                           warning='danger'
#
                  lcd.clear()
                  lcd.write_string(warning)
                  time.sleep(1) 
#                  photo_ch = 1
#                  adc_value=readadc(photo_ch, SPICLK, SPIMOSI, SPIMISO, SPICS)
#                  print now + " : " + "Channel = " + str(photo_ch) + " Value = " + str(adc_value) 
                 # if adc_value == 0:
                 #          print"no water\n"
                 #          print"adc_value :"+str(adc_value)+"\n"
                 # elif adc_value>0 and adc_value<30 :
                 #          print"it is raindrop\n"
                 #          print"adc_value :"+str(adc_value)+"\n"
                 # elif adc_value>=30 and adc_value<200 :
                 #          print"it is water flow"
                 #          print"water level:"+str("%.1f"%(adc_value/200.*100))+"%\n"
                 #          print"adc_value :"+str(adc_value)+"\n"
                  #print "adc_value= " +str(adc_value)+"\n"
                  
                  
                  

        

if __name__ == '__main__':
         try:
                  main()
                 
         except KeyboardInterrupt:
                  pass
GPIO.cleanup()





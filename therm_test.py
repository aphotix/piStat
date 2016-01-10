#Thermostat test script This tests all functionality
import wiringpi as io
import time
import Adafruit_CharLCD as LCD
import sht31
sht31 = sht31.SHT31(0)
LOW = 0
HIGH = 1
OUTPUT = 1
RELAY = 7

io.wiringPiSetup()
io.pinMode(RELAY,OUTPUT)

lcd = LCD.Adafruit_CharLCDPlate()

# Test Relay
io.digitalWrite(RELAY,HIGH)
time.sleep(1)
io.digitalWrite(RELAY,LOW)
time.sleep(1)

# activate screen
lcd.set_color(1,1,1)
lcd.clear()
time.sleep(1)
lcd.message('Hello!')
time.sleep(1)

# initialize temp
temperature, humidity = sht31.get_temp_and_humidity()

f = temperature * 9 / 5 + 32
h = humidity
print "Temperature: %s in celcius" % temperature
print "Humidity: %s" % h
print "Temperature %s in F" % f

buttons = ( (LCD.SELECT, 'Select'),
            (LCD.LEFT,   'Left'),
            (LCD.UP,     'Up'),
            (LCD.DOWN,   'Down'),
            (LCD.RIGHT,  'Right') )

counter = 25;
ideal_temp = 70.0
last_message = "Hello!"

lcd.clear()



while True:
    counter += 1
    time.sleep(.25)

    if counter % 20 == 0:
        temperature, humidity = sht31.get_temp_and_humidity()
        f = round((temperature * 9 / 5 + 32),1)
        h = round(humidity, 1)

    if counter > 40:
        counter = 0
        lcd.clear()

    lcd.message("Temp " + str(f) + "    %rh\nSet  " + str(ideal_temp) + "   " + str(h))


    for button in buttons:
        if lcd.is_pressed(button[0]):
            if button[1] == 'Select':
                if sht31.check_heater_status():
                    sht31.turn_heater_off()
                    print "sht31 Heater Off"
                else:
                    sht31.turn_heater_on()
                    print "sht31 Heater On"
            if button[1] == 'Up':
                ideal_temp += 1
            if button[1] == 'Down':
                ideal_temp -= 1


    if f < ideal_temp:
        io.digitalWrite(RELAY,HIGH)
    else:
        io.digitalWrite(RELAY,LOW)

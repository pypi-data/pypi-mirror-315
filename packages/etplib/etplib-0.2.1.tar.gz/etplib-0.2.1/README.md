# Embedded Tester Protocol (ETP) library for Python

`etplib` allows access to microcontroller peripherals from a host computer. Microcontroller should be running the ETP firmware.

## Inital setup
- Install `etplib` using pip
  ```terminal
  pip install etplib
  ```

## Flashing ETP firmware
### Arduino Uno
- Download [ETP firmware for Arduino Uno](https://github.com/jabezwinston/etplib/releases/download/v0.2.0/etp_fw_arduino_uno_v0.2.0.hex)
- Flash ETP firmware to the Arduino Uno using `avrdude` (Get avrdude [here](https://github.com/avrdudes/avrdude/releases/))

  ```terminal
   avrdude -v -p atmega328p -c arduino -P COM4 -b 115200 -D -U flash:w:etp_fw_arduino_uno_v0.1.0.hex:i
  ```
> NOTE : Replace `COM4` with the port where the Arduino Uno is connected

### ESP32
- Download [ETP firmware package for ESP32](https://github.com/jabezwinston/etplib/releases/download/v0.2.0/etp_fw_esp32_v0.2.0.zip)
- Install `esptool` using pip
  ```terminal
  pip install esptool
  ```
- Run `flash.bat` (Windows) or `flash.sh` (Linux) to flash the ETP firmware to the ESP32
> NOTE : ETP firmware for ESP32 is experimental !

## Usage

### Blink LED

```python
import etplib
import time

etp = etplib.ETP(transport='serial', port='COM4', baudrate=115200)
etp.open()
etp.reset()

etp.gpio.init({"_13": "output"})

# Blink LED on pin 13 of the Arduino Uno
while True:
    etp.gpio_write({"_13": 1})
    time.sleep(1)
    etp.gpio_write({"_13": 0})
    time.sleep(1)

etp.close()
```

# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:

class Sensor():
    def __init__(self):
        self.TRIGGER_THRESHOLD = 900
        self.NOISE_THRESHOLD = 200
        CLK  = 2
        MISO = 8
        MOSI = 7
        CS   = 3
        self.mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

    def read(self,channel):
        return self.mcp.read_adc(channel)

    def trigger(self, channel):
        measurement = self.read(channel)
        return (measurement < self.TRIGGER_THRESHOLD) and (measurement > self.NOISE_THRESHOLD)

    def trigger0(self):
        return self.trigger(0)

    def trigger1(self):
        return self.trigger(1)

    def read0(self):
        return self.read(0)

    def read1(self):
        return self.read(1)
        


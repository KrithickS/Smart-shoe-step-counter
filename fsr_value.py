import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import paho.mqtt.publish as publish

# Calibration parameters
# You need to calibrate these values based on your FSR specifications and setup
VCC = 3.3  # Supply voltage (in volts) changed to 3.3V
R_DIV = 10000.0  # Value of the resistor (in ohms) connected in series with the FSR

# Function to calculate force based on FSR resistance
def fsr_to_force(voltage):
    # Calculate FSR resistance
    fsr_voltage = VCC * (voltage / 65535.0)  # Convert ADC reading to voltage
    if fsr_voltage == 0:
        return 0  # Avoid division by zero
    fsr_resistance = R_DIV / (VCC / fsr_voltage - 1)

    # Calibrated formula for converting FSR resistance to force
    # This function needs to be calibrated based on your FSR specifications and setup
    # The values provided here are just placeholders
    force = (fsr_voltage*fsr_resistance)*100000

    return force

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

# MQTT Broker (Server) Details
mqtt_broker_ip = "192.168.227.90"
mqtt_topic = "thala"

try:
    while True:
        print("Raw ADC Value:", chan.value)
        print("ADC Voltage:", str(chan.voltage) + "V")
        force = fsr_to_force(chan.voltage)
        print("Force:", str(force) + "N")  # Assuming force unit is Newton

        # Publish force value to MQTT server
        publish.single(mqtt_topic, payload=str(force), hostname=mqtt_broker_ip)

        time.sleep(0.5)  # Adjust sleep time as needed

except KeyboardInterrupt:
    pass  # Allow the user to exit the loop by pressing Ctrl+C

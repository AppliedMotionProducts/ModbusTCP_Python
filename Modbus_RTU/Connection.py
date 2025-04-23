import modbus.client
from pymodbus.client.serial import ModbusSerialClient as ModbusClient

# Configure the serial client
client = ModbusClient (
    framer ='rtu',
    port='COM5',     # change com port according to your setup
    baudrate=9600,
    timeout=1,
    parity='N',              # 'E' (even), 'O' (odd), or 'N' (none)
    stopbits=1,
    bytesize=8
)

# Connect to the RTU device
if client.connect():
    print("✅ Connected to RTU device.")

    client.close()
else:
    print("❌ Failed to connect to RTU device.")


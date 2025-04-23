from pymodbus.client import ModbusTcpClient

# Define Modbus server details
IP_ADDRESS = "10.10.10.10"  # Replace with your device's IP
PORT = 502  # Default Modbus TCP port
slave = 1  # Modbus slave ID

# Create Modbus client
client = ModbusTcpClient(IP_ADDRESS, port=PORT)

# Connect to the device
if client.connect():
    print("✅ Connected to Modbus TCP device")
else:
    print("❌ Failed to connect to Modbus TCP device")

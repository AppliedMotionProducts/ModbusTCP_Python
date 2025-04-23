import struct
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

    # MDX+ Modbus TCP example, find Register table in the manual

    # --- Read first 50 holding registers ---
    response = client.read_holding_registers(address=0, count=50, slave=1)
    if response.isError():
        print(f"❌ Error reading registers: {response}")
    else:
        print(f"📥 Register values: {response.registers}")

        # Read Absolute Position
        # Extract signed 32-bit value from registers 6 and 7 (big-endian) (40007 and 40008 as per manual)
        raw = struct.pack('>HH', response.registers[6], response.registers[7])
        Abs_Pos = struct.unpack('>i', raw)[0]
        print(f"🧭 Immediate Absolute Position (IP): {Abs_Pos}")

        # Read Status Code
        # Extract signed 32-bit value from registers 2 and 3 (big-endian) (40003 and 40004 as per manual)
        Status_Code = (response.registers[2] << 16) | response.registers[3]
        print(f"🛎️ Status Code (SC): {Status_Code}")

        # Read Immediate Actual Velocity (IV) from Register 16 (40017 as per manual)
        Act_Vel = response.registers[16]/240.0
        print(f"🏃‍♂️ Immediate Actual Velocity (IV): {Act_Vel}")

    # Close connection
    client.close()

else:
    print("❌ Failed to connect to Modbus TCP device")

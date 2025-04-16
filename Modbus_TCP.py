import struct
from pymodbus.client import ModbusTcpClient

# Define Modbus server details
IP_ADDRESS = "10.10.10.10"  # Replace with your device's IP
PORT = 502  # Default Modbus TCP port
UNIT_ID = 1  # Modbus slave ID

# Create Modbus client
client = ModbusTcpClient(IP_ADDRESS, port=PORT)

# Connect to the device
if client.connect():
    print("✅ Connected to Modbus TCP device")

    # MDX+ Modbus TCP example, find Register table in the manual
    # --- Read holding registers ---
    response = client.read_holding_registers(address=0, count=50, slave=1)
    if response.isError():
        print(f"❌ Error reading registers: {response}")
    else:
        print(f"📥 Register values: {response.registers}")

        # Extract signed 32-bit value from registers 6 and 7 (big-endian) (40007 and 40008 as per manual)
        raw = struct.pack('>HH', response.registers[6], response.registers[7])
        signed_val = struct.unpack('>i', raw)[0]
        print(f"🧭 Immediate Absolute Position (IP): {signed_val}")

    # --- Write ---
    try:
        # Ask user for an unsigned 16-bit value
        user_input = input("Enter HEX value to write to register 124(40125): ")
        value = int(user_input, 16)

        if not (0 <= value <= 0xFFFF):
            print("❌ Each value must be between 0x0000 and 0xFFFF (16-bit unsigned integer)")
        else:
            # Write the value to register 40125 as per manual
            result = client.write_register(address=124, value=value, slave=1)

            if result.isError():
                print("❌ Write failed:", result)
            else:
                print(f"✅ Successfully wrote {value} to register 124")

    except ValueError:
        print("❌ Invalid input. Please enter a valid signed integer.")

    # Close connection
    client.close()

else:
    print("❌ Failed to connect to Modbus TCP device")

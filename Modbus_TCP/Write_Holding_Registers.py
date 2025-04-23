import struct
from pymodbus.client import ModbusTcpClient

# Modbus TCP connection details
IP_ADDRESS = "10.10.10.10"  # Replace with your device's IP
PORT = 502
SLAVE_ID = 1

# Distance, Acceleration, Deceleration, Velocity holding register addresses
DI_Register_address = 351 - 1  # Modbus uses 0-based indexing (40351..352 as per modbus manual)
AC_Register_address = 345 - 1  # Modbus uses 0-based indexing
DE_Register_address = 347 - 1  # Modbus uses 0-based indexing
VE_Register_address = 349 - 1  # Modbus uses 0-based indexing


# Create Modbus client
client = ModbusTcpClient(IP_ADDRESS, port=PORT)

# Signed 32-bit DINT value to write Distance at register address 40351..352
Distance = 100000

# Unsigned 32-bit DINT value to write Accel at register address 40345..40346
AC = 10 * 6 # Writing 10 rps/s

# Unsigned 32-bit DINT value to write Accel at register address 40347..40348
DE = 10 * 6 # Writing 10 rps/s

# Unsigned 32-bit DINT value to write Vel at register address 40349..40350
VE = 3 * 240 # Writing 3 rps


# Pack Distance as signed 32-bit int (big-endian), then unpack into 2 words
packed = struct.pack('>i', Distance)  # '>i' = big-endian signed int
h_DI, l_DI = struct.unpack('>HH', packed)

# Convert unsigned 32-bit int to two 16-bit words (big-endian)
packed = struct.pack('>I', AC)
h_AC, l_AC = struct.unpack('>HH', packed)

# Convert unsigned 32-bit int to two 16-bit words (big-endian)
packed = struct.pack('>I', DE)
h_DE, l_DE = struct.unpack('>HH', packed)

# Convert unsigned 32-bit int to two 16-bit words (big-endian)
packed = struct.pack('>I', VE)
h_VE, l_VE = struct.unpack('>HH', packed)

# Connect and write
if client.connect():
    print("✅ Connected to Modbus TCP device.")

    result = client.write_registers(address=DI_Register_address,
                                    values=[h_DI, l_DI],
                                    slave=SLAVE_ID)
    result = client.write_registers(address=AC_Register_address,
                                    values=[h_AC, l_AC],
                                    slave=SLAVE_ID)
    result = client.write_registers(address=DE_Register_address,
                                    values=[h_DE, l_DE],
                                    slave=SLAVE_ID)
    result = client.write_registers(address=VE_Register_address,
                                    values=[h_VE, l_VE],
                                    slave=SLAVE_ID)

    if result.isError():
        print("❌ Failed to write value.")
    else:
        print(f"✅ Wrote values to registers")


        # --- Write to register 124 (40125) --- Use AMP_Opcode.py for different HEX commands, 9E for Motor disable, 9F for Motor enable, 66 for relative move, 67 for absolute move
        user_input = input("📝 Enter 2-digit hex command to write to register 40125/ check AMP_Opcode.py: ").strip()

        try:
            if len(user_input) != 2 or not all(c in "0123456789abcdefABCDEF" for c in user_input):
                raise ValueError("Invalid input. Enter exactly 2 hex characters (e.g., A5, 1F).")

            hex_value = int(user_input, 16)
            write_address = 125 - 1  # Zero-based address for pymodbus

            write_result = client.write_register(address=write_address, value=hex_value, slave=SLAVE_ID)

            if write_result.isError():
                print("❌ Failed to write to register.")
            else:
                print(f"✅ Wrote {user_input.upper()} (decimal {hex_value}) to register 40125.")
        except ValueError as ve:
            print(f"❗ Input Error: {ve}")

    client.close()
else:
    print("❌ Could not connect to Modbus TCP device.")

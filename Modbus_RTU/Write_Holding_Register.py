import struct
from pymodbus.client.serial import ModbusSerialClient as ModbusClient


# Configure the serial client
client = ModbusClient (
    framer ='rtu',
    port='COM5',     # choose COM port according to your setup
    baudrate=9600,
    timeout=1,
    parity='N',              # 'E' (even), 'O' (odd), or 'N' (none)
    stopbits=1,
    bytesize=8
)


# TSM23Q-3RG Modbus RTU example, find Register table in the manual

# Distance, Acceleration, Deceleration, Velocity holding register addresses
DI_Register_address = 31 - 1  # Modbus uses 0-based indexing (40031..32 as per modbus manual)
AC_Register_address = 28 - 1  # Modbus uses 0-based indexing
DE_Register_address = 29 - 1  # Modbus uses 0-based indexing
VE_Register_address = 30 - 1  # Modbus uses 0-based indexing

# Signed 32-bit DINT value to write Distance at register address 40031..32
# Assign negative values for reverse direction
Distance = 500000

# Pack Distance as signed 32-bit int (big-endian), then unpack into 2 words
packed = struct.pack('>i', Distance)  # '>i' = big-endian signed int
h_DI, l_DI = struct.unpack('>HH', packed)

# Unsigned 16-bit INT value to write Accel at register address 40028
AC = 10 * 6 # Writing 10 rps/s

# Unsigned 16-bit DINT value to write Accel at register address 40029
DE = 10 * 6 # Writing 10 rps/s

# Unsigned 16-bit DINT value to write Vel at register address 40030
VE = 3 * 240 # Writing 3 rps

SLAVE_ID = 32  # Get Slave ID using Applied Motion Software for TSM motor it is step servo quick tuner software

# Connect to the RTU device
if client.connect():
    print("✅ Connected to RTU device.")

    result = client.write_registers(address=DI_Register_address,
                                    values=[h_DI, l_DI],
                                    slave=SLAVE_ID)
    result = client.write_registers(address=AC_Register_address,
                                    values=[AC],
                                    slave=SLAVE_ID)
    result = client.write_registers(address=DE_Register_address,
                                    values=[DE],
                                    slave=SLAVE_ID)
    result = client.write_registers(address=VE_Register_address,
                                    values=[VE],
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
    print("❌ Failed to connect to RTU device.")

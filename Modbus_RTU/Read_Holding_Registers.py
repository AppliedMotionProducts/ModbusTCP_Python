from pymodbus.client.serial import ModbusSerialClient as ModbusClient
import struct

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

# Connect to the RTU device
if client.connect():
    print("✅ Connected to RTU device.")

    # -------- Read first 50 holding registers from 40000 to 40049 ---------
    # Example: Read Holding Register starting at address 0, count=50, from slave ID 32 (use applied motion software for configuration setup)
    response = client.read_holding_registers(address=0, count=50, slave=32)

    if not response.isError():
        print(f"📥 Register values: {response.registers}")

        # Read Absolute Position
        # Extract signed 32-bit value from registers 6 and 7 (big-endian) (40007 and 40008 as per manual)
        raw = struct.pack('>HH', response.registers[6], response.registers[7])
        signed_val = struct.unpack('>i', raw)[0]
        print(f"🧭 Immediate Absolute Position (IP): {signed_val}")

        # Read Status Code
        # Read Status Code (SC) from Register 1 (40002 as per manual)
        Status_Code = response.registers[1]
        print(f"🛎️ Status Code (SC): {Status_Code}")

        # Read Immediate Actual Velocity (IV) from Register 16 (40011 as per manual)
        Act_Vel = response.registers[10]/240.0
        print(f"🏃‍♂️ Immediate Actual Velocity (IV): {Act_Vel}")

    else:
        print(f"❌ Error reading registers: {response}")

    client.close()
else:
    print("❌ Failed to connect to RTU device.")

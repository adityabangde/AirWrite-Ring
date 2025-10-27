import asyncio
from bleak import BleakClient, BleakScanner

SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHAR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

def callback(sender, data):
    value = int.from_bytes(data, byteorder='little')
    print(f"D1 = {value}")

async def main():
    print("Scanning for MyESP32...")
    devices = await BleakScanner.discover(timeout=5.0)

    device = next((d for d in devices if d.name == "MyESP32"), None)
    if not device:
        print("Device not found!")
        return

    async with BleakClient(device.address) as client:
        print(f"Connected to {device.address}")
        await client.start_notify(CHAR_UUID, callback)
        print("Reading data... (Ctrl+C to stop)")
        try:
            while True:
                await asyncio.sleep(0.1)
        except KeyboardInterrupt:
            pass

asyncio.run(main())

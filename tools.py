import serial.tools.list_ports

# List all available COM ports
ports = serial.tools.list_ports.comports()

print("Available COM ports:")
for port in ports:
    print(port.device)

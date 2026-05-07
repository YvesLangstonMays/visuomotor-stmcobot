import serial as s


class serial_commander:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.ser = None

        try:
            self.ser = s.Serial(self.port, baudrate, timeout=1)
            print(f"Port {self.port} opened.")
        except s.SerialException as e:
            print(f"Failed to open port {self.port}: {e}")

    def close_port(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"Port {self.port} closed")

    def read_response(self):
        if self.ser and self.ser.is_open:
            try:
                response = self.ser.readline().decode("utf-8").strip()
                return response
            except Exception as e:
                return f"Read Error: {e}"


testPort = serial_commander("/dev/tty.Bluetooth-Incoming-Port")
print(testPort.read_response())
testPort.close_port()

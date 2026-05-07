import serial as s
from abc import ABC, abstractmethod


class master_commander(ABC):

    @abstractmethod
    def send_command(self, command):
        pass

    @abstractmethod
    def read_response(self):
        pass

    @abstractmethod
    def close_port(self):
        pass


class serial_commander(master_commander):

    def __init__(self, port, baudrate=9600):
        self.port = port
        self.ser = None

        try:
            self.ser = s.Serial(self.port, baudrate, timeout=1, write_timeout=5)
            print(f"Port {self.port} opened.")
        except s.SerialException as e:
            print(f"Failed to open port {self.port}: {e}")

    def send_command(self, command):
        if self.ser and self.ser.is_open:
            self.ser.write(command)

    def read_response(self):
        if self.ser and self.ser.is_open:
            try:
                response = self.ser.readline().decode("utf-8").strip()
                return response
            except Exception as e:
                return f"Read Error: {e}"

    def close_port(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"Port {self.port} closed")


testPort = serial_commander("/dev/ttys001")
print(testPort.read_response())
print(testPort.send_command("MOVE 90 45 30\n".encode("utf-8")))
testPort.close_port()

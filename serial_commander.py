import serial as s
from abc import ABC, abstractmethod
import ikpy, math


# concept prototype - see repo issues
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


class mock_commander(master_commander):
    def __init__(self, port):
        self.port = port
        print(f"[MOCK] Port {self.port} opened.")

    def read_response(self):
        print("Read success.")

    def close_port(self):
        print("Port closed")

    def send_command(self, command):
        print(f"Command: {command} sent.")

    def set_angle(self, command, angleList):
        self.send_command(command)


class command_formatter:
    def __init__(self):
        pass

    def test_angle(self, angle):

        if 0 <= angle <= 180:
            return True
        else:
            return False

    @staticmethod
    def rad_to_deg(degreeValue):

        radianValue = 180 / (math.pi) * degreeValue
        return radianValue

    def reset_angles(self):
        # write a function to set the angles based on the command
        pass

    def get_new_angles(self, angleList):
        new_angles = []
        for angle in angleList:
            temp_angle = round(self.rad_to_deg(angle), 2)
            if self.test_angle(temp_angle):
                new_angles.append(str(temp_angle))
            else:
                print("Invalid angles, resetting")
                self.reset_angles()
                break
        if len(new_angles) < 6:
            print("Angle list not valid length")
            return

        return new_angles

    def format_command(self, command, new_angles):
        if not new_angles:
            return False
        formatted_command = ",".join(new_angles)
        formatted_command = f"{command}:{formatted_command}\n"

        return formatted_command


testPort = mock_commander("/dev/ttys001")
print(testPort.read_response())
print(testPort.send_command("MOVE 90 45 30\n".encode("utf-8")))
testPort.close_port()

formatter = command_formatter()
angles = [1.57, 0.785, 0.523, 0.0, 1.047, 0.261]
new_angles = formatter.get_new_angles(angles)
print(formatter.format_command("MOVE", new_angles))

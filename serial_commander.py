class serial_commander:

    def open_port():
        try:
            print("Port open")
        except:
            print("Failed to open port")

    def close_port():
        try:
            print("Port closed")
        except:
            print("Failed to open port")

    def read_response():
        try:
            response = ""
            print(response)
        except:
            print("No response available")

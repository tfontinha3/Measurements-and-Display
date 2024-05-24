import socket

class Velocity:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        self.sock.bind(("0.0.0.0", 4210))
        self.sock.settimeout(1.0)  # Set timeout for blocking socket operations

    def get_data(self):
        try:
            data, addr = self.sock.recvfrom(1024)  
            #print("Received message from:", addr)
            #print("Received message:", data.decode())
            data_pairs = [pair.split(',') for pair in data.decode().split(';') if pair]
            return [(float(time), float(value)) for time, value in data_pairs]
        except socket.timeout:
            print("Timeout: No data received.")
        except UnicodeDecodeError:
            print("Decode Error: Could not decode the data.")
        except Exception as e:
            print("Error occurred:", str(e))
        return []

    def close(self):
        self.sock.close()

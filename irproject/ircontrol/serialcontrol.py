import serial
import struct

class SerialControl:
    port = None
    baud_rate = None
    
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        
    def execute(self, frequency, periods):
        try:
            ser = serial.Serial(self.port, self.baud_rate, timeout=5)
            serialdata = struct.pack('B', frequency)
            serialdata += struct.pack('<H', len(periods))
            for period in periods:
                serialdata += struct.pack('<H', period)
            ser.write(serialdata)
            result = [ord(ser.read()), ""]
            ser.close()
            return result
        except Exception as ex:
            return [-128, str(ex)]

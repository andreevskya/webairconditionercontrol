import serial
import struct

class SerialControl:
    COMMAND_IR = 0
    COMMAND_TEMP = 1
    
    port = None
    baud_rate = None
    
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        
    def execute(self, frequency, periods):
        try:
            ser = serial.Serial(self.port, self.baud_rate, timeout=5)
            serialdata = struct.pack('B', self.COMMAND_IR)
            serialdata += struct.pack('B', frequency)
            serialdata += struct.pack('<H', len(periods))
            for period in periods:
                serialdata += struct.pack('<H', period)
            ser.write(serialdata)
            result = [ord(ser.read()), ""]
            ser.close()
            return result
        except Exception as ex:
            return [-128, str(ex)]
            
    def measure_temp(self):
        try:
            ser = serial.Serial(self.port, self.baud_rate, timeout=5)
            ser.write(struct.pack('B', self.COMMAND_TEMP))
            r = ord(ser.read())
            t1 = ord(ser.read())
            t2 = ord(ser.read())
            result = [r, "", ((t2 << 8) + t1) * 0.0625]
            ser.close()
            return result
        except Exception as ex:
            return [-128, str(ex), 128]

class HCSR04:
    # TRIG_PIN = pin2
    # ECHO_PIN = pin1
    def __init__(self):
        self.DISTANCE_CM_PER_BIT = 0.21
        self.DISTANCE_OFFSET = 1.8
        self.TRIG_PIN = False
        self.ECHO_PIN = False
        self.okay = False

    def spinit(self):
        if (self.TRIG_PIN and self.ECHO_PIN):
            self.okay = True
            spi.init(baudrate=50000, bits=8, mode=0, miso=self.ECHO_PIN)

    def set_echo_pin(self, pin):
        self.ECHO_PIN = pin
        self.spinit(self)

    def set_trigger_pin(self, pin):
        self.TRIG_PIN = pin
        self.spinit(self)

    def distance(self):
        if (self.okay is False):
            return -1
        gc.disable()
        self.TRIG_PIN.write_digital(True)
        self.TRIG_PIN.write_digital(False)
        x = spi.read(200)
        high_bits = 0
        for i in range(len(x)):
            if x[i] == 0 and high_bits > 0:
                break
            elif x[i] == 0xff:
                high_bits += 8
            else:
                high_bits += bin(x[i]).count('1')
        x = None
        gc.enable()
        gc.collect()
        try:
            return high_bits * self.DISTANCE_CM_PER_BIT + self.DISTANCE_OFFSET
        except:
            return -1


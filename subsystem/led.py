import wpilib
import commands2
kLEDBuffer = 60


class LED(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()
        # PWM Port 9
        # Must be a PWM header, not MXP or DIO
        self.led = wpilib.AddressableLED(9)

        # LED Data
        self.ledData = [wpilib.AddressableLED.LEDData() for _ in range(kLEDBuffer)]

        # Store what the last hue of the first pixel is
        self.rainbowFirstPixelHue = 0

        # Default to a length of 60, start empty output
        # Length is expensive to set, so only set it once, then just update data
        self.led.setLength(kLEDBuffer)

        # Set the data
        self.led.setData(self.ledData)
        self.led.start()
    def setledrgb(self,r,g,b):
        for i in range(kLEDBuffer):
            self.ledData[i].setRGB(r,g,b)
    def rainbow(self):
        # For every pixel
        for i in range(kLEDBuffer):
            # Calculate the hue - hue is easier for rainbows because the color
            # shape is a circle so only one value needs to precess
            hue = (self.rainbowFirstPixelHue + (i * 180 / kLEDBuffer)) % 180

            # Set the value
            self.ledData[i].setHSV(int(hue), 255, 128)

        # Increase by to make the rainbow "move"
        self.rainbowFirstPixelHue += 3
        # Check bounds
        self.rainbowFirstPixelHue %= 180
    def periodic(self) -> None:
        self.led.setData(self.ledData)
        return super().periodic()
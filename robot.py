import wpilib
from wpilib.drive import DifferentialDrive
import commands2
from container import RobotContainer
from subsystem.led import LED
class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self):
        self.led = LED()
        self.container = RobotContainer(self)
        self.drive = self.container.drive_subsystem
        self.autonomousCommand = self.container.getAutonomousCommand()
    def autonomousInit(self):
        self.autonomousCommand = self.container.getAutonomousCommand()
        self.container.drive_subsystem.setStartingPose(self.container.auton_chooser)
        if self.autonomousCommand:
            print("valid autonomous command")
            self.autonomousCommand.schedule()
    def disabledInit(self) -> None:
        self.led.rainbow()
        return super().disabledInit()
    def autonomousPeriodic(self):
        #print(self.container.drive_subsystem.getWheelSpeeds())
        self.led.setledrgb(255,0,0)
    def teleopInit(self) -> None:
        if self.autonomousCommand:
            self.autonomousCommand.cancel()
    def teleopPeriodic(self):
        self.container.balanceCommand.periodic()
        self.led.setledrgb(0,0,255)
if __name__ == '__main__':
    wpilib.run(MyRobot)    

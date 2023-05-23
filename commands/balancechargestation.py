import commands2
import wpimath.controller
import wpilib
from subsystem.drive import drive as DriveSubsystem

from contants import DriveConstants

class BalanceChargeStation(commands2.PIDCommand):

    def __init__(self, drive_subsystem: DriveSubsystem):
        self.drive_subsystem = drive_subsystem
        super().__init__(
            wpimath.controller.PIDController(
                DriveConstants.kPBalance, DriveConstants.kIBalance, DriveConstants.kDBalance
            ),
            lambda: drive_subsystem.gyro.getGyroAngleY(),  # PID kontrolcüsünün geribildirim olarak kullandığı değer
            0,  # PID kontrolcüsünün set noktası
            lambda volts: self.drive_subsystem.voltDrive(volts, volts),  # PID kontrolcüsünden gelen çıkışın kullanıldığı kısım
            [drive_subsystem]  # Kullanılan alt sistemlerin listesi
        )
        self.getController().setTolerance(5)  # PID kontrolcüsünün hata payı belirlenir
        wpilib.SmartDashboard.putData("BalanceChargeStationPID", self.getController())  # PID kontrolcüsü SmartDashboard'a eklenir

        wpilib.Preferences.initFloat("kP", 0)  # P sabiti için önbellek değeri belirlenir
        wpilib.Preferences.initFloat("kI", 0)  # I sabiti için önbellek değeri belirlenir
        wpilib.Preferences.initFloat("kD", 0)  # D sabiti için önbellek değeri belirlenir

    def atSetpoint(self) -> bool:
        return self.getController().atSetpoint()  # PID kontrolcüsü set noktasına ulaşıldığında True döner

    def periodic(self):
        # SmartDashboard üzerinden P, I, D sabitlerinin değiştirilip değiştirilmediği kontrol edilir ve gerekirse güncellenir
        if wpilib.Preferences.getFloat("kP", 0) != self.getController().getP():
            self._controller.setP(wpilib.Preferences.getFloat("kP", 0))
        
        if wpilib.Preferences.getFloat("kI", 0) != self.getController().getI():
            self._controller.setI(wpilib.Preferences.getFloat("kI", 0))

        if wpilib.Preferences.getFloat("kD", 0) != self.getController().getD():
            self._controller.setD(wpilib.Preferences.getFloat("kD", 0))

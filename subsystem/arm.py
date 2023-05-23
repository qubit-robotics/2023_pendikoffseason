import wpilib
import wpimath.controller
import rev
import commands2
import enum
from wpilib import SmartDashboard
class Mode(enum.auto):
    CUBE = "cube"
    CONE = "cone"

class PWR(enum.auto):
    HOLD = 0.2
    SWALLOW = 0.5
    SPIT = -0.3

class ARM(commands2.PIDSubsystem):
    def __init__(self):
        super().__init__(
            wpimath.controller.PIDController(
                6,
                0,
                0
            ),
            0
        )
        # kol motoru 10 numaralı CAN SparkMax motor kontrolcüsüne tanımlanıyor.
        self.motor_angle = rev.CANSparkMax(10, rev.CANSparkMax.MotorType.kBrushless)
        # kol encoderi tanımlanıyor.
        self.motor_angleEncoder = self.motor_angle.getEncoder()
        # gripper motoru 3 numaralı PWM SparkMax motor kontrolcüsüne tanımlanıyor.
        self.motor_gripper = wpilib.PWMSparkMax(3)
        # PID denetleyicisi etkinleştiriliyor.
        self.enable()
        
    # yukarı bölme için setpoint değeri 1.7 olacak şekilde PID denetleyicisinin setpoint'i ayarlanıyor.
    def topRow(self):
        self.setSetpoint(1.7)
    
    # orta bölme için setpoint değeri 0.9 olacak şekilde PID denetleyicisinin setpoint'i ayarlanıyor.
    def midRow(self):
        self.setSetpoint(0.9)
    
    # setpoint değeri 0 olacak şekilde PID denetleyicisinin setpoint'i ayarlanıyor.
    def retract(self):
        self.setSetpoint(0)
    
    # human player'den küp almak için setpoint değeri 1.25 olacak şekilde PID denetleyicisinin setpoint'i ayarlanıyor.
    def humanPlayerCube(self):
        self.setSetpoint(1.25)
    
    # human player'den koni almak setpoint değeri 1.35 olacak şekilde PID denetleyicisinin setpoint'i ayarlanıyor.
    def humanPlayerCone(self):
        self.setSetpoint(1.35)
    
    # Encoder okunarak kolun mevcut pozisyon değeri alınıyor.
    def _getMeasurement(self) -> float:
        SmartDashboard.putNumber("armPidPos", self.motor_angleEncoder.getPosition())
        return self.motor_angleEncoder.getPosition()
    
    # PID denetleyicisinin çıkışı kullanılarak motor kontrolcüsüne PWM sinyali gönderiliyor.
    def _useOutput(self, output: float, setpoint: float) -> None:
        #print("output voltage", output)
        self.motor_angle.setVoltage(output)
        SmartDashboard.putNumber("armPidOut", output)
    
    # PID denetleyicisi devre dışı bırakılıyor.
    def disable(self) -> None:
        print("disable")
        SmartDashboard.putBoolean("ArmPIDStatus", False)
        return super().disable()
    
    # PID denetleyicisi etkinleştiriliyor.
    def enable(self) -> None:
        print("enable")
        SmartDashboard.putBoolean("ArmPIDStatus", True)
        return super().enable()
    
    # Motoru manuel olarak yukarı kaldıran bir gerilim değeri uygulanıyor.
    def raiseArmManual(self):
        print("manual raise")
        self.motor_angle.setVoltage(2)
    
    # Motoru manuel olarak geri çeken bir gerilim değeri uygulanıyor.
    def retractArmManual(self):
        print("manual retract")
        self.motor_angle.setVoltage(-2)
    
    # Motorun durmasını sağlayan bir gerilim değeri uygulanıyor.
    def stopArmManual(self):
        print("manual stop")
        self.motor_angle.set(0)
    
    # gripper motoruna intake voltajı veriliyor.
    def swallow(self):
        print("swallowing")
        self.motor_gripper.set(PWR.SWALLOW)
    
    # gripper motoruna bırakma voltajı veriliyor.
    def spit(self):
        print("spitting")
        self.motor_gripper.set(PWR.SPIT)
    
    # gripper motoruna sabit tutma voltajı veriliyor.
    def hold(self):
        self.motor_gripper.set(PWR.HOLD)
    
    # gripper motoruna 0 değeri verilerek intake durduruluyor.
    def stopIntake(self):
        print("no intake power")
        self.motor_gripper.set(0)

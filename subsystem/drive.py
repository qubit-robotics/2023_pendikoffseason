from wpilib.drive import DifferentialDrive
import wpilib
import wpimath.estimator, wpimath.geometry, wpimath.kinematics
import wpimath
import commands2
from rev import CANSparkMax
import rev
from contants import DriveConstants
import commands2
import qsparkmax
from subsystem.cam import CamSubsystem
from hud.autonchooser import AutonChooser

class drive(commands2.SubsystemBase):
    def __init__(self, MyRobot: commands2.TimedCommandRobot) -> None:

        super().__init__()
        self.Robot = MyRobot
        
        # Motorlar
        self.motor_frontLeft = qsparkmax.Qubit_CANSparkMax(1, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        self.motor_rearLeft = qsparkmax.Qubit_CANSparkMax(2, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        self.motor_frontRight = qsparkmax.Qubit_CANSparkMax(3, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        self.motor_rearRight = qsparkmax.Qubit_CANSparkMax(4, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        
        # Encoderlar
        self.motor_frontLeftEncoder = self.motor_frontLeft.getEncoder()
        self.motor_rearLeftEncoder = self.motor_rearLeft.getEncoder()
        self.motor_frontRightEncoder = self.motor_frontRight.getEncoder()
        self.motor_rearRightEncoder = self.motor_rearRight.getEncoder()
        
        # Encoderlar için dönüşüm değerleri 
        conversion_factor = 0.0446812324929972
        self.motor_frontLeftEncoder.setPositionConversionFactor(conversion_factor)
        self.motor_frontLeftEncoder.setVelocityConversionFactor(conversion_factor)
        self.motor_rearLeftEncoder.setPositionConversionFactor(conversion_factor)
        self.motor_rearLeftEncoder.setVelocityConversionFactor(conversion_factor)
        self.motor_frontRightEncoder.setPositionConversionFactor(conversion_factor)
        self.motor_frontRightEncoder.setVelocityConversionFactor(conversion_factor)
        self.motor_rearRightEncoder.setPositionConversionFactor(conversion_factor)
        self.motor_rearRightEncoder.setVelocityConversionFactor(conversion_factor)
        
        # Gyro sensörü
        self.gyro = wpilib.ADIS16448_IMU()
        self.gyro.calibrate()
        self.gyro.reset()
        
        # Kinematik ve konum tahminleyici
        self.kinematics = DriveConstants.kinematics
        self.estimator = wpimath.estimator.DifferentialDrivePoseEstimator(
            self.kinematics,
            wpimath.geometry.Rotation2d.fromDegrees(-self.gyro.getAngle()),
            (self.motor_frontLeftEncoder.getPosition() + self.motor_rearLeftEncoder.getPosition()) / 2,
            (self.motor_frontRightEncoder.getPosition() + self.motor_rearRightEncoder.getPosition()) / 2,
            DriveConstants.kStartingPose
        )
        
        self.lastPose = DriveConstants.kStartingPose
        self.last_camEstimatedPose = wpimath.geometry.Pose3d()
        
        # Alan görüntüsü
        self.field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("estimatorField", self.field)
        # Sol ve sağ motor grupları
        self.left_group = wpilib.MotorControllerGroup(self.motor_frontLeft, self.motor_rearLeft)
        self.right_group = wpilib.MotorControllerGroup(self.motor_frontRight, self.motor_rearRight)
        
        # DifferentialDrive
        self.drive = DifferentialDrive(self.left_group, self.right_group)
    
    def calibrate(self):
        """
        Motor encoderları ve gyro sensörünü sıfırlar.
        """
        self.motor_frontLeftEncoder.setPosition(0)
        self.motor_frontRightEncoder.setPosition(0)
        self.motor_rearLeftEncoder.setPosition(0)
        self.motor_rearRightEncoder.setPosition(0)
        self.gyro.reset()
    
    def getWheelSpeeds(self):
        """
        Tekerlek hızlarını döndürür.
        """
        if self.Robot.isSimulation():
            speeds = wpimath.kinematics.DifferentialDriveWheelSpeeds(
                (self.motor_frontLeft.getSimVelocity() + self.motor_rearLeft.getSimVelocity()) / 2,
                (self.motor_frontRight.getSimVelocity() + self.motor_rearRight.getSimVelocity()) / 2
            )
        else:
            speeds = wpimath.kinematics.DifferentialDriveWheelSpeeds(
                (self.motor_frontLeftEncoder.getVelocity() + self.motor_rearLeftEncoder.getVelocity()) / 2,
                (self.motor_frontRightEncoder.getVelocity() + self.motor_rearRightEncoder.getVelocity()) / 2
            )
        return speeds
    
    def updateEstimator(self):
        """
        Tahminleyiciyi günceller.
        """
        self.lastPose = self.estimator.update(
            wpimath.geometry.Rotation2d.fromDegrees(-self.gyro.getAngle()),
            (self.motor_frontLeftEncoder.getPosition() + self.motor_rearLeftEncoder.getPosition()) / 2,
            (self.motor_frontRightEncoder.getPosition() + self.motor_rearRightEncoder.getPosition()) / 2
        )
        self.field.setRobotPose(self.estimator.getEstimatedPosition())
    
    def getEstimatedPose(self):
        """
        Tahmin edilen konumu döndürür.
        """
        return self.lastPose
    
    def voltDrive(self, leftVolts, rightVolts):
        """
        Voltaj değeriyle hareketi sağlar.
        """
        self.left_group.setVoltage(leftVolts)
        self.right_group.setVoltage(rightVolts)
        self.drive.feed()
    
    def periodic(self) -> None:
        self.updateEstimator()
    
    def setStartingPose(self, auton_chooser: AutonChooser):
        """
        Maçın başında Shuffleboard üzerinden başlangıç pozisyonunu ayarlar.
        """
        trajectory = auton_chooser.generatePath()
        
        if trajectory != wpimath.trajectory.Trajectory():
            trajectory_initial = trajectory.initialPose()
            self.estimator.resetPosition(
                wpimath.geometry.Rotation2d.fromDegrees(-self.gyro.getAngle()),
                0,
                 0,
                trajectory_initial
            )

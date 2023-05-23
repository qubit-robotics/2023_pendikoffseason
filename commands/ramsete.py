import commands2
import wpimath.controller
import wpimath.trajectory
import wpimath.trajectory.constraint
import wpimath.geometry
from wpilib import SmartDashboard

from contants import DriveConstants
from subsystem.drive import drive as DriveSubsystem


class PathCommand:
    def __init__(self, drive_subsystem: DriveSubsystem, path: wpimath.trajectory.Trajectory):
        """
        PathCommand sınıfı, robotun belirli bir yol üzerinde hareket etmesini sağlar.

        :param drive_subsystem: sürüş subsysteminin referansını tutar.
        :param path: wpimath.trajectory.Trajectory türünde bir yol nesnesi, robotun takip edeceği yolun tanımını içerir.
        """
        # Otomatik gerilim kısıtlaması için DifferentialDriveVoltageConstraint oluşturulur.
        self.autoVoltageConstraint = (
            wpimath.trajectory.constraint.DifferentialDriveVoltageConstraint(
                wpimath.controller.SimpleMotorFeedforwardMeters(
                    DriveConstants.ksVolts,
                    DriveConstants.kvVoltSecondsPerMeter,
                    DriveConstants.kaVoltSecondsSquaredPerMeter,
                ),
                DriveConstants.kinematics,
                DriveConstants.kMaxVoltsRamsete,
            )
        )

        # Yörünge konfigürasyonunda max değerler tanımlanır.
        self.config = wpimath.trajectory.TrajectoryConfig(
            DriveConstants.kMaxSpeedMetersPerSecond,
            DriveConstants.kMaxAccelerationMetersPerSecondSquared,
        )

        # Robotun kinematik modelini ayarlanır
        self.config.setKinematics(DriveConstants.kinematics)

        # Yörüngeye uygulanacak kısıtlamaları eklenir
        self.config.addConstraint(self.autoVoltageConstraint)

        # Başlangıç konumu tanımlanır.
        self.initialPosition = wpimath.geometry.Pose2d()

        # Hareket noktaları tanımlanır.
        self.movements = [
            wpimath.geometry.Translation2d(x=1, y=1),
        ]

        # Son konum tanımlanır.
        self.finalPosition = wpimath.geometry.Pose2d(
            wpimath.geometry.Translation2d(x=2, y=-1), wpimath.geometry.Rotation2d(0)
        )

        # Örnek yörünge oluşturulur.
        self.exampleTrajectory = (
            wpimath.trajectory.TrajectoryGenerator.generateTrajectory(
                self.initialPosition, self.movements, self.finalPosition, self.config
            )
        )

        # Belirtilen yörüngeyi kullanarak Ramsete Komutu oluşturulur.
        self.trajectory = path
        self.ramseteCommand = commands2.RamseteCommand(
            self.trajectory,  # Takip edilecek yörünge
            drive_subsystem.getEstimatedPose,  # Robotun tahmini konumunu döndüren fonksiyon
            wpimath.controller.RamseteController(b=2, zeta=0.7),  # Ramsete kontrolcüsü
            wpimath.controller.SimpleMotorFeedforwardMeters(
                DriveConstants.ksVolts,
                DriveConstants.kvVoltSecondsPerMeter,
                DriveConstants.kaVoltSecondsSquaredPerMeter,
            ),  # FeedForward değerleri
            DriveConstants.kinematics,  # Robotun kinematik modeli
            drive_subsystem.getWheelSpeeds,  # Tekerlek hızlarını döndüren fonksiyon
            wpimath.controller.PIDController(DriveConstants.kPDriveVel, 0, 0),  # Hız PID kontrolcüsü
            wpimath.controller.PIDController(DriveConstants.kPDriveVel, 0, 0),  # Hız PID kontrolcüsü
            drive_subsystem.voltDrive,  # Voltajla sürüş fonksiyonu
            [drive_subsystem],  # kullanılan subsystem
        )

    def getRamseteCommand(self):
        #Oluşturulan Ramsete Komutunu döndürür.
        return self.ramseteCommand

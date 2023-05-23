import commands2
import wpilib
from wpilib import SmartDashboard
import wpimath.trajectory

class AutonChooser(commands2.SubsystemBase):

    def __init__(self) -> None:

        super().__init__()

        # Tag seçici oluşturulur ve seçenekler eklenir
        self.tagchooser = wpilib.SendableChooser()
        self.tagchooser.addOption("1",  "paths/output/Path1.wpilib.json")
        self.tagchooser.addOption("2",  "paths/output/Path2.wpilib.json")
        self.tagchooser.addOption("3",  "paths/output/Path3.wpilib.json")


        # Varsayılan seçenekler belirlenir
        self.tagchooser.setDefaultOption("None", None)

        # Son seçim değişkenleri tanımlanır
        self.last_tagchoice = None

        # Seçim işlemleri SmartDashboard'a eklenir
        SmartDashboard.putData("tagchooser", self.tagchooser)

    def generatePath(self) -> wpimath.trajectory.Trajectory:

        """
        RamseteCommand'a geçirilebilecek bir path oluşturur.
        
        """
        # Seçimler alınır
        self.tagchoice = self.tagchooser.getSelected()
        self.last_tagchoice = self.last_tagchoice
        print(self.tagchoice, wpilib.DriverStation.getAlliance())
        if (self.tagchoice != None):
            # Belirli bir tag ve mobility seçildiyse ilgili path oluşturulur
            return wpimath.trajectory.TrajectoryUtil.fromPathweaverJson(f"{self.tagchoice}")
        
        else:
            # Seçim yapılmadıysa veya tag/mobility seçimi pathlare uyumsuzsa varsayılan path oluşturulur
            if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kBlue:
                return wpimath.trajectory.TrajectoryUtil.fromPathweaverJson("paths\output\a.json")
            elif wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kRed:
                return wpimath.trajectory.TrajectoryUtil.fromPathweaverJson("paths\output\a.json")
            else:
                return wpimath.trajectory.Trajectory()

    def hasModeChanged(self) -> bool:
        
        """
        path oluşturma işleminden sonra modun değişip değişmediğini kontrol eder.
        """

        if (self.tagchooser.getSelected() != self.last_tagchoice):
            return True
        else:
            return False

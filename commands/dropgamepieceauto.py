import commands2
import commands2.cmd
import wpilib

from subsystem.arm import ARM 

class DropGamePieceAuto(commands2.SequentialCommandGroup):

    def __init__(self, arm_subsystem: ARM):
        self.arm_subsystem = arm_subsystem

        # Kolun uzatılması için bir komut oluşturulur
        self.extendCommand = commands2.cmd.runOnce(
            lambda: self.arm_subsystem.topRow(), [self.arm_subsystem]
        )

        # Uzatma işlemi sonrası beklemek için bir bekleme komutu oluşturulur
        self.waitForExtend = commands2.WaitCommand(1.5)

        # Oyuncak bırakma işlemi için bir komut oluşturulur
        self.spitCommand = commands2.cmd.runOnce(
            lambda: self.arm_subsystem.spit(), [self.arm_subsystem]
        )

        # Bırakma işleminden sonra beklemek için bir bekleme komutu oluşturulur
        self.waitForSpit = commands2.WaitCommand(1)

        # Kolun geri çekilmesi için bir komut oluşturulur
        self.retractCommand = commands2.cmd.runOnce(
            lambda: self.arm_subsystem.retract(), [self.arm_subsystem]
        )
        
        # Geri çekme işleminden sonra beklemek için bir bekleme komutu oluşturulur
        self.waitForRetract = commands2.WaitCommand(1.5)

        super().__init__(
            self.extendCommand,
            self.waitForExtend,
            self.spitCommand,
            self.waitForSpit,
            self.retractCommand,
            self.waitForRetract
        )

import photonvision
import wpimath.geometry
import robotpy_apriltag
import commands2

from contants import SimCameraConstants

class CamSubsystem(commands2.SubsystemBase):

    # Reference Pose3d for intelliSense to autocomplete

    def __init__(self):
        super().__init__()
        self.cam = photonvision.PhotonCamera("camera")
    
    
    def getBestTargetTransform(self) -> int and wpimath.geometry.Transform3d:
        if self.cam.hasTargets():
            return self.cam.getLatestResult().getBestTarget().getFiducialId(), self.cam.getLatestResult().getBestTarget().getBestCameraToTarget()
    
    def getLatencyMillis(self) -> float:
        if self.cam.hasTargets():
            return self.cam.getLatestResult().getLatency()
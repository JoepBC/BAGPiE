from ease import *
from bagpie import *


class Operation(IOperation):

    # Some static arrays with operations to perform
    operationOnAnimationCalls = []
    operationOnEveryFrameCalls = []

    def __init__(self, attachEasesToAnimation=True, scaleToAnimationDimensions=True) -> None:
        self._progressFrame = 0
        self.attachEasesToAnimation = attachEasesToAnimation
        self.scaleToAnimationDimensions = scaleToAnimationDimensions
        self.eases: Dict[Ease] = {}

    def getProgress(self):
        return self._progressFrame.fraction()

    def perform(self, onAnimation: BAGPiE):
        # The default operation called by the AniMather object
        self.drawOnAnimation(onAnimation)

        # Possible added operations
        for opCall in Operation.operationOnAnimationCalls:
            opCall(onAnimation)

        # Operations on individual frames
        self.performOnAllFrames(onAnimation)

    def performOnAllFrames(self, onAnimation: BAGPiE):
        for frame in onAnimation.frames:
            self._progressFrame = frame
            self.drawOnFrame(frame)
            for operation in Operation.operationOnEveryFrameCalls:
                operation(frame)

    def drawOnAnimation(self, animation: BAGPiE):
        """! 
        Empty method, available for implementation at subclass
        @param animation: the animation to be modified
        """
        pass

    def drawOnFrame(self, frame: Frame):
        """! 
        Empty method, available for implementation at subclass
        @param frame: the frame to be modified
        """
        pass

    def _performAttachEasesToAnimation(self, animation: BAGPiE):
        for index in self.eases:
            self.eases[index].setFractionFunc(self.getProgress)

    def _performScaleToAnimationDimensions(self, animation: BAGPiE):
        self.setScaleFactors(animation.dimensions[0], animation.dimensions[1])

    def drawOnAnimation(self, animation: BAGPiE):
        if (self.attachEasesToAnimation):
            self._performAttachEasesToAnimation(animation)
        if (self.scaleToAnimationDimensions):
            self._performScaleToAnimationDimensions(animation)

    def setScaleFactors(self, x: float, y: float):
        raise Exception("Subclass responsibility")

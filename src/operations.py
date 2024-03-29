from relaters import *
from bagpie import *


class Operation(IOperation):

    # Some static arrays with operations to perform
    operationOnAnimationCalls = []
    operationOnEveryFrameCalls = []

    def __init__(self, attachRelatersToAnimation=True, scaleToAnimationDimensions=True) -> None:
        super().__init__()
        self._progressFrame = None
        self.attachRelatersToAnimation = attachRelatersToAnimation
        self.scaleToAnimationDimensions = scaleToAnimationDimensions
        self.relaters: Dict[Relater] = {}

    def getProgress(self):
        return self._progressFrame.fraction()

    def perform(self, onAnimation: BAGPiE):
        print("\n"+self.__class__.__name__+">")
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
            if not self.shouldOperateOnFrame(frame.id):
                continue
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
        # Printing frame ID's as a progress indicator
        print(str(frame.id), end='-')

    def _performAttachRelatersToAnimation(self, animation: BAGPiE):
        for index in self.relaters:
            self.relaters[index].setFractionFunc(self.getProgress)

    def _performScaleToAnimationDimensions(self, animation: BAGPiE):
        self.setScaleFactors(animation.dimensions[0], animation.dimensions[1])

    def drawOnAnimation(self, animation: BAGPiE):
        if (self.attachRelatersToAnimation):
            self._performAttachRelatersToAnimation(animation)
        if (self.scaleToAnimationDimensions):
            self._performScaleToAnimationDimensions(animation)

        """ When Relaters are translated from fractions to pixels, it must be defined
            whether they should be related to the horizontal or vertical axis.
        """ 
    def setScaleFactors(self, x: float, y: float):
        raise Exception("Subclass responsibility")

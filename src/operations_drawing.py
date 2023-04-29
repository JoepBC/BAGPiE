from operations import *

class CircleOperation(Operation):

    def __init__(self, x: float | Ease = 0.5, y: float | Ease = 0.5, color=(255, 255, 255), radius: float | Ease = 0.5,
                 attachEasesToAnimation=True, scaleToAnimationDimensions=True) -> None:
        super().__init__(attachEasesToAnimation=attachEasesToAnimation,
                         scaleToAnimationDimensions=scaleToAnimationDimensions)
        self.eases['x'] = AbstractEaser.Ensure(x)
        self.eases['y'] = AbstractEaser.Ensure(y)
        self.eases['radius'] = AbstractEaser.Ensure(radius)
        self.eases['color'] = AbstractEaser.Ensure(color)

    def setScaleFactors(self,  x:float, y:float):
        self.eases['x'].factor = x
        self.eases['y'].factor = y
        self.eases['radius'].factor = max(x,y)

    def drawOnFrame(self, frame: Frame):
        # Printing frame ID's as a progress indicator
        print(str(frame.id), end='-')
        frame.circle(self.eases['x'].value(), self.eases['y'].value(),
                     self.eases['radius'].value(), self.eases['color'].intsValue())


class SnakeOperation(CircleOperation):
    def __init__(self, x: float | Ease = 0.5, y: float | Ease = 0.5, color=(255, 255, 255), radius: float | Ease = 0.5,
                 attachEasesToAnimation=True, scaleToAnimationDimensions=True,
                 tailLength: int | Ease = 5
                 ) -> None:
        super().__init__(x, y, color, radius, attachEasesToAnimation, scaleToAnimationDimensions)
        self.tailLength = AbstractEaser.Ensure(tailLength)

    def drawOnFrame(self, frame: Frame, tail: int = None, tailFrame: Frame = None):
        if (tail is None):
            print(str(frame.id), end='-')
            tail = self.tailLength.value(frame.fraction())
            tailFrame = frame
        # Printing frame ID's as a progress indicator
        tailFraction = tailFrame.fraction()
        self._progressFrame.circle(self.eases['x'].value(tailFraction), self.eases['y'].value(tailFraction),
                                   self.eases['radius'].value(tailFraction), self.eases['color'].intsValue(tailFraction))
        if (tail > 0 and tailFrame.hasPrevious()):
            self.drawOnFrame(frame, tail-1, tailFrame.previous())

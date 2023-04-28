from operations import *

class CircleOperation(Operation):

    def __init__(self, x: float | Ease = 0.5, y: float | Ease = 0.5, color=(255, 255, 255), radius: float | Ease = 0.5,
                 attachEasesToAnimation=True, scaleToAnimationDimensions=True) -> None:
        super().__init__(attachEasesToAnimation=attachEasesToAnimation,
                         scaleToAnimationDimensions=scaleToAnimationDimensions)
        self.x = AbstractEaser.Ensure(x)
        self.y = AbstractEaser.Ensure(y)
        self.radius = AbstractEaser.Ensure(radius)
        self.color = AbstractEaser.Ensure(color)

    def setScaleFactors(self, dimsFac: tuple[float, float]):
        self.x.factor = dimsFac[0]
        self.y.factor = dimsFac[1]
        self.radius.factor = max(dimsFac[0], dimsFac[1])

    def getAllEases(self):
        return [self.x, self.y, self.radius, self.color]

    def drawOnFrame(self, frame: Frame):
        # Printing frame ID's as a progress indicator
        print(str(frame.id), end='-')
        frame.circle(self.x.value(), self.y.value(),
                     self.radius.value(), self.color.intsValue())


class SnakeOperation(CircleOperation):
    def __init__(self, x: float | Ease = 0.5, y: float | Ease = 0.5, color=(255, 255, 255), radius: float | Ease = 0.5,
                 attachEasesToAnimation=True, scaleToAnimationDimensions=True,
                 tailLength: int | Ease = 5
                 ) -> None:
        super().__init__(x, y, color, radius, attachEasesToAnimation, scaleToAnimationDimensions)
        self.tailLength = AbstractEaser.Ensure(tailLength)

    def getAllEases(self):
        return [*super().getAllEases(), self.tailLength]

    def drawOnFrame(self, frame: Frame, tail: int = None, tailFrame: Frame = None):
        if (tail is None):
            print(str(frame.id), end='-')
            tail = self.tailLength.value(frame.fraction())
            tailFrame = frame
        # Printing frame ID's as a progress indicator
        tailFraction = tailFrame.fraction()
        self._progressFrame.circle(self.x.value(tailFraction), self.y.value(tailFraction),
                                   self.radius.value(tailFraction), self.color.intsValue(tailFraction))
        if (tail > 0 and tailFrame.hasPrevious()):
            self.drawOnFrame(frame, tail-1, tailFrame.previous())

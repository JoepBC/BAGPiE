from bagpie import Frame
from operations import *


class LineOperation(Operation):
    def __init__(self, x1: float, y1: float, x2: float, y2: float, color=(255, 255, 255),
                 attachRelatersToAnimation=True, scaleToAnimationDimensions=True) -> None:
        super().__init__(attachRelatersToAnimation=attachRelatersToAnimation,
                         scaleToAnimationDimensions=scaleToAnimationDimensions)
        self.relaters['x1'] = AbstractRelater.Ensure(x1)
        self.relaters['y1'] = AbstractRelater.Ensure(y1)
        self.relaters['x2'] = AbstractRelater.Ensure(x2)
        self.relaters['y2'] = AbstractRelater.Ensure(y2)
        self.relaters['color'] = AbstractRelater.Ensure(color)

    def setScaleFactors(self, x: float, y: float):
        self.relaters['x1'].factor = x
        self.relaters['y1'].factor = y
        self.relaters['x2'].factor = x
        self.relaters['y2'].factor = y

    def drawOnFrame(self, frame: Frame):
        print("DL"+str(frame.id))
        frame.line(self.relaters['x1'].value(), self.relaters['y1'].value(),
                   self.relaters['x2'].value(), self.relaters['y2'].value(), self.relaters['color'].intsValue())


class CircleOperation(Operation):

    def __init__(self, x: float | Relater = 0.5, y: float | Relater = 0.5, color=(255, 255, 255), radius: float | Relater = 0.5,
                 attachRelatersToAnimation=True, scaleToAnimationDimensions=True) -> None:
        super().__init__(attachRelatersToAnimation=attachRelatersToAnimation,
                         scaleToAnimationDimensions=scaleToAnimationDimensions)
        self.relaters['x'] = AbstractRelater.Ensure(x)
        self.relaters['y'] = AbstractRelater.Ensure(y)
        self.relaters['radius'] = AbstractRelater.Ensure(radius)
        self.relaters['color'] = AbstractRelater.Ensure(color)

    def setScaleFactors(self, x: float, y: float):
        self.relaters['x'].factor = x
        self.relaters['y'].factor = y
        self.relaters['radius'].factor = max(x, y)

    def drawOnFrame(self, frame: Frame):
        frame.circle(self.relaters['x'].value(), self.relaters['y'].value(),
                     self.relaters['radius'].value(), self.relaters['color'].intsValue())


class SnakeOperation(CircleOperation):
    def __init__(self, x: float | Relater = 0.5, y: float | Relater = 0.5, color=(255, 255, 255), radius: float | Relater = 0.5,
                 attachRelatersToAnimation=True, scaleToAnimationDimensions=True,
                 tailLength: int | Relater = 5
                 ) -> None:
        super().__init__(x, y, color, radius,
                         attachRelatersToAnimation, scaleToAnimationDimensions)
        self.tailLength = AbstractRelater.Ensure(tailLength)

    def drawOnFrame(self, frame: Frame, tail: int = None, tailFrame: Frame = None):
        if (tail is None):
            print(str(frame.id), end='-')
            tail = self.tailLength.value(frame.fraction())
            tailFrame = frame
        # Printing frame ID's as a progress indicator
        tailFraction = tailFrame.fraction()
        self._progressFrame.circle(self.relaters['x'].value(tailFraction), self.relaters['y'].value(tailFraction),
                                   self.relaters['radius'].value(tailFraction), self.relaters['color'].intsValue(tailFraction))
        if (tail > 0 and tailFrame.hasPrevious()):
            self.drawOnFrame(frame, tail-1, tailFrame.previous())

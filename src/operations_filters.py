from bagpie import Frame
from operations import *
import numpy as np

import scipy.ndimage


class ConvoluteOperation(Operation):

    def __init__(self, maskMatrix=[[0, 0, 0], [0, 1, 0], [0, 0, 0]], attachRelatersToAnimation=True, scaleToAnimationDimensions=True) -> None:
        super().__init__(attachRelatersToAnimation, scaleToAnimationDimensions)
        self.mask = maskMatrix

    def drawOnFrame(self, frame: Frame):
        Operation.drawOnFrame(self, frame)
        ar = np.array(frame.im)
        # RED: ar[:,:,0] - #GREEN: ar[:,:,1] - #BLUE: ar[:,:,2]
        for convolveIndex in range(3):
            ar[:, :, convolveIndex] = scipy.ndimage.convolve(
                ar[:, :, convolveIndex], self.mask)
        frame.im = Image.fromarray(ar)

    def setScaleFactors(self, x: float, y: float):
        pass


class DeriveRight(ConvoluteOperation):
    def __init__(self, maskMatrix=[[-1, 1]]) -> None:
        super().__init__(maskMatrix)


class DeriveLeft(ConvoluteOperation):
    def __init__(self, maskMatrix=[[1, -1]]) -> None:
        super().__init__(maskMatrix)


class Blur3x3(ConvoluteOperation):
    def __init__(self, maskMatrix=[[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]) -> None:
        super().__init__(maskMatrix)


class Blur3x3NoCenter(ConvoluteOperation):
    def __init__(self, maskMatrix=[[1/8, 1/8, 1/8], [1/8, 0, 1/8], [1/8, 1/8, 1/8]]) -> None:
        super().__init__(maskMatrix)


class ReRastarized(Operation):


    def __init__(self, xRes = 20, yRes=20, rgbFrames=[True, True, True],
                 attachRelatersToAnimation=True, scaleToAnimationDimensions=True) -> None:
        super().__init__(attachRelatersToAnimation, scaleToAnimationDimensions)
        self.rgbFrames = rgbFrames
        self.xRes = xRes
        self.yRes = yRes

    def drawOnFrame(self, frame: Frame):
        Operation.drawOnFrame(self, frame)
        ar = np.array(frame.im)
        for colour in range(3):
            if not self.rgbFrames[colour]:
                continue
            [width, height] = frame.parent.dimensions
            ar[:,:,colour] = self.toBaseTable(self.toBaseTable(ar[:,:,colour], self.xRes, self.yRes), width, height)
            frame.im = Image.fromarray(ar)

    def toBaseTable(self, aTable, xRes, yRes):
        """ Create a new table, with resolution xRes; yRes, based on aTable """
        tWidth = len(aTable[0])
     #  if (tWidth < xRes): raise ValueError(str(tWidth)+"<"+str(xRes))
        txStep = tWidth / xRes
        tHeight = len(aTable)
     #  if (tHeight < yRes): raise ValueError(str(tHeight)+"<"+str(yRes))
        tyStep = tHeight / yRes
        newTable = np.zeros(shape=(yRes, xRes))
        for iX in range (0, xRes):
            x1 = round(txStep*iX)
            x2 = round(txStep*(iX+1))
            if (x1 >= tWidth): x1 = tWidth-1 # don't exceed boundaries due to rounding
            if x1 == x2: x2 = x1+1 # have at least a single cell for averaging

            for iY in range (0, yRes):
                y1 = round(tyStep*iY)
                y2 = round(tyStep*(iY+1))
                #print("yres/y1y2-xres/x1x2--"+str(yRes)+"/"+str(y1)+";"+str(y2)+";--"+str(xRes)+"/"+str(x1)+";"+str(x2))
                if (y1 >= tHeight): y1 = tHeight-1 # don't exceed boundaries due to rounding
                if y1 == y2: y2 = y1+1 # have at least a single cell for averaging
                tabSec = aTable[y1:y2,x1:x2]
                newTable[iY, iX] = np.average(tabSec)
        return newTable

    def setScaleFactors(self, x: float, y: float):
        pass

class ConwaysGameOfLife(ReRastarized):

    def __init__(self, xRes=9 ^ 2, yRes=9 ^ 2, rgbFrames=[True, True, True], threshold=128, negated=False,
                 attachRelatersToAnimation=True, scaleToAnimationDimensions=True) -> None:
        super().__init__(xRes, yRes, rgbFrames, attachRelatersToAnimation, scaleToAnimationDimensions)

    
    def drawOnFrame(self, frame: Frame):
        """ Conway can only draw when a previous frame exists"""
        if (not frame.hasPrevious()):
            return

        Operation.drawOnFrame(self, frame)
        # base on previous frame
        ar = np.array(frame.previous.im)
        for colour in range(3):
            if not self.rgbFrames[colour]:
                continue
            fromBase = self.toBaseTable[:, :, colour]

        # RED: ar[:,:,0] - #GREEN: ar[:,:,1] - #BLUE: ar[:,:,2]
        for convolveIndex in range(3):
            ar[:, :, convolveIndex] = scipy.ndimage.convolve(
                ar[:, :, convolveIndex], self.mask)
        frame.im = Image.fromarray(ar)


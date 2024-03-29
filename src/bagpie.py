#!/bin/python3

from PIL import Image, ImageDraw
import numpy as np
from typing import List, Dict
import math
import warnings


class IOperation:

    def __init__(self):
        # First frame to include
        self.fromFrame = -1
        # Last frame to include
        self.toFrame = -1

    def setToFrame(self, toFrame: int):
        self.toFrame = toFrame
        return self

    def setFromFrame(self, fromFrame: int):
        self.fromFrame = fromFrame
        return self

    def perform(self, onAnimation: 'BAGPiE'):
        # The default operation
        pass

    def shouldOperateOnFrame(self, frameNumber: int):
        if (self.fromFrame != -1) and (frameNumber < self.fromFrame):
            return False
        if (self.toFrame != -1) and (frameNumber > self.toFrame):
            return False
        return True


class BAGPiE:

    def __init__(self, dimensions: tuple[float, float] = (128, 128), numberOfFrames: int = 164, bgColor=(0, 0, 0), frameRate=10, loopCount=1) -> None:
        """! An animation that countains some frames to be filled later.
        @param dimensions: an [int, int] array with the width and height of the image.
        """
        # Setting instance variables:
        self.dimensions = dimensions
        self.numberOfFrames = numberOfFrames
        self.frameRate = frameRate
        self.operations: List[IOperation] = []
        self.currentFrame = None
        self.loopCount = loopCount
        self.bgColor = bgColor
        self.createFrames()
        print("Thank you for using BAGPiE: BAGPiE Animated Gif Programmable Interface Experience.")

    def ao(self, anOperation: IOperation):
        """ 'Add Operation (ao), optimised alias for 'operation.append', returning self for chain-calling

        :param IOperation anOperation: The operation to add to the chain
        :return BAGPiE: returns self, enable calling a chain of ao's.
        """
        self.operations.append(anOperation)
        return self

    def createFrames(self):
        """!
        Internal method, create frames
        @param numberOfFrames: The number of frames to be created.
        @return Nothing.
        """
        self.frames: List[Frame] = []
        for i in range(self.numberOfFrames):
            self.frames.append(Frame(self, i, bgColor=self.bgColor))

    def exportGif(self, outFileName: str):
        """!
        Performs all operations on the animation and exports it afterwards.
        @param outFileName: export this filename eventually
        """

        for operation in self.operations:
            operation.perform(self)
        images = self._getImages()
        images[0].save(outFileName, save_all=True,
                       append_images=images[1:], optimize=False, duration=self.frameRate, loop=self.loopCount)
        return self

    def _getImages(self):
        imageList: List[Image.Image] = []
        [imageList.append(frame.im) for frame in self.frames]
        return imageList

    def frameCount(self) -> int:
        """Return the total number of frames
        :return int: total amount of frames
        """
        return self.frames.__len__()


""" End class BAGPiE """


class Frame:
    def __init__(self, parentAnimation: BAGPiE, id: int, bgColor=(0, 0, 0)):
        self.id = id
        self.parent = parentAnimation
        self.im = Image.new('RGB', (self.parent.dimensions), bgColor)

    def fraction(self):
        return (self.id+1) / self.parent.frameCount()

    def c2r(self, y: float) -> int:
        """Carthesian Y value (0 is bottom) to row (0 is top) conversion

        :param float y: a carthesian y coordinate element
        :return float: a corresponding row in the PIL Image table
        """
        return math.ceil(self.parent.dimensions[1] - y)-1

    def hasPrevious(self):
        return not (self.previous() is None)

    def previous(self):
        """Return the previous frame in the sequence
        :return Frame:
        """
        if self.id - 1 < 0:
            return None
        return self.parent.frames[self.id-1]

    def hasNext(self) -> bool:
        return not (self.next is None)

    def next(self):
        """ Return the next frame in the sequence
        :return Frame: 
        """
        if self.id + 1 >= self.parent.frameCount:
            return None
        return self.parent.frames[self.id+1]

    def ellipse(self, x1: float, y1: float, x2: float, y2: float, color: tuple[int, int, int]):
        """Draw an ellipse spanning from the top left to the bottom right

        :param float x1: left
        :param float y1: top
        :param float x2: right
        :param float y2: bottom
        :param tuple[int, int, int] color: RGB color
        """
        vecTuple2 = (x1, self.c2r(y1),
                     x2, self.c2r(y2))
        draw = ImageDraw.Draw(self.im)
        draw.ellipse(
            vecTuple2,
            fill=color)

    def line(self, x1: float, y1: float, x2: float, y2: float, color: tuple[int, int, int]):
        """Draw a line from x1,y2 to x2,y2

        :param float x1: v1,x
        :param float y1: v1,y
        :param float x2: v2,x
        :param float y2: v2,y
        :param tuple[int, int, int] color: RGB color
        """

        vecTuple2 = (x1, self.c2r(y1),
                     x2, self.c2r(y2))
        draw = ImageDraw.Draw(self.im)
        draw.line(vecTuple2,
                  fill=color)

    def circle(self, x: float, y: float, r: float, color: tuple[float, float, float]):
        """Wrapper around self.ellipse

        :param float x: x (0 is left)
        :param float y: y (0 is bottom)
        :param float r: radius
        :param tuple[float,float,float] color: RGB color
        """
        self.ellipse(x-r, y+r, x+r, y-r, color)

    def pointIsInsideImage(self, x: float, y: float) -> tuple[int, int]:
        """Checks whether coordinates are within the boundaries of the image, and puts them right within that boundaries if not

        :param float x:
        :param float y:
        :return tuple[int,int]: The same or modified x,y vector
        """
        if x < 0:
            warnings.warn("Negative x value: "+str(x))
            x = 0
        if y < 0:
            warnings.warn("Negative y value: "+str(y))
            y = 0
        if x >= self.parent.dimensions[0]:
            warnings.warn(
                "X value: "+str(x)+" exceeds width dimension: "+str(self.parent.dimensions[0]))
            x = self.parent.dimensions[0]-1
        if y >= self.parent.dimensions[1]:
            warnings.warn(
                "Y value: "+str(y)+" exceeds height dimension: "+str(self.parent.dimensions[1]))
            y = self.parent.dimensions[1]-1
        return (x, y)

    def getPixel(self, x: float, y: float):
        print("x:"+str(x)+" y:"+str(y))
        x = math.ceil(x)-1
        y = self.c2r(y)
        (x, y) = self.pointIsInsideImage(x, y)
        print("X:"+str(x)+" y:"+str(y))
        return self.im.getpixel((x, y))

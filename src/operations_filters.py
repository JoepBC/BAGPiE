from bagpie import Frame
from operations import *
import numpy as np

import scipy.ndimage

class ConvoluteOperation(Operation):
    
    def __init__(self, maskMatrix = [[0, 0,0],[0,1,0],[0,0,0]], attachRelatersToAnimation=True, scaleToAnimationDimensions=True) -> None:
        super().__init__(attachRelatersToAnimation, scaleToAnimationDimensions)
        self.mask = maskMatrix

    def drawOnFrame(self, frame: Frame):
        Operation.drawOnFrame(self, frame)
        ar = np.array(frame.im)
        #RED: ar[:,:,0] - #GREEN: ar[:,:,1] - #BLUE: ar[:,:,2] 
        for convolveIndex in range(3):
            ar[:,:,convolveIndex] = scipy.ndimage.convolve(ar[:,:,convolveIndex], self.mask)
        frame.im = Image.fromarray(ar)

    def setScaleFactors(self, x: float, y: float):
        pass
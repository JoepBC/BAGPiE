from bagpie import *
from relaters import *
from operations_drawing import *
import operations_filters as Filters

bagpie = BAGPiE(dimensions=(400, 400), numberOfFrames=128,
                bgColor=(255, 255, 255))
# bagpie = BAGPiE(dimensions=(400, 400), numberOfFrames=128, bgColor=(0,0,0))


bagpie.ao(
    SnakeOperation(x=Relater(0, 1), y=Relater(0, 1, relateFunc=RelateFuncs.sin),
                   radius=0.008, color=TupleRelater((0, 0, 255), (255, 0, 0)), tailLength=128)
).ao(
    SnakeOperation(x=Relater(0, 1), y=Relater(0, 1, relateFunc=RelateFuncs.sawTooth),
                   radius=0.008, color=TupleRelater((0, 255, 0), (0, 0, 255)), tailLength=128)
).ao(
    SnakeOperation(x=Relater(0, 1), y=Relater(0, 1, relateFunc=RelateFuncs.tCos1),
                   radius=0.008, color=TupleRelater((255, 0, 0), (0, 255, 0)), tailLength=128)
).ao(
    LineOperation(0, 0.5, 1, Relater(0,1), (255, 0, 255))
).exportGif('a.gif'
).ao(
    Filters.ReRastarized(rgbFrames=[True,False, False]).setFromFrame(0).setToFrame(43)
).ao(
    Filters.ReRastarized(rgbFrames=[False, True, False]).setFromFrame(44).setToFrame(86)
).ao(
    Filters.ReRastarized(rgbFrames=[False, False, True]).setFromFrame(87).setToFrame(128)
).exportGif('a-c.gif')

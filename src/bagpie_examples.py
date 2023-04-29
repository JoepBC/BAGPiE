from bagpie import *
from relaters import *
from operations_drawing import *
from operations_filters import *

bagpie = BAGPiE(dimensions=(400, 400), numberOfFrames=128, bgColor=(255,255,255))
#bagpie = BAGPiE(dimensions=(400, 400), numberOfFrames=128, bgColor=(0,0,0))


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
    ConvoluteOperation(maskMatrix=([1/8, 1/8, 1/8],[1/8, 0, 1/8], [1/8, 1/8, 1/8]))
).exportGif('a.gif')

from bagpie import *
from relaters import *
from operations_drawing import *

bagpie = BAGPiE(dimensions=(640, 480), numberOfFrames=128)


"""TODO: work Operation ON bagpie not append it to operations of... """

bagpie.operations.append(SnakeOperation(
    x=Relater(0,1), y=Relater(0, 1, relateFunc=RelateFuncs.sin) , radius=0.008, color=TupleRelater((0, 0, 255), (255, 0, 0)), tailLength=128))

bagpie.operations.append(SnakeOperation(
    x=Relater(0,1), y=Relater(0, 1, relateFunc=RelateFuncs.sawTooth) , radius=0.008, color=TupleRelater((0, 255, 0), (0, 0, 255)), tailLength=128))

bagpie.operations.append(SnakeOperation(
    x=Relater(0,1), y=Relater(0, 1, relateFunc=RelateFuncs.tCos1) , radius=0.008, color=TupleRelater(( 255,0, 0), (0, 255, 0)), tailLength=128))

bagpie.exportGif('a.gif')

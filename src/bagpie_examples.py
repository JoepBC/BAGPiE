from bagpie import *
from ease import *
from operations_drawing import *

bagpie = BAGPiE(dimensions=(640, 480), numberOfFrames=128)

""" anim.operations.append(CircleOperation(
    x=Ease(0, 1, ease=EaseFuncs.sawTooth), radius=Ease(0, 0.4), color=(255, 0, 0)))
colorTween = TupleEase((0, 255, 255), (0, 0, 255))
anim.operations.append(CircleOperation(
    y=Ease(0, 1), radius=Ease(0.4, 0.15), color=colorTween))
"""


"""TODO: work Operation ON bagpie not append it to operations of... """

bagpie.operations.append(SnakeOperation(
    x=Ease(0,1), y=Ease(0, 1, ease=EaseFuncs.sin) , radius=0.008, color=TupleEase((0, 0, 255), (255, 0, 0)), tailLength=128))

bagpie.operations.append(SnakeOperation(
    x=Ease(0,1), y=Ease(0, 1, ease=EaseFuncs.sawTooth) , radius=0.008, color=TupleEase((0, 255, 0), (0, 0, 255)), tailLength=128))

bagpie.operations.append(SnakeOperation(
    x=Ease(0,1), y=Ease(0, 1, ease=EaseFuncs.tCos1) , radius=0.008, color=TupleEase(( 255,0, 0), (0, 255, 0)), tailLength=128))

bagpie.exportGif('mynewesttest.gif')

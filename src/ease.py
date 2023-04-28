import math
from typing import Any, List, Dict


class EaseFuncs:
    """Functions that vary values over the duration of an animation.
    """

    def identity(input:float) -> float:
        """The identity ease function, x = x

        :param float input: range 0-1
        :return float: range 0-1
        """
        return input
    
    def inv(input:float) -> float:
        """The inverse ease function, x = 1-x

        :param float input: range 0-1
        :return float: range 0-1
        """
        return 1.0-input
    
    def sawTooth(input:float) -> float:
        """The sawTooth ease function, x = 1-|0.5-x|*2

        :param float input: range 0-1
        :return float: range 0-1
        """
        return 1.0-(abs (0.5-input)*2)
        
    def sin(input: float) -> float:
        """A curvy version of the sawtooth, x = sin(x*pi)

        :param float input: range 0-1
        :return float: range 0-1
        """
        return math.sin(input * math.pi)
    

    def tCos1(input:float) -> float:
        return (1 + math.sin(-math.pi*0.5+input*2*math.pi))/2

    def tCos2(input:float) -> float:
        return (1 + math.sin(-math.pi*0.5+input*2*math.pi))/2

class AbstractEaser:
    def __init__(self, valueFrom, valueTo,  fractionFunc=(lambda: 0), factor=1, ease=EaseFuncs.identity) -> None:
        self._fractionFunc = fractionFunc
        self.factor = factor
        self.ease=ease

    def setFractionFunc(self, fractionFunc):
        self._fractionFunc = fractionFunc

    def value(self, fraction: float = None):
        raise Exception('AbstractTween instance cannot return values')

    def Ensure(aValue: Any):
        if (isinstance(aValue, AbstractEaser)):
            return aValue
        if (isinstance(aValue, tuple)):
            return TupleEase(aValue)
        return Ease(aValue)

    def nowFraction(self, overrideFraction=None):
        return self.ease(self._fractionFunc() if (overrideFraction is None) else overrideFraction)



class Ease(AbstractEaser):

    def __init__(self, valueFrom: float, valueTo: float = None, fractionFunc=(lambda: 0), factor=1, ease=EaseFuncs.identity) -> None:
        super().__init__(valueFrom, valueTo, fractionFunc, factor, ease)
        self.valueFrom = valueFrom
        self.valueTo = valueFrom if (valueTo is None) else valueTo

    def value(self, overrideFraction=None):
        # Default linear Tween
        diff = self.valueTo - self.valueFrom
        return (self.valueFrom + (diff * self.nowFraction(overrideFraction)))*self.factor


class TupleEase(AbstractEaser):
    """!
    Has a collection of tweens for all items in a tuple stored in @member tupleItems of @type List[Tween]
    """

    def __init__(self, valueFrom: tuple, valueTo: tuple = None, fractionFunc=lambda: 0, factor=1, ease=EaseFuncs.identity) -> None:
        super().__init__(valueFrom, valueTo, fractionFunc, factor, ease)
        valueTo = valueFrom if (valueTo is None) else valueTo
        if (len(valueFrom) != len(valueTo)):
            raise Exception("Tuples for tween differ in length: " +
                            str(valueFrom)+" / "+str(valueTo))
        self.tupleItems: List[Ease] = []
        for i in range(len(valueFrom)):
            self.tupleItems.append(
                Ease(valueFrom[i], valueTo[i], fractionFunc, factor))

    def value(self, overrideFraction: float = None):
        items = []
        for i in range(len(self.tupleItems)):
            items.append(self.tupleItems[i].value(
                self.nowFraction(overrideFraction)))
        return tuple(items)

    def intsValue(self, overrideFraction: float = None):
        baseVal = self.value(overrideFraction)
        return tuple(map(int, baseVal))

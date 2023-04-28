import types
import numpy


def tweenFunc(input: float):
    return 1-(abs (0.5-input)*2)


a = tweenFunc
b = (1, 2.)
c: float = (type(a) is types.FunctionType)
d = [1, 'x', 2.0]
e = tuple(['a', 2, 3.3])

for tval in [a, b, c, d, e]:
    print("Val: "+str(tval)+"("+str(type(tval))+")")
    if (isinstance(tval, tuple)):
        # print("Tuple of length "+ str(list(map(type, tval)).__len__())+str(list(map(type, tval))))
        pass

for fi in numpy.arange(0.0, 1.0, 0.04):
    print(str(fi) + " -> "+str(tweenFunc(fi)))

class A:
    def foo(self):
        print ('fooing')


x = A()
x.foo()
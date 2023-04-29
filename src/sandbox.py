import types
import numpy as np
import scipy.ndimage as spnd

def tweenFunc(input: float):
    return 1-(abs (0.5-input)*2)

def testTweenFuncs():
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

    for fi in np.arange(0.0, 1.0, 0.04):
        print(str(fi) + " -> "+str(tweenFunc(fi)))

class A:
    def foo(self):
        print ('fooing')


x = A()
getattr(x, 'foo')()

a = np.array([[1.0,2,3,4],[1,2,3,5],[5,6,7,8]])
print(a)
m = np.array([[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]])
print (m)
print('....')
r = spnd.convolve(a,m)
print(r)
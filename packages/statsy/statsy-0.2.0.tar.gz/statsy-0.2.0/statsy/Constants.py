from .main import *

e = summation(None,None,lambda n: 1/(math.factorial(n)), [[n for n in range (1000)]])

pi= math.pi

def e_specified(depth:int) -> Number:
    """
    A specified depth to calculate the constant e.
    """
    depth_list = [n for n in range (depth)]
    return summation(None,None,lambda n: 1/(math.factorial(n)), [depth_list])

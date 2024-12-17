from .main import *
import math, statistics

def ln(a:Number)->Number:
    """
    Returns the natural log.
    """
    return math.log(a)

def log(base:Number,a:Number)->Number:
    """
    Returns any logarithm for base and value.
    """
    return (math.log10(a)/math.log10(base))

from .main import *
from .Logarithms import *

def Sturges_rule(number_of_points:Number)->Number:
    """
    Sturges' rule for determining the approx. number of intervals for histograms.
    """
    return round(1 + log(2,number_of_points))

def Rice_rule(number_of_points:Number)->Number:
    """
    Rice rule for determining the approx. number of intervals for histograms.
    """
    return round(2 * (root(3,number_of_points)))

def arithmetic_mean(data:list)->Number:
    """
    Returns the arithmetic mean of a list of data points.
    """
    return (summation(None,None,None,[data])) / len(data)

def median(data:list)->Number:
    """
    Returns the simple mean of an ordered quantitative list.
    """
    total_length = len(data)
    if total_length & 1:
        return  data[int((total_length+1)/2)-1]
    else:
        return (data[ int((total_length/2)-1)] + data[int((total_length/2)+1)])/2

def mode(data:list)->any:
    """
    A shortcut for statistics.mode(data)
    """
    return statistics.mode(data)

def trimean(data:list)->Number:
    """
    Returns the trimean of a set of data.
    Be sure to order list in an increasing order.
    """
    p25 = get_value_from_percentile(25,data)
    p50 = get_value_from_percentile(50,data)
    p75 = get_value_from_percentile(75,data)
    
    return ( (p25 + (2 * p50) + p75 ) / 4 )

def geometric_mean(data:list)->Number:
    """
    Returns the geometric mean of a list of data.
    """
    return (product_notation(None,None,None,[data]) ** (1/len(data)))

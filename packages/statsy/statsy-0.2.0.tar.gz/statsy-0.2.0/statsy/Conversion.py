from .main import *

def Celcius_to_Fahrenheit(C:Number) -> Number:
    """
    Returns the Fahrenheit value of a Celcius value.
    """
    return (1.8 * C) + 32

def Fahrenheit_to_Celcius(F:Number) -> Number:
    """
    Returns the Celcius value of a Fahrenheit value.
    """
    return (F - 32)/1.8

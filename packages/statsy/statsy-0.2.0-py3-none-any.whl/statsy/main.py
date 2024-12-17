import math, string, inspect
from typing import Callable, Union, List

Number = Union[int, float]

def get_value_from_percentile(percentile:Number,data:list) -> Number:
    """
    percentile = known percentile \n
    data = list of ordered elements \n
    This function returns the desired weighted percentile from a list of data.
    """
    value =(percentile/100) * (len(data) + 1)
    fr = value - (math.floor(value))
    ir = (math.floor(value))
    ir_value = data[ir-1]
    ir_plus_1_value = data[ir]
    if ir_value > ir_plus_1_value:
        lowest = ir_plus_1_value
    if ir_plus_1_value > ir_value:
        lowest = ir_value
    if ir_plus_1_value == ir_value:
        lowest = ir_value
    diff = abs(ir_plus_1_value - ir_value)
    value = (diff * fr) + lowest
    return value

def summation(i:int,range:int,expression:Callable,data:List[List[Number]]) -> Number:
    """
    i = beginning of the range to execute. \n
    range = range to execute \n
    expression = function to apply to the data \n
    data = list of lists that contain values to evaluate \n
    This function returns the value of a summation.
    """
    if expression is None:
        expression = lambda x: x
    if len(inspect.signature(expression).parameters) != len(data):
        raise ValueError("There must be the same number of input data lists as expression inputs")
    lists_ready_to_eval = []
    # For each list in the data, return the range to be evaluated
    for input_list in data:
        # If no start and range are specified, pass the entire list to evaluate
        if i is None and range is None:
            lists_ready_to_eval.append(input_list)
        # If a range is given, slice that part of the list and return it to the list of lists to evaluate
        else:
            lists_ready_to_eval.append(input_list[i-1:range+1])
    # Create a list containing all the evaluated values in the range of interest
    evaluated_list = []    
    # Check for multi-variable functions by checking the number of input lists. These two numbers should be the same.
    if  len(data) > 1:
        # If multi-variable function is given:
        range_of_list_to_eval = len(lists_ready_to_eval[0])
        current_index_of_list_to_eval = 0
        # Use zip to iterate through all lists at the same time and '*' to unpack the lists. This returns a tuple where each item in the tuple has the same index across all lists
        for val in zip(*lists_ready_to_eval):
            # Use * to unpack the tuple and input into the function and add to evaluated list
            evaluated_list.append(expression(*val))
    else:
        for val in lists_ready_to_eval[0]:
            # Evaluate expression and add to evaluated list
            evaluated_list.append(expression(val))
              
    return sum(evaluated_list)

def multiply_elements(data:list)->Number:
    """
    Multiplies all elements in a list together.
    """
    res = 1
    for element in data:
        res = res * element
    return res

def product_notation(i:int,range:int,expression:Callable,data:List[List[Number]]) -> Number:
    """
    i = beginning of the range to execute. \n
    range = range to execute \n
    expression = function to apply to the data \n
    data = list of lists that contain values to evaluate \n
    This function returns the value of a product notation.
    """
    if expression is None:
        expression = lambda x: x
    if len(inspect.signature(expression).parameters) != len(data):
        raise ValueError("There must be the same number of input data lists as expression inputs")
    lists_ready_to_eval = []
    # For each list in the data, return the range to be evaluated
    for input_list in data:
        # If no start and range are specified, pass the entire list to evaluate
        if i is None and range is None:
            lists_ready_to_eval.append(input_list)
        # If a range is given, slice that part of the list and return it to the list of lists to evaluate
        else:
            lists_ready_to_eval.append(input_list[i-1:range+1])
    # Create a list containing all the evaluated values in the range of interest
    evaluated_list = []    
    # Check for multi-variable functions by checking the number of input lists. These two numbers should be the same.
    if  len(data) > 1:
        # If multi-variable function is given:
        range_of_list_to_eval = len(lists_ready_to_eval[0])
        current_index_of_list_to_eval = 0
        # Use zip to iterate through all lists at the same time and '*' to unpack the lists. This returns a tuple where each item in the tuple has the same index across all lists
        for val in zip(*lists_ready_to_eval):
            # Use * to unpack the tuple and input into the function and add to evaluated list
            evaluated_list.append(expression(*val))
    else:
        for val in lists_ready_to_eval[0]:
            # Evaluate expression and add to evaluated list
            evaluated_list.append(expression(val))
              
    return multiply_elements(evaluated_list)

def root(root_value:Number,root_input:Number)->Number:
    """
    Returns the arbitrary root of an input.
    """
    return root_input ** (1/root_value)

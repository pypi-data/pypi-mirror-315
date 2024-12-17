"""
This is a Cython module.

:meta public:
"""

def harmonic_mean(*args):
    """
    This is a function written for Cyton. This is a reference to the math:
    https://en.wikipedia.org/wiki/Harmonic_mean 

    Args:
        *args: A list of numbers passed as floats.
    
    Returns:
        Harmonic mean of the numbers.

    :meta public:
    """
    if type(args[0]) == list:
        measurements = args[0]
    else:
        measurements = list(args)
    num_measurements = len(measurements)
    inverse_args = [1/arg for arg in measurements]
    return num_measurements / sum(inverse_args)
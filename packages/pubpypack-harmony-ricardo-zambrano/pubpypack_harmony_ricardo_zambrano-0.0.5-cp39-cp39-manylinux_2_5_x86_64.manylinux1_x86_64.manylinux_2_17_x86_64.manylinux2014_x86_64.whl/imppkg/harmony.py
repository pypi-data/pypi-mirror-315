"""
A command-line interface for calculating the harmonic mean of user-provided numbers.

:meta public:
"""

import sys
from imppkg.harmonic_mean import harmonic_mean
from termcolor import cprint
from termcolor import colored


def _parse_num(inputs: list[str]) -> list[float]:
    """
    This function parses the parameters from the cli.

    Args:
        inpus(list[str]): A list of numbers in passed as strings from the CLI.

    Returns:
        list[float]: Casts the numbers passed as string to float. The output is
        a list of floats.

    :meta public:
    """
    try:
        nums = [float(arg) for arg in inputs]
    except ValueError:
        # If input cannot be converted to float, proceed as if there was no input
        nums = []

    return nums


def _calculate_results(nums: list[float]) -> float:
    """
    This function will have a coment to send to sphix

    :meta public:
    """

    try:
        #: There is variable called result in this try-except block.
        #: The variable definition calls harmonic_mean()
        result = harmonic_mean(nums)  #: Alternative placement od doc comment
        return result
    except ZeroDivisionError:
        # If there is no input or if the input is zero, rpoceed with the default result
        result = 0.0  # The result will be zero unless succesfully calculated
        return result


def _format_output(result: float) -> str:

    result_str = str(result)
    formated_result = colored(result_str, "red", "on_cyan", attrs=["bold"])

    return formated_result


def main():

    numbers = _parse_num(sys.argv[1:])

    results = _calculate_results(numbers)

    out = _format_output(results)

    cprint(out)


# def main():

#     result = 0.0 # The result will be zero unless succesfully calculated

#     try:
#         nums = [float(arg) for arg in sys.argv[1:]]

#     except ValueError:
#         # If input cannot be converted to float, proceed as if there was no input
#         nums = []

#     try:
#         result = harmonic_mean(nums)
#     except ZeroDivisionError:
#         # If there is no input or if the input is zero, rpoceed with the default result
#         pass

#     cprint(result, 'red', 'on_cyan', attrs=['bold'])

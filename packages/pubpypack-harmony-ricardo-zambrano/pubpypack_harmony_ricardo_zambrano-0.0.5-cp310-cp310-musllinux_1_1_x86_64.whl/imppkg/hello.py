"""
This module is meant to test sphinx

:meta public:
"""

# Hello, this is a comment to test the test_branch

# To create the pull request from VS Code I had to run the following commands from
# the terminal:

# > git remote remove origin
# > git remote add origin https://github.com/rzambrano1/first-python-package.git


class MyClass(object):
    """
    Description for class.

    Attributes:
        var1 (type): Initial value, set by `par1`.
        var2 (type): Initial value, set by `par2`.

    :meta public:
    """

    def __init__(self, par1, par2):
        """
        Initializes MyClass with given parameters.

        Args:
            par1 (type): Description of the first parameter.
            par2 (type): Description of the second parameter.

        :meta public:
        """
        self.var1 = par1
        self.var2 = par2

    def method(self):
        """
        Example method.

        Returns:
            None

        :meta public:
        """
        pass

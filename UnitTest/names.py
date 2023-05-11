# python -m doctest <file>   use this command to run the test code inside of the """ """
# python -m unittest <file>  use this command to run all classes that inherit from unittest.Testcase, 
#                            it will only run the deffinitions that start with test 


import unittest
import pandas

def get_first_last(name):
    """This function takes in a full name and splits it into first and last
    
    >>> get_first_last("Caleb Price")
    ('Caleb', 'Price')
    
    """
    return tuple(name.split(" "))

# add comment
class Testing(unittest.TestCase):
    def test_names(self):
        self.assertEqual(get_first_last("Caleb Price"), ("Caleb", "Price"))
    
    def test_golden_file(self):
        df = pandas.read_csv("names.csv")
        df["first_name"] = df.apply(lambda x: get_first_last(x["Full Names"])[0], axis = 1)
        df["last_name"] = df.apply(lambda x: get_first_last(x["Full Names"])[1], axis = 1)
        print(df)



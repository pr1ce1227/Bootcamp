''' This is a module Comment'''


# Regular comment 

"""
This is a multi line comment 
"""

class person: 
    """
    This is the docstring since it oc urs below the class definition,
    This represent a person class
    """

    def __init_(self):
        """
        This initializes my class
        """
        pass

    def walk(self):
        """This causes person to walk """
        pass

    def talk(self):
        """This causes person to talk """
        pass

    def eat(self):
        """This causes person to eat """
        pass


def main():
    caleb = person()
    print("Docstring for person\n", person.__doc__)
    print("Docstring for walk\n\n", person.walk.__doc__)
    #help(person)    # this prints everything 

if __name__ == "__main__":
    main()



#! /usr/bin/python 
# the above shebang is added so that you can just type the file name without specifying pythong and it will run

#  Basics: 
#  * No braces in python only white space, must follow proper indentation 
#  * once a variable is created regardless of scope (unless in a function) that variable now exists in the file 
#  * class object variables can be created by using the self.<var> structure in the class methods 
#  * generally import nearly every function that someone else has alread writtent 


import requests

# "self", or the object is always the first variable passed to a method, by convention we include self always as 
# the first perameter. You don't need to pass it yourself its automatically done. Remember self.<var> will create the variable
# in the class you don't have to declare it outside the method like other languages 
class person:
    def __init__(self, name):
        self.x = 0; 
        self.y = 0; 
        self.name = name; 
    
    def move(self, x, y): 
        self.x += x 
        self.y += y 

    def location(self): 
        print(self.name, ": (", self.x, ',', self.y, ")")

#basic function example 
def sayHello():
    print("Hello", end="") # print includes \n automatically add this end statment to remove 
    print("Caleb")

def main():
    caleb = person("Caleb")
    caleb.location()
    caleb.move(5,6)
    caleb.location()
    sayHello()
    # print(dir(caleb)) #when called on an object is gives all the functions, and object variables 

# This if statement causes the code only to be ran when this files is ran as the main file 
# otherwise if it was just imported and being used by another file the code below this statement wont run 
if __name__ == "__main__":
   main()
   
 
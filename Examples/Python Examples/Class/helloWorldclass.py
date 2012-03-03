# hello class
# 3/3/2012

class hello:
    def __init__(self):
        self.string = "Hello World!"
        
    def Printer(self):
        self.printString = self.string
        print self.printString
        

# This class can be assigned to a variable and then the functions within
# the class can be accessed.

# This creates the object.
value = hello()

# Now to call the Printer function within it to print the string.
value.Printer()

from myro import *

class RectButton:
    def __init__(self, win, center, width, height):
        w, h = width/2.0, height/2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        self.center = center
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('gray')
        self.rect.draw(win)
        self.win = win
    def makeLabel(self, label):
        self.label = Text(self.center, label)
        self.label.setSize(10)
        self.label.draw(self.win)
    def removeLabel(self):
        self.label.undraw()
    def removeButton(self):
        self.rect.undraw()
    def clicked(self, p):
        return(self.xmin<= p.getX()<= self.xmax
               and self.ymin<= p.getY()<= self.ymax)
    def getCenter(self):
        return self.rect.getCenter()

class RadioButton:
    def __init__(self, win, center, radius):
        self.circ = Circle(center,radius)
        self.circ.setFill('white')
        self.circ.draw(win)
        self.center = center
        self.radius = radius
        self.active = False
        self.win = win
    def makeLabel(self, distanceFromCenterX, distanceFromCenterY, label):
        self.labelCenter = self.center.clone()
        self.labelCenter.move(distanceFromCenterX,distanceFromCenterY)
        self.label = Text(self.labelCenter, label)
        self.label.setSize(10)
        self.label.draw(self.win)
    def removeLabel(self):
        self.label.undraw()
    def removeButton(self):
        self.circ.undraw()
    def clicked(self, p):
        return((self.circ.p1.x <= p.x <= self.circ.p2.x)
               and (self.circ.p1.y <= p.y <= self.circ.p2.y))
    def turnOn(self):
        self.circOn = Circle(self.center,self.radius-7)
        self.circOn.draw(self.win)
        self.circOn.setFill('black')
        self.active = True
    def turnOff(self):
        self.circOn.undraw()
        self.active = False


##This was a Test
##def main():
##    win = GraphWin()
##    rb = RadioButton(win, Point(50,50), 10)
##    rb.makeLabel(50,0,'yes')
##    for i in range(10):
##            p = win.getMouse()
##            if rb.clicked(p) == True and rb.active == False:
##                    rb.turnOn()
##            elif rb.clicked(p) == True and rb.active == True:
##                    None
##            elif rb.clicked(p) == False and rb.active == True:
##                    rb.turnOff()
##            elif rb.clicked(p) == False and rb.active == False:
##                    None

## Author: Dylan Hulon
## Created:
##  3/22/12

#from main import Application
from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.task.Task import Task 
from panda3d.core import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.actor.Actor import Actor
import sys

class UserInputControl(DirectObject.DirectObject):
	def __init__(self):
                self.firstModel = Actor("models/proofOfConcept.egg", {"walk":"models/proofOfConcept.egg"})

##	def acceptKeys(self):	
##		self.accept("w", self.setKey, ["mvUp", 1])
##		self.accept("s", self.setKey, ["mvDown", 1])
##		self.accept("a", self.setKey, ["mvLeft", 1])
##		self.accept("d", self.setKey, ["mvRight", 1])
##		
##		self.accept("w-up", self.setKey, ["mvUp", 0])
##		self.accept("s-up", self.setKey, ["mvDown", 0])
##		self.accept("a-up", self.setKey, ["mvLeft", 0])
##		self.accept("d-up", self.setKey, ["mvRight", 0])
##		
		
		
		
	def move(self, keyClass):
		if (keyClass.keyMap["forward"]!=0):
                        self.firstModel.setH(50)
                        y = self.firstModel.getH()
                        print y
		
	
class Keys(DirectObject.DirectObject):
	def __init__(self):
		self.isTyping = False
		self.keyMap = {"left":0, "right":0, "forward":0, "back":0, "cam-right":0}
		self.accept("escape", sys.exit)
		self.accept("arrow_left", self.setKey, ["left",1])
		self.accept("arrow_right", self.setKey, ["right",1])
		self.accept("arrow_up", self.setKey, ["forward",1])
		self.accept("arrow_down", self.setKey, ["back",1])
		self.accept("arrow_left-up", self.setKey, ["left",0])
		self.accept("arrow_right-up", self.setKey, ["right",0])
		self.accept("arrow_up-up", self.setKey, ["forward",0])
		self.accept("arrow_down-up", self.setKey, ["back",0])
		
	def setKey(self, key, value):
		if not self.isTyping:
			self.keyMap[key] = value

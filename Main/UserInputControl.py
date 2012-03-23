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

class UserInputControl(DirectObject.DirectObject):
	def __init__(self):
		self.keyMap = {"mvUp":0, "mvDown":0, "mvLeft":0, "mvRight":0}
		#model = Application()
	
	def acceptKeys(self):	
		self.accept("w", self.setKey, ["mvUp", 1])
		self.accept("s", self.setKey, ["mvDown", 1])
		self.accept("a", self.setKey, ["mvLeft", 1])
		self.accept("d", self.setKey, ["mvRight", 1])
		
		self.accept("w-up", self.setKey, ["mvUp", 0])
		self.accept("s-up", self.setKey, ["mvDown", 0])
		self.accept("a-up", self.setKey, ["mvLeft", 0])
		self.accept("d-up", self.setKey, ["mvRight", 0])
		
		#taskMgr.add(self.move, "moveTask")
		
		print "Initialized"
		
	def move(self):
		print "Hello"
		if (self.keyMap["mvUp"]!=0):
			self.firstModel.setY(self.firstModel, 50)
			y = self.firstModel.getY()
			print y
		
	def setKey(self, key, value):
		self.keyMap[key] = value
		
	def allFunctions(self, task):
		self.acceptKeys()
		self.move()
		return task.cont

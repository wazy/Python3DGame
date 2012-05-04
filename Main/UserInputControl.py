## Author: Dylan Hulon
## Created:
##  3/22/12

#from main import Application
#from direct.showbase.ShowBase import ShowBase
#from other import model
from direct.showbase import DirectObject
from direct.task.Task import Task 
from panda3d.core import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.actor.Actor import Actor
import sys
from pandac.PandaModules import RenderState


class Keys(DirectObject.DirectObject):
	def __init__(self):
		#self.firstModel = Actor("models/babya.x")
		#self.firstModel.reparentTo(self.render)
		
		self.isTyping = False
		self.keyMap = {"mvUp":0, "mvDown":0, "mvLeft":0, "mvRight":0}
		
		self.accept("escape", sys.exit)
		
		self.accept("w", self.setKey, ["mvUp", 1])
		self.accept("s", self.setKey, ["mvDown", 1])
		self.accept("a", self.setKey, ["mvLeft", 1])
		self.accept("d", self.setKey, ["mvRight", 1])
		
		self.accept("w-up", self.setKey, ["mvUp", 0])
		self.accept("s-up", self.setKey, ["mvDown", 0])
		self.accept("a-up", self.setKey, ["mvLeft", 0])
		self.accept("d-up", self.setKey, ["mvRight", 0])
		
	def setKey(self, key, value):
		if not self.isTyping:
			print "why did you call me? I serve no purpose, also you pressed %s \n" %key
			self.keyMap[key] = value
			print self.keyMap

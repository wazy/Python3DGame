from direct.directbase import DirectStart
from interactiveTexture import *

import platform
import sys

if platform.system() == "Windows":
	props = WindowProperties()
	props.setFullscreen(True)
	base.win.requestProperties(props)

base.disableMouse()

class world(object):
	def __init__(self):
		"""
		Setup the interactive texture. It's size has to be power of two.
		"""
		self.it = interactiveTexture("demo", 2048, 1024)
		self.itTex = self.it.getTexture()
		
		"""
		Two samples from the manual. They're unchanged, except for placement and, obviously, parent.
		Anything you want to be displayed on an interactive texture must be parented to interactiveTexture.renderRoot.
		"""
		self.directButtonSample()
		self.directEntrySample()
		
		self.instruction = OnscreenText(
			text = "Move the mouse to move the cursor on the texture\n[f1] -- Rotate camera left\n[f2] -- Rotate camera right\n[f3] -- Rotate camera up\n[f4] -- Rotate camera down\n",
			pos = (-1.7, -0.25), 
			scale = 0.07,
			align=TextNode.ALeft,
			parent = self.it.renderRoot)
		
		self.model = loader.loadModel("./map")
		self.model.reparentTo(render)
		self.modelNode = self.model.find("-PandaNode")
		
		"""
		The texture can be placed anywhere. You can have multiple screens using the same texture,
		have the texture projected onto the environment or wrapped around complex meshes -- in any case,
		it will work.
		"""
		self.screens = []
		for childNode in self.modelNode.getChildren():
			if childNode.getTag("type") == "screen":
				childNode.setTexture(self.itTex, 1)
				self.screens.append(childNode)
			elif childNode.getTag("type") == "camPos":
				self.cameraParent = childNode
				base.cam.reparentTo(self.cameraParent)
				base.cam.setPos(Vec3(0, -1, 0))
		
		base.accept("f1", self.moveCamLeft)
		base.accept("f2", self.moveCamRight)
		base.accept("f3", self.moveCamUp)
		base.accept("f4", self.moveCamDown)
		base.accept("escape", sys.exit)
		
		props = WindowProperties()
		props.setMouseMode(WindowProperties.MRelative)
		props.setCursorHidden(True)
		base.win.requestProperties(props)
		
		base.setBackgroundColor(.2, .2, .2)
		base.camLens.setFov(75)
		base.camLens.setNear(0.01)
		
		self.it.enable()
	
	def moveCamLeft(self):
		self.cameraParent.setH(self.cameraParent.getH() - 5.0)
	
	def moveCamRight(self):
		self.cameraParent.setH(self.cameraParent.getH() + 5.0)
	
	def moveCamUp(self):
		self.cameraParent.setP(self.cameraParent.getP() - 5.0)
	
	def moveCamDown(self):
		self.cameraParent.setP(self.cameraParent.getP() + 5.0)
	
	def directEntrySample(self):
		self.entry = DirectEntry(text = "" ,scale=0.1, initialText="Type Something", numLines = 2,focus = 1, parent = self.it.renderRoot, pos = (-1.1, 0, 0.1))
	
	def setText(self):
		bk_text = "Button Clicked"
		self.textObject.setText(bk_text)

	def directButtonSample(self):
		# Add some text
		bk_text = "This is my Demo"
		self.textObject = OnscreenText(
			text = bk_text,
			pos = (0.95,-0.95), 
			scale = 0.07,
			fg=(1,0.5,0.5,1),
			align=TextNode.ACenter,
			mayChange=1,
			parent = self.it.renderRoot)
		
		# Add button
		self.button = DirectButton(text = ("OK", "click!", "rolling over", "disabled"), scale=0.1, command=self.setText, parent = self.it.renderRoot, pos = (0.5, 0, 0.5))

w = world()
run()

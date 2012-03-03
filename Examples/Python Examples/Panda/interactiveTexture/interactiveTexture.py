from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from pandac.PandaModules import *

class interactiveTexture(object, DirectObject):
	def __init__(self, name, sizeX, sizeY):
		self.name = name
		
		self.sizeX = sizeX
		self.sizeY = sizeY
		
		self.enabled = False
		
		"""
		Dummy mouse watcher used to disable events
		"""
		self.dummyMW = MouseWatcher("dummy" + name)
		
		self.setupRender()
		self.disable()
		
		self.texture = self.renderBuffer.getTexture()
		self.texture.setMagfilter(Texture.FTLinear)
		self.texture.setMinfilter(Texture.FTLinearMipmapLinear)
		self.texture.setAnisotropicDegree(16)
		
		self.cursor = self.renderRoot.attachNewNode(name + "_cursorParent", sort = 1000)
		
		self.cursorImage = DirectFrame(
			frameSize = (0, 0.1, -0.1, 0),
			pos = Vec3(0, 0, 0),
			frameColor = (1, 1, 1, 1),
			parent = self.cursor,
			relief = DGG.FLAT,
			sortOrder = 1000,
			frameTexture = "./cursor.png",
			)
		self.cursorImage.setTransparency(TransparencyAttrib.MAlpha)
		
		self.mouseLeaveFrameCounter = 0
		
	def getTexture(self):
		return self.texture
	
	def enable(self):
		self.enabled = True
		
		props = WindowProperties()
		
		"""
		In real use, you will probably want to use these two commented lines.
		Note, that on Windows MRelative is currently not supported, thus this system only works reliably
		in fullscreen on Windows.
		"""
		#props.setMouseMode(WindowProperties.MRelative)
		#props.setCursorHidden(True)
		base.win.movePointer(0, base.win.getXSize()/2, base.win.getYSize()/2)
		base.win.requestProperties(props)
		
		self.renderRoot.node().setMouseWatcher(base.mouseWatcherNode)
		
		taskMgr.doMethodLater(1.0/60.0, self.updateMousePos, "screenSurfaceUpdateMouse")
	
	def disable(self):
		self.enabled = False
		self.renderRoot.node().setMouseWatcher(self.dummyMW)
		
		props = WindowProperties()
		props.setMouseMode(WindowProperties.MAbsolute)
		props.setCursorHidden(False)
		base.win.requestProperties(props)
		
		taskMgr.remove("screenSurfaceUpdateMouse")
	
	def setupRender(self):
		"""
		This is practically ripped off from the ShowBase. It's a replacement for aspect2d.
		"""
		self.renderBuffer = base.win.makeTextureBuffer(self.name + "Buffer", self.sizeX, self.sizeY)
		
		self.renderRoot = NodePath(PGTop(self.name + "RenderRoot"))
		self.renderRoot.setDepthTest(0)
		self.renderRoot.setDepthWrite(0)
		self.renderRoot.setMaterialOff(1)
		self.renderRoot.setTwoSided(1)
		
		self.aspectRatio = base.getAspectRatio(self.renderBuffer)
		self.renderRoot.setScale(1.0 / self.aspectRatio, 1.0, 1.0)
		
		dr = self.renderBuffer.makeMonoDisplayRegion(0, 1, 0, 1)
		dr.setSort(10)
		dr.setClearDepthActive(1)
		dr.setIncompleteRender(False)
		self.left, self.right, self.bottom, self.top = -self.aspectRatio, self.aspectRatio, -1, 1
		
		cam2dNode = Camera(self.name + "Camera")
		
		lens = OrthographicLens()
		lens.setFilmSize(self.right - self.left, self.top - self.bottom)
		lens.setFilmOffset((self.right + self.left) * 0.5, (self.top + self.bottom) * 0.5)
		lens.setNearFar(-1000, 1000)
		cam2dNode.setLens(lens)
		
		self.camera2d = self.renderRoot.attachNewNode(self.name + "Camera2d")

		camera2d = self.camera2d.attachNewNode(cam2dNode)
		dr.setCamera(camera2d)
		
		self.cam2d = camera2d
	
	def updateMousePos(self, task):
		if base.mouseWatcherNode.hasMouse() and self.enabled:
			x = base.mouseWatcherNode.getMouseX() * self.aspectRatio
			y = base.mouseWatcherNode.getMouseY()
			
			xEdge = False
			yEdge = False
			
			if x <= self.left:
				x = self.left
				xEdge = True
			elif x >= self.right - 0.02:
				x = self.right - 0.02
				xEdge = True
				
			if y <= self.bottom + 0.02:
				y = self.bottom + 0.02
				yEdge = True
			elif y >= self.top:
				y = self.top
				yEdge = True
			
			self.cursor.setPos(self.renderRoot, x, 0, y)
			"""
			if xEdge or yEdge:
				self.mouseLeaveFrameCounter += 1
			else:
				self.mouseLeaveFrameCounter = 0
			
			if self.mouseLeaveFrameCounter == 60:
				self.disable()
				self.mouseLeaveFrameCounter = 0
			"""
			return task.again

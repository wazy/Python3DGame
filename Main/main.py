## Written and experimented with by Daniel Ballard.
## 1:09 AM 3/4/2012

# Standard imports for Panda3d.
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText,TextNode 
from panda3d.core import *

# This may not be necessary but configures Panda to use OpenAL.
#loadPrcFileData("", "audio-library-name p3openal_audio")

class Application(ShowBase):
    def __init__(self):
        # Always add this!!! To load/render/etc.
        ShowBase.__init__(self)

        # Make a plane to play the movie on.
        self.cm = CardMaker("plane")
        self.cm.setFrame(-1, 1, -1, 1)

        # Render that plane to the render2d for Panda.
        self.plane = self.render2d.attachNewNode(self.cm.generate())

        # Load movie and its sound (if it has sound).
        self.movie = self.loader.loadTexture("videos/loading_screen.ogm")
        self.sound = self.loader.loadSfx("videos/loading_screen.ogm")

        # Load movie into the texture plane.
        self.plane.setTexture(self.movie)

        # This can prevent squashing or distorting of the video.
        self.plane.setTexScale(TextureStage.getDefault(), self.movie.getTexScale())

        # 0 means do not loop infinitely.
        self.movie.setLoop(0)

        # If it has sound, synchronize it to the video.
        self.movie.synchronizeTo(self.sound)

        # Play the sound.
        self.sound.play()

        self.loadingText=OnscreenText("Loading...",1,fg=(1,1,1,1),pos=(0,0),align=TextNode.ACenter,scale=.07,mayChange=1) 
        self.graphicsEngine.renderFrame() #render a frame otherwise the screen will remain black 
        self.graphicsEngine.renderFrame() #idem dito
		
        self.image = self.loadImageAsPlane('models/Fireworks.jpg')
        taskMgr.doMethodLater(14,self.image.reparentTo(aspect2d),"ImageLoader")
        taskMgr.doMethodLater(14,self.image.setTransparency(TransparencyAttrib.MAlpha),"ImageTrans")
		
    def loadImageAsPlane(self, task, filepath, yresolution = 600): 
		#Load image as 3d plane; Arguments: filepath -- image file path yresolution -- pixel-perfect width resolution 
		self.tex = loader.loadTexture(filepath) 
		self.tex.setBorderColor(Vec4(0,0,0,0)) 
		self.tex.setWrapU(Texture.WMBorderColor)
		self.tex.setWrapV(Texture.WMBorderColor)
		self.cm2 = CardMaker(filepath + ' card')
		self.cm2.setFrame(-self.tex.getOrigFileXSize(), self.tex.getOrigFileXSize(), -self.tex.getOrigFileYSize(), self.tex.getOrigFileYSize())
		self.card = NodePath(self.cm2.generate())
		self.card.setTexture(self.tex)
		self.card.setScale(self.card.getScale()/ yresolution)
		self.card.flattenLight() # apply scale
		return self.card, task.cont 
# Assign the class to a variable.        
app = Application()
# And finally, run it!!
app.run()

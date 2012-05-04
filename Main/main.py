## Version 0.01
## Last change:
## 21:40 3/22/2012

# Standard imports for Panda3d.
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task 
from panda3d.core import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from UserInputControl import *

# Custom import.
from FirstPersonCamera import MouseLook

import sys

class Application(ShowBase):
    def __init__(self):
        # Always add this!!! To load/render/etc.
        ShowBase.__init__(self)
        #keys = Keys()
        #base.disableMouse() 
        ## Loads everything here.
        #self.firstModel = self.loader.loadModel("models/babya.x")
        #self.firstTexture = self.loader.loadTexture("images/dragontail.tga")
        #self.world = loader.loadModel("./models/world.bam")
        self.firstModel = Actor("./models/babya.x", {"Run":"./models/babya.x"})
        self.secondModel = Actor("./models/babya.x", {"Run":"./models/babya.x"})
        
        # Load movie and its sound (if it has sound).
        self.movie = self.loader.loadTexture("videos/loading_screen.ogm")
        self.sound = self.loader.loadSfx("videos/loading_screen.ogm")

        # Make a plane to play the movie on.
        self.cm = CardMaker("plane")
        self.cm.setFrame(-1, 1, -1, 1)

        # Render that plane to the render2d for Panda.
        self.plane = self.render2d.attachNewNode(self.cm.generate())
        
        # Load movie into the texture plane.
        self.plane.setTexture(self.movie)

        # This can prevent squashing or distorting of the video.
        self.plane.setTexScale(TextureStage.getDefault(), self.movie.getTexScale())

        # 0 means do not loop infinitely.
        self.movie.setLoop(0)

        # If it has sound, synchronize it to the video.
        self.movie.synchronizeTo(self.sound)

        # Will set the Sound to loop.
        self.sound.setLoopCount(0)
        # Play the sound.
        self.sound.play()

        # Schedule bg image to show 10 seconds later.
        taskMgr.doMethodLater(1, self.loadImageAsPlane, "ImageLoader")
        
        """ To do, add more commands """
        #completed now to make it work??

        """ To do, implement text below model """
        #self.background_text = "Health"
        #self.backgroundText = OnscreenText(self.background_text, pos = (0.95,-0.95) , 
                                     # scale = 0.07, fg = (1,0.5,0.5,1), align = TextNode.ACenter, 
                                     # mayChange = 1)
                                     
                                     
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
            if key == "mvUp" and value == 1:
                self.firstModel.loop('Run', fromFrame = 0, toFrame = 20)
                hello = self.firstModel.getX()
                print "The x coordinate is now: ", hello
                x = hello + 5
                self.firstModel.setPos(x,0,0)
            elif key == "mvUp" and value == 0:
                self.firstModel.stop()
                print "The w key was released."
            else:
				print "That key isn't supported yet."				
        
    def loadWorld(self):
        #self.background_text = "Thy journey has begun..."
        #self.backgroundText.setText(self.background_text)

        # Remove the buttons and the background image.
        self.newGameButton.destroy()
        self.loadSavedGameButton.destroy()
        self.background.removeNode()

        # Set 3d background color.
        self.setBackgroundColor(0.5, 0.8, 0.8)
        
        self.background.removeNode()
        
        #self.world.reparentTo(self.render)
        self.firstModel.reparentTo(self.render)
        self.secondModel.reparentTo(self.render)
        
        self.firstModel.setScale(0.25, 0.25, 0.25)
        self.secondModel.setScale(0.1, 0.1, 0.1)
        
        self.firstModel.setPos(0, 100, 0)
        self.secondModel.setPos(20, 0, 0)
        
        # The Camera.
        self.mouseLook = MouseLook(base.cam)  
        # Will stop the sound if the button is pressed.
        self.sound.stop()
		
	#def setModelPosition(self, x=0, y=0, z=0):
		#self.firstModel.setPos(x,y,z)	
    def loadImageAsPlane(self, task): 
	# Loads image and puts it onscreen. 
        self.background = OnscreenImage(parent=render2d, image='images/Fireworks.jpg')

        # Let's add a button..
        self.newGameButton = DirectButton(text = ("New Game", None, None, None),
                                   pressEffect = 1, scale = .05, command = self.loadWorld)

        self.loadSavedGameButton = DirectButton(text = ("Load Game", None, None, None),
                                   pressEffect = 1, scale = .05, command = self.loadWorld)
        
        self.newGameButton.setPos(-1,1,-0.1)
        self.loadSavedGameButton.setPos(-1,1,-0.2)
        
        # Removes Intro Movie.
        self.plane.removeNode()
        
# Assign the class to a variable.        
app = Application()
# And finally, run it!!
app.run()

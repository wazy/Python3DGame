## Version 0.01
## Last change:
## 1:40 AM 3/16/2012

# Standard imports for Panda3d.
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task 
from panda3d.core import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *


import sys

class Application(ShowBase):
    def __init__(self):
        # Always add this!!! To load/render/etc.
        ShowBase.__init__(self)

        # Loads everything here.
        self.firstModel = self.loader.loadModel("models/proofOfConcept.obj")
        self.firstTexture = self.loader.loadTexture("images/proofOfConceptTexture.png")
        
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
        self.movie.setLoop(1)

        # If it has sound, synchronize it to the video.
        self.movie.synchronizeTo(self.sound)

        # Will set the Sound to loop.
        self.sound.setLoopCount(0)
        # Play the sound.
        self.sound.play()

        # Schedule bg image to show 10 seconds later.
        taskMgr.doMethodLater(10, self.loadImageAsPlane, "ImageLoader")

        """ To do, add more commands """
        self.accept("escape", sys.exit)


        """ To do, implement text above model """
        #self.background_text = "Health"
        #self.backgroundText = OnscreenText(self.background_text, pos = (0.95,-0.95) , 
                                     # scale = 0.07, fg = (1,0.5,0.5,1), align = TextNode.ACenter, 
                                     # mayChange = 1)
        
    def loadWorld(self):
        #self.background_text = "Thy journey has begun..."
        #self.backgroundText.setText(self.background_text)

        # Remove the button and the background image.
        self.button.destroy()
        self.background.removeNode()

        # Set 3d background color.
        self.setBackgroundColor(0.5, 0.8, 0.8)

        # Loads and renders the model.
        self.background.removeNode()
        self.firstModel.reparentTo(self.render)
        self.firstModel.setScale(0.75, 0.75, 0.75)
        self.firstModel.setPos(0, 50, 0)
        self.firstModel.setTexture(self.firstTexture)
        
        # Will stop the sound if the button is pressed.
        self.sound.stop()
		
    def loadImageAsPlane(self, task): 
	# Loads image and puts it onscreen. 
        self.background = OnscreenImage(parent=render2d, image='images/Fireworks.jpg')

        # Let's add a button..
        self.button = DirectButton(text = ("New Game", None, None, None),
                                   pressEffect = 1, scale = .05, command = self.loadWorld)
        
        # Removes Intro Movie.
        self.plane.removeNode()
        
# Assign the class to a variable.        
app = Application()
# And finally, run it!!
app.run()

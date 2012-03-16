## Written and experimented with by Daniel Ballard.
## 1:09 AM 3/4/2012

# Standard imports for Panda3d.
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task 
from panda3d.core import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *
from direct.gui.DirectGui import *

#import direct.directbase.DirectStart
import sys

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
        self.movie.setLoop(1)

        # If it has sound, synchronize it to the video.
        self.movie.synchronizeTo(self.sound)

        # Will set the Sound to loop.
        self.sound.setLoopCount(0)
        # Play the sound.
        self.sound.play()

        self.accept("escape", sys.exit)


        self.background_text = ""
        self.backgroundText = OnscreenText(self.background_text, pos = (0.95,-0.95) , 
                                      scale = 0.07, fg = (1,0.5,0.5,1), align = TextNode.ACenter, 
                                      mayChange = 1)
        
        # Let's add a button..
        self.button = DirectButton(text = ("New Game", None, None, None),
                                   pressEffect = 1, scale = .05, command = self.setText)

    def setText(self):
        self.background_text = "Thy journey has begun..."
        self.backgroundText.setText(self.background_text)
        # Schedule it to happen 0.1 seconds later.
        taskMgr.doMethodLater(0.1, self.loadImageAsPlane, "ImageLoader")
        #Will stop the sound if the button is pressed.
        self.sound.stop()
		
    def loadImageAsPlane(self, task): 
	# Load image and put onscreen 
        background = OnscreenImage(parent=render2d, image='models/Fireworks.jpg')
        
        
# Assign the class to a variable.        
app = Application()
# And finally, run it!!
app.run()

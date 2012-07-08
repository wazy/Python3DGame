## Daniel B.
## Version 0.03
## Last Revision 6/27/2012

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
        ## Loads everything here.
        #self.firstModel = self.loader.loadModel("models/babya.x")
        #self.firstTexture = self.loader.loadTexture("images/dragontail.tga")
        #self.world = loader.loadModel("./models/world.bam")
        self.firstModel = Actor("./models/babya.x", {"Run":"./models/babya.x"})
        self.secondModel = Actor("./models/babya.x", {"Run":"./models/babya.x"})
        
        #self.firstModel = self.loader.loadModel("./models/babya.x")
        #self.secondModel = self.loader.loadModel("./models/babya.x")
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

        # Schedule bg image to show x seconds later.
        taskMgr.doMethodLater(1, self.loadImageAsPlane, "ImageLoader")
        
        """ TODO: add more commands """
                                                                          
        self.keyMap = {"mvUp":0, "mvDown":0, "mvLeft":0, "mvRight":0, "shift1":0}

        self.accept("escape", sys.exit)
        
        self.accept("shift", self.setKey, ["shift1", 1])
        self.accept("w", self.setKey, ["mvUp", 1])
        self.accept("s", self.setKey, ["mvDown", 1])
        self.accept("a", self.setKey, ["mvLeft", 1])
        self.accept("d", self.setKey, ["mvRight", 1])	

        self.accept("shift-up", self.setKey, ["shift1", 0])
        self.accept("w-up", self.setKey, ["mvUp", 0])
        self.accept("s-up", self.setKey, ["mvDown", 0])
        self.accept("a-up", self.setKey, ["mvLeft", 0])
        self.accept("d-up", self.setKey, ["mvRight", 0])
        
        taskMgr.add(self.move,"moveTask")

        # Moving variable.
        self.isMoving = False
        
        #base.disableMouse()
        #camera.setPos(self.firstModel.getX(),self.firstModel.getY()+10,2)
        
        # Handle Collisions!
        self.cTrav = CollisionTraverser()
        collisionHandler = CollisionHandlerQueue()
        firstCollide = self.firstModel.attachNewNode(CollisionNode('smile'))
        firstCollide.node().addSolid(CollisionSphere(0,0,0,5))
        self.cTrav.addCollider(firstCollide, collisionHandler)
        smileyCollider = self.secondModel.attachNewNode(CollisionNode('smileycnode'))
        smileyCollider.node().addSolid(CollisionSphere(0, 0, 0, 5))
        self.cTrav.addCollider(smileyCollider, collisionHandler)
        
        
        def traverseTask(task=None):
  # as soon as a collison is detected, the collision queue handler will 
  #contain all the objects taking part in the collison, but we must sort 
  #that list first, so to have the first INTO object collided then the 
  #second and so on. Of course here it is pretty useless 'cos there is 
  #just one INTO object to collide with in the scene but this is the 
  #way to go when there are many other.
            collisionHandler.sortEntries()
            for i in range(collisionHandler.getNumEntries()):
                entry = collisionHandler.getEntry(i)
                print "collision"
                if task: return task.cont
            if task: return task.cont
        
        #add the collision system to the task manager    
        taskMgr.add(traverseTask, "tsk_traverse")
        
        #debugging purposes show collisions
        self.cTrav.showCollisions(render)

    def setKey(self, key, value):
        self.keyMap[key] = value            
        
    def move(self, task):

        camera.lookAt(self.firstModel)
        # If a move-key is pressed, move firstModel in the specified direction.
        if (self.keyMap["mvLeft"]!=0):
            self.firstModel.setH(self.firstModel.getH() + 300 * globalClock.getDt())
        if (self.keyMap["mvRight"]!=0):
            self.firstModel.setH(self.firstModel.getH() - 300 * globalClock.getDt())
        if (self.keyMap["mvUp"]!=0):
            if self.keyMap["shift1"]!=0:
                self.firstModel.setY(self.firstModel, + 50 * globalClock.getDt())
            else:				
                self.firstModel.setY(self.firstModel, + 25 * globalClock.getDt())
        if (self.keyMap["mvDown"]!=0):
            self.firstModel.setY(self.firstModel, - 25 * globalClock.getDt())
        print self.firstModel.getX()
        print self.firstModel.getY()
        print self.firstModel.getZ()
        # If firstModel is moving, loop the run animation.
        # If he is standing still, stop the animation.

        if (self.keyMap["mvUp"]!=0) or (self.keyMap["mvLeft"]!=0) or (self.keyMap["mvRight"]!=0) or (self.keyMap["mvDown"]!=0):
            if self.isMoving is False:
                self.firstModel.loop('Run', fromFrame = 0, toFrame = 20)
                self.isMoving = True
        else:
            if self.isMoving:
                self.firstModel.stop()
                #self.firstModel.pose("stand", 0)
                self.firstModel.loop('Run', fromFrame = 0, toFrame = 0)
                self.isMoving = False
        return task.cont
        
    def loadWorld(self):
        #self.background_text = "Thy journey has begun..."
        #self.background_text = "Health"
        #self.backgroundText = OnscreenText(self.background_text, pos = (0.95,-0.95) , 
        #                              scale = 0.07, fg = (1,0.5,0.5,1), align = TextNode.ACenter, 
        #                              mayChange = 1)
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
        self.secondModel.setPos(0, 120, 0)
        
        # The Camera.
        #self.mouseLook = MouseLook(base.cam)  
        # Will stop the sound if the button is pressed.
        self.sound.stop()
    def loadWorld2(self):
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
        with open('SaveData.txt') as f:
            int_list = [float(x) for x in line.split()
        self.firstModel.setPos(int_list[0], int_list[1], int_list[2])
        self.secondModel.setPos(0, 120, 0)
        
        # The Camera.
        #self.mouseLook = MouseLook(base.cam)  
        # Will stop the sound if the button is pressed.
        self.sound.stop()
        
    def loadImageAsPlane(self, task): 
    # Loads image and puts it onscreen. 
        self.background = OnscreenImage(parent=render2d, image='images/Fireworks.jpg')

        # Let's add a button..
        self.newGameButton = DirectButton(text = ("New Game", None, None, None),
                                   pressEffect = 1, scale = .05, command = self.loadWorld)

        self.loadSavedGameButton = DirectButton(text = ("Load Game", None, None, None),
                                   pressEffect = 1, scale = .05, command = self.loadWorld2)
        
        self.newGameButton.setPos(-1,1,-0.1)
        self.loadSavedGameButton.setPos(-1,1,-.2)
        
        # Removes Intro Movie.
        self.plane.removeNode()
        
# Assign the class to a variable.        
app = Application()
# And finally, run it!!
app.run()

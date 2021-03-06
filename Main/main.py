## Daniel B.
## Version 0.05
## Last Revision 1/15/2013

# Standard imports for Panda3d.
from direct.task.Task import Task 
from panda3d.core import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from UserInputControl import *
from panda3d.ai import *
from direct.gui.OnscreenText import OnscreenText
 
import direct.directbase.DirectStart
from pandac.PandaModules import *
 
from direct.showbase.DirectObject import DirectObject


# Custom import.
from FirstPersonCamera import MouseLook

import sys

pursue = True
class Application(DirectObject):
    def __init__(self):
        
        traverser = CollisionTraverser()
        
        base.physics = PhysicsCollisionHandler()
        base.physics.addInPattern("%fn-into%in")
        base.physics.addOutPattern("%fn-out-%in")
        base.enableParticles()
        
       # player = Player()
       # player.setCollision(traverser)
       
        ## Loads everything here.
        #self.firstModel1 = self.loader.loadModel("models/fig.obj")
        #self.firstTexture = self.loader.loadTexture("images/dragontail.tga")
        #self.world = loader.loadModel("./models/world.bam")
        self.firstModel = Actor("./models/babya.x", {"Run":"./models/babya.x"})
        self.secondModel = Actor("./models/babya.x", {"Run":"./models/babya.x"})
        #self.firstModel = self.loader.loadModel("./models/babya.x")
        #self.secondModel = self.loader.loadModel("./models/babya.x")
        # Load movie and its sound (if it has sound).
        self.movie = base.loader.loadTexture("videos/loading_screen.ogm")
        self.sound = base.loader.loadSfx("videos/loading_screen.ogm")
        self.health = 100
        # Make a plane to play the movie on.
        self.cm = CardMaker("plane")
        self.cm.setFrame(-1, 1, -1, 1)

        # Render that plane to the render2d for Panda.
        self.plane = base.render2d.attachNewNode(self.cm.generate())
        
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
        self.accept("q", self.saveGame)
        
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
        self.text = 1
        # Moving variable.
        self.isMoving = False
        #base.disableMouse()
        #camera.setPos(self.firstModel.getX(),self.firstModel.getY()+10,2)
        
        # Handle Collisions!
        self.cTrav = CollisionTraverser()
        collisionHandler = CollisionHandlerQueue()
        playerCollider = self.firstModel.attachNewNode(CollisionNode('player'))
        playerCollider.node().addSolid(CollisionSphere(0,0,0,5))
        self.cTrav.addCollider(playerCollider, collisionHandler)
        objectCollider = self.secondModel.attachNewNode(CollisionNode('wall/object'))
        objectCollider.node().addSolid(CollisionSphere(0, 0, 0, 5))
        self.cTrav.addCollider(objectCollider, collisionHandler)
        
        
        def traverseTask(task=None):
            # handler contains all objects in collisions
            # sort them first to find out first, second, etc
            collisionHandler.sortEntries()
            for i in range(collisionHandler.getNumEntries()):
                entry = collisionHandler.getEntry(i)
                print "collision", self.health
                alive = False
                if (self.health > 0):
                    alive = True
                if (alive):
                    self.health = self.health - 1
                    self.addState(0.9, "Collision, your hp is: " + str(self.health))
                else:
                    self.addState(0.9, "You have died.")
                    self.firstModel.play('Death', fromFrame = 306, toFrame = 327)
                    self.AIbehaviors.wander(5, 0, 10, 1.0)
                    self.AIworld.update()   
                if task: return task.cont
            if task: return task.cont
        
        #add the collision system to the task manager    
        taskMgr.add(traverseTask, "tsk_traverse")
        
        #debugging purposes show collisions
        self.cTrav.showCollisions(render)

    # called for modelLocation and returns a string 
    # i.e. "0.0 100.0 0.0"
    def modelLocation(self):
        x = self.firstModel.getX()
        y = self.firstModel.getY()
        z = self.firstModel.getZ()
        position = str(x) + " " + str(y) + " " + str(z)
        return position
    
    # calls for position then writes the location    
    def saveGame(self):
        with open("SaveData.txt", "w") as save:
            save.write(self.modelLocation())
        save.close()
        print "location saved", self.modelLocation()

    def setKey(self, key, value):
        self.keyMap[key] = value            
        
    def addState(self, pos, msg):
        if (self.text != 1):
            self.text.destroy()
        self.text = OnscreenText(text=msg, style=1, fg=(1,1,1,1), font = loader.loadFont("cmss12"),
                            pos=(-1.3, pos), align=TextNode.ALeft, scale = .1)
        return self.text

    def move(self, task):
        camera.lookAt(self.firstModel)
        # If a move-key is pressed, move firstModel in the specified direction.
        ##TODO better movement
        startPos = self.firstModel.getPos()
        #if (self.keyMap["mvLeft"]!=0):
            #self.firstModel.setPos(startPos + Point3(-0.75,0,0))
        if (self.keyMap["mvLeft"]!=0):
            self.firstModel.setH(self.firstModel.getH() + 450 * globalClock.getDt())
        if (self.keyMap["mvRight"]!=0):
            self.firstModel.setH(self.firstModel.getH() - 450 * globalClock.getDt())
        if (self.keyMap["mvUp"]!=0):
            if self.keyMap["shift1"]!=0:
                self.firstModel.setY(self.firstModel, + 150 * globalClock.getDt())
            else:
                self.firstModel.setY(self.firstModel, + 100 * globalClock.getDt())
        if (self.keyMap["mvDown"]!=0):
            self.firstModel.setY(self.firstModel, - 75 * globalClock.getDt())

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
                self.firstModel.loop('Stand', fromFrame = 22, toFrame = 52)
                self.isMoving = False
        return task.cont
        
    def loadNewWorld(self):
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
        base.setBackgroundColor(0.5, 0.8, 0.8)
        
        self.background.removeNode()
        
        #self.world.reparentTo(self.render)
        
        self.firstModel.reparentTo(base.render)
        self.secondModel.reparentTo(base.render)

        self.firstModel.setScale(0.25, 0.25, 0.25)
        self.secondModel.setScale(0.1, 0.1, 0.1)
        
        self.firstModel.setPos(0, 100, 0)
        self.secondModel.setPos(100, -120, 0)
        
        # The Camera.
        #self.mouseLook = MouseLook(base.cam)  
        # Will stop the sound if the button is pressed.
        self.sound.stop()
        
        #ai
        self.setAI()
        
    def loadSavedWorld(self):
        self.newGameButton.destroy()
        self.loadSavedGameButton.destroy()
        self.background.removeNode()

        # Set 3d background color.
        base.setBackgroundColor(0.5, 0.8, 0.8)
        
        self.background.removeNode()
        
        #self.world.reparentTo(self.render)
        self.firstModel.reparentTo(base.render)
        self.secondModel.reparentTo(base.render)
        
        self.firstModel.setScale(0.25, 0.25, 0.25)
        self.secondModel.setScale(0.1, 0.1, 0.1)
        
        with open('SaveData.txt') as load:
            for line in load:
                int_list = [float(x) for x in line.split()]        
        load.close()
        
        self.firstModel.setPos(int_list[0], int_list[1], int_list[2])
        self.secondModel.setPos(0, 120, 0)
        
        # The Camera.
        #self.mouseLook = MouseLook(base.cam)  
        # Will stop the sound if the button is pressed.
        self.sound.stop()
        
        #ai
        self.setAI()
        
    def loadImageAsPlane(self, task): 
    # Loads image and puts it onscreen. 
        self.background = OnscreenImage(parent=render2d, image='images/Fireworks.jpg')

        # Let's add a button..
        self.newGameButton = DirectButton(text = ("New Game", None, None, None),
                                   pressEffect = 1, scale = .05, command = self.loadNewWorld)

        self.loadSavedGameButton = DirectButton(text = ("Load Game", None, None, None),
                                   pressEffect = 1, scale = .05, command = self.loadSavedWorld)
        
        self.newGameButton.setPos(-1,1,-0.1)
        self.loadSavedGameButton.setPos(-1,1,-.2)
        
        # Removes Intro Movie.
        self.plane.removeNode()

    def setAI(self):
        #Creating AI World
        self.AIworld = AIWorld(render)
 
        self.AIchar = AICharacter("seeker",self.secondModel, 100, 0.05, 5)
        self.AIworld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        
        #currently pursues the player.
        #if (pursue):
        self.AIbehaviors.pursue(self.firstModel, 0.2)
        #else:
       # self.AIbehaviors.evade(self.firstModel, 15, 80, 0.8)
            
        self.secondModel.loop('Run', fromFrame = 0, toFrame = 20)
 
        #AI World update        
        taskMgr.add(self.AIUpdate,"AIUpdate")
         
    #to update the AIWorld    
    def AIUpdate(self,task):
        self.AIworld.update()            
        return Task.cont
        
# Assign the class to a variable.        
app = Application()
# And finally, run it!!
run()

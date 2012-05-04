import direct.directbase.DirectStart
from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.actor.Actor import Actor
#for Pandai
from panda3d.ai import *
 
class World(DirectObject):
 
    def __init__(self):
        base.disableMouse()
        base.cam.setPosHpr(0,0,55,0,-90,0)
 
        self.loadModels()
        self.setAI()
 
    def loadModels(self):
		# Seeker
        ralphStartPos = Vec3(2, 0, 0)
        self.fleer = Actor("models/ralph",
                                 {"run":"models/ralph-run"})
        self.fleer.reparentTo(render)
        self.fleer.setScale(0.5)
        self.fleer.setPos(ralphStartPos)
        # Target
        self.target = loader.loadModel("models/arrow")
        self.target.setColor(1,0,0)
        self.target.setPos(5,0,0)
        self.target.setScale(1)
        self.target.reparentTo(render)
 
    def setAI(self):
        #Creating AI World
        self.AIworld = AIWorld(render)
 
        self.AIchar = AICharacter("fleer",self.fleer, 100, 0.05, 5)
        self.AIworld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
 
        self.AIbehaviors.flee(self.target, 5, 5)
        self.fleer.loop("run")
 
        #AI World update        
        taskMgr.add(self.AIUpdate,"AIUpdate")
 
    #to update the AIWorld    
    def AIUpdate(self,task):
        self.AIworld.update()            
        return Task.cont
 
w = World()
run()

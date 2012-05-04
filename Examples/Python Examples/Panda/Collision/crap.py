#Learning about Projected Texturing, Terrain Decals 
#Author:  brianinsuwon, brianinsuwon@yahoo.com, July 1, 2008 

import direct.directbase.DirectStart 
from direct.gui.OnscreenText import OnscreenText 
from direct.actor.Actor import Actor 
from direct.task.Task import Task 
from direct.showbase.DirectObject import DirectObject 
import random, sys, os, math 
from pandac.PandaModules import * 
from direct.interval.IntervalGlobal import * 


class World(DirectObject): 
                  
                        
    def __init__(self): 
        
        #add screen instructions and output 
        self.title = OnscreenText(text = "Learning about Projected Textures", 
                         style = 1, fg = (1,1,1,0.8), pos = (-1.2,0.9), 
                         align = TextNode.ALeft,  scale = .08) 
        self.inst1 = OnscreenText(text = "    Keys A,S,D: increases H,P,R values", 
                         style = 1, fg = (1,1,1,0.8), pos = (-1.2,0.8), 
                         align = TextNode.ALeft,  scale = .07) 
        self.inst2 = OnscreenText(text = "    Keys Z,X,C: decreases H,P,R values", 
                         style = 1, fg = (1,1,1,0.8), pos = (-1.2,0.7), 
                         align = TextNode.ALeft,  scale = .07) 
        self.inst3 = OnscreenText(text = "    Keys Q,W: increase,decrease Z value", 
                         style = 1, fg = (1,1,1,0.8), pos = (-1.2,0.6), 
                         align = TextNode.ALeft,  scale = .07) 
        self.inst4 = OnscreenText(text = "    Keys E,R: increase,decrease X value", 
                         style = 1, fg = (1,1,1,0.8), pos = (-1.2,0.5), 
                         align = TextNode.ALeft,  scale = .07) 
        self.inst5 = OnscreenText(text = "    Keys N,M: increase,decrease mapScale", 
                         style = 1, fg = (1,1,1,0.8), pos = (-1.2,0.4), 
                         align = TextNode.ALeft,  scale = .07) 
        self.inst6 = OnscreenText(text = "    Keys J,K: increase,decrease texScale", 
                         style = 1, fg = (1,1,1,0.8), pos = (-1.2,0.3), 
                         align = TextNode.ALeft,  scale = .07) 
        self.output1 = OnscreenText(text = " ", 
                         style = 1, fg = (1,1,1,0.8), pos = (-1.2,0.2), 
                         align = TextNode.ALeft,  scale = .07, mayChange=1) 
        self.output2 = OnscreenText(text = " ", 
                         style = 1, fg = (1,1,1,0.8), pos = (-1.2,0.1), 
                         align = TextNode.ALeft,  scale = .07, mayChange=1) 
        self.output3 = OnscreenText(text = " ", 
                         style = 1, fg = (1,1,1,0.8), pos = (-1.2,0.0), 
                         align = TextNode.ALeft,  scale = .07, mayChange=1) 
        
        #setup initial values 
        self.mapScale =1 
        self.texScaleU=1 
        self.texScaleV=1 
                
        #set the camera 
        base.oobe()        
        base.disableMouse() 
        base.camera.reparentTo(render) 
        base.camera.setPos(0,0,1) 

        #set up lights 
        self.alight = AmbientLight('alight') 
        self.alight.setColor(VBase4(1, 1, 1, 1)) 
        self.alnp = render.attachNewNode(self.alight) 
        render.setLight(self.alnp) 
        
        #set up my floor 
            #floor was created in Blender using a subdivided plane 
            #texture was applied in Blender 
        self.floor = loader.loadModel('models/greenFloor2.egg') 
        self.floor.reparentTo(render) 
        self.floor.setPos(0,0,0) 
        self.floor.setScale(self.mapScale) 
        
        #set up my decal texture 
            #decal was maade in gimp, using a transparent background 
        self.tex = loader.loadTexture('textures/ring.png') 
        self.ts = TextureStage('ts') 
        self.ts.setMode(TextureStage.MDecal) 
            #needed the lines below to get only 1 ring,without this, floor is covered in rings 
        self.tex.setWrapU(Texture.WMBorderColor) 
        self.tex.setWrapV(Texture.WMBorderColor) 
        self.tex.setBorderColor(VBase4(1,1, 1, 0)) #needed to set my alpha to zero 
        
        self.floor.setTexScale(self.ts, self.texScaleU, self.texScaleV) 
  
        #setup the projector 
        self.proj = render.attachNewNode(LensNode('proj')) 
        self.lens = PerspectiveLens() 
        self.proj.node().setLens(self.lens) 
        self.proj.reparentTo(render) 
        self.proj.setPos(0, 0, 10) 
        self.proj.setHpr(0, 90, 0) 
    
        self.floor.projectTexture(self.ts, self.tex, self.proj) 


        #setup keyboard controls 
        self.accept("escape", sys.exit) 
        
        self.accept("a", self.hupF) 
        self.accept("s", self.pupF) 
        self.accept("d", self.rupF) 
        
        self.accept("z", self.hdownF) 
        self.accept("x", self.pdownF) 
        self.accept("c", self.rdownF) 
        
        
        self.accept("q", self.zupF) 
        self.accept("w", self.zdownF) 
        self.accept("e", self.xupF) 
        self.accept("r", self.xdownF) 
        
        self.accept("n", self.mapScaleupF) 
        self.accept("m", self.mapScaledownF) 
        self.accept("j", self.texScaleupF) 
        self.accept("k", self.texScaledownF) 
    

        
    def zupF (self): 
        self.proj.setZ(self.proj.getZ()+5) 
        self.updateF() 
    def zdownF (self): 
        self.proj.setZ(self.proj.getZ()-5) 
        self.updateF() 
    def xupF (self): 
        self.proj.setX(self.proj.getX()+5) 
        self.updateF() 
    def xdownF (self): 
        self.proj.setX(self.proj.getX()-5) 
        self.updateF() 
        
    def hupF (self): 
        self.proj.setH(self.proj.getH()+5) 
        self.updateF() 
    def pupF (self): 
        self.proj.setP(self.proj.getP()+5) 
        self.updateF() 
    def rupF (self): 
        self.proj.setR(self.proj.getR()+5) 
        self.updateF() 
    def hdownF (self): 
        self.proj.setH(self.proj.getH()-5) 
        self.updateF() 
    def pdownF (self): 
        self.proj.setP(self.proj.getP()-5) 
        self.updateF() 
    def rdownF (self): 
        self.proj.setR(self.proj.getR()-5) 
        self.updateF() 
        
    def mapScaleupF (self): 
        self.mapScale = self.mapScale +1 
        self.floor.setScale(self.mapScale) 
        self.updateF() 
    def mapScaledownF (self): 
        self.mapScale = self.mapScale -1 
        self.floor.setScale(self.mapScale) 
        self.updateF() 
        
    def texScaleupF (self): 
        self.texScaleU = self.texScaleU +1 
        self.texScaleV = self.texScaleV +1 
        self.floor.setTexScale(self.ts, self.texScaleU, self.texScaleV) 
        self.updateF() 
    def texScaledownF (self): 
        self.texScaleU = self.texScaleU -1 
        self.texScaleV = self.texScaleV -1 
        self.floor.setTexScale(self.ts, self.texScaleU, self.texScaleV) 
        self.updateF() 
  
        
    def updateF(self): 
        ot1 = "Projector Position: " +   str(self.proj.getPos())      
        self.output1.setText(ot1) 
        ot2 = "Projector Hpr: " +   str(self.proj.getHpr()) 
        self.output2.setText(ot2) 
        ot3 = "texture scales U and V = %s , %s" %  (str(self.texScaleU), str(self.texScaleU)) 
        self.output3.setText(ot3) 
      
        
w = World() 
run() 


from pandac.PandaModules import * 
from direct.task import Task 
from direct.showbase.DirectObject import DirectObject 

class MouseLook (DirectObject): 
   """ 
   simple camera mouse look and WASD key control 
   r and f keys move camera up/down 
   q and e keys rotate camera    
   hit enter to start/stop controls 
   """ 

   def __init__(self,camera): 
    
      self.camera  = camera 
      self.running = False 
      self.time    = 0 
      self.centX   = base.win.getProperties().getXSize()/2 
      self.centY   = base.win.getProperties().getYSize()/2 

      # key controls 
      self.forward   = False 
      self.backward  = False 
      self.left      = False 
      self.right     = False 
      self.up        = False 
      self.down      = False 
      self.up        = False 
      self.down      = False 
      self.rollLeft  = False 
      self.rollRight = False 

      # sensitivity settings 
      self.movSens  = 2 
      self.rollSens = 50 
      self.sensX = self.sensY = 0.2       
       
      self.accept("enter",self.toggle)           

   # camera rotation task 
   def cameraTask(self,task): 
      dt = task.time - self.time 
       
      # handle mouse look 
      md = base.win.getPointer(0)        
      x = md.getX() 
      y = md.getY() 
       
      if base.win.movePointer(0, self.centX, self.centY):    
         self.camera.setH(self.camera,self.camera.getH(self.camera) - (x - self.centX) * self.sensX) 
         self.camera.setP(self.camera,self.camera.getP(self.camera) - (y - self.centY) * self.sensY)       

      # handle keys: 

      if self.forward == True: 
         self.camera.setY(self.camera, self.camera.getY(self.camera) + self.movSens*dt) 
      if self.backward == True: 
         self.camera.setY(self.camera, self.camera.getY(self.camera) - self.movSens*dt) 
      if self.left == True: 
         self.camera.setX(self.camera, self.camera.getX(self.camera) - self.movSens*dt) 
      if self.right == True: 
         self.camera.setX(self.camera, self.camera.getX(self.camera) + self.movSens*dt) 
      if self.up == True: 
         self.camera.setZ(self.camera, self.camera.getZ(self.camera) + self.movSens*dt) 
      if self.down == True: 
         self.camera.setZ(self.camera, self.camera.getZ(self.camera) - self.movSens*dt)           
      if self.rollLeft == True: 
         self.camera.setR(self.camera, self.camera.getR(self.camera) - self.rollSens*dt) 
      if self.rollRight == True: 
         self.camera.setR(self.camera, self.camera.getR(self.camera) + self.rollSens*dt) 
          
      self.time = task.time       
      return task.cont 

   def start(self):    
      base.disableMouse() 
      # hide mouse cursor, comment these 3 lines to see the cursor 
      props = WindowProperties() 
      props.setCursorHidden(True) 
      base.win.requestProperties(props) 
      # reset mouse to start position: 
      base.win.movePointer(0, self.centX, self.centY)             
      taskMgr.add(self.cameraTask, 'HxMouseLook::cameraTask')        
      #Task for changing direction/position 
      self.accept("w",setattr,[self,"forward",True]) 
      self.accept("w-up",setattr,[self,"forward",False]) 
      self.accept("s",setattr,[self,"backward",True]) 
      self.accept("s-up",setattr,[self,"backward",False]) 
      self.accept("a",setattr,[self,"left",True]) 
      self.accept("a-up",setattr,[self,"left",False]) 
      self.accept("d",setattr,[self,"right",True]) 
      self.accept("d-up",setattr,[self,"right",False]) 
      self.accept("r",setattr,[self,"up",True]) 
      self.accept("r-up",setattr,[self,"up",False]) 
      self.accept("f",setattr,[self,"down",True]) 
      self.accept("f-up",setattr,[self,"down",False]) 
      self.accept("q",setattr,[self,"rollLeft",True]) 
      self.accept("q-up",setattr,[self,"rollLeft",False]) 
      self.accept("e",setattr,[self,"rollRight",True]) 
      self.accept("e-up",setattr,[self,"rollRight",False]) 
       
   def stop(self): 
      taskMgr.remove("HxMouseLook::cameraTask") 

      base.enableMouse() 
      props = WindowProperties() 
      props.setCursorHidden(False) 
      base.win.requestProperties(props)        
       
      self.forward  = False 
      self.backward = False 
      self.left     = False 
      self.right    = False 
      self.up       = False 
      self.down     = False 
      self.rollLeft = False 

      self.ignore("w") 
      self.ignore("w-up") 
      self.ignore("s") 
      self.ignore("s-up") 
      self.ignore("a") 
      self.ignore("a-up") 
      self.ignore("d") 
      self.ignore("d-up") 
      self.ignore("r") 
      self.ignore("r-up") 
      self.ignore("f") 
      self.ignore("f-up") 
      self.ignore("q") 
      self.ignore("q-up") 
      self.ignore("e") 
      self.ignore("e-up")              
       
   #call to stop control system 
   def toggle(self): 
      if(self.running): 
         self.stop() 
         self.running=False 
      else: 
         self.start() 
         self.running=True 

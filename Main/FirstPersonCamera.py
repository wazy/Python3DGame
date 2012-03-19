from direct.showbase import DirectObject 
from pandac.PandaModules import WindowProperties 
from direct.task import Task 

##   First person camera controller, "free view"/"FPS" style. 
#    
#    Simple camera mouse look and WASD key controller 
#    shift to go faster, 
#    r and f keys move camera up/down, 
#    q and e keys rotate camera, 
#    hit enter to start/stop controls. 
#    If a refNode is specified, heading and up/down are performed wrt the 
#    reference node (usually the root node of scene, i.e. base.render) 
#    and camera behaves more similarly to an "FPS" camera. 
class FirstPersonCamera(DirectObject.DirectObject): 
    ''' 
    First person camera controller. 
    ''' 
    
    ## Constructor 
    # @param gameaApp: the game application to which this controller 
    # applies, that should be ShowBase derived. 
    # @param camera: the camera to which this controller applies 
    # @param refNode: reference node wrt heading and up/down are performed 
    def __init__(self, gameApp, camera, refNode=None): 
        ''' 
        Constructor 
        ''' 
        
        self.gameApp = gameApp 
        self.camera = camera 
        if refNode != None: 
            self.refNode = refNode 
        else: 
            self.refNode = self.camera 
        self.running = False 
        self.time = 0 
        self.centX = self.gameApp.win.getProperties().getXSize() / 2 
        self.centY = self.gameApp.win.getProperties().getYSize() / 2 
        
        # key controls 
        self.forward = False 
        self.backward = False 
        self.fast = 1.0 
        self.left = False 
        self.right = False 
        self.up = False 
        self.down = False 
        self.up = False 
        self.down = False 
        self.rollLeft = False 
        self.rollRight = False 
        
        # sensitivity settings 
        self.movSens = 2 
        self.movSensFast = self.movSens * 5 
        self.rollSens = 50 
        self.sensX = self.sensY = 0.2        
          
        self.accept("enter", self.toggle)            

    ## Camera rotation task 
    def cameraTask(self, task): 
        dt = task.time - self.time 
          
        # handle mouse look 
        md = self.gameApp.win.getPointer(0)        
        x = md.getX() 
        y = md.getY() 
          
        if self.gameApp.win.movePointer(0, self.centX, self.centY):    
            self.camera.setH(self.refNode, self.camera.getH(self.refNode) 
                             - (x - self.centX) * self.sensX) 
            self.camera.setP(self.camera, self.camera.getP(self.camera) 
                             - (y - self.centY) * self.sensY)        
        
        # handle keys: 
        if self.forward == True: 
            self.camera.setY(self.camera, self.camera.getY(self.camera) 
                             + self.movSens * self.fast * dt) 
        if self.backward == True: 
            self.camera.setY(self.camera, self.camera.getY(self.camera) 
                             - self.movSens * self.fast * dt) 
        if self.left == True: 
            self.camera.setX(self.camera, self.camera.getX(self.camera) 
                             - self.movSens * self.fast * dt) 
        if self.right == True: 
            self.camera.setX(self.camera, self.camera.getX(self.camera) 
                             + self.movSens * self.fast * dt) 
        if self.up == True: 
            self.camera.setZ(self.refNode, self.camera.getZ(self.refNode) 
                             + self.movSens * self.fast * dt) 
        if self.down == True: 
            self.camera.setZ(self.refNode, self.camera.getZ(self.refNode) 
                             - self.movSens * self.fast * dt)            
        if self.rollLeft == True: 
            self.camera.setR(self.camera, self.camera.getR(self.camera) 
                             - self.rollSens * dt) 
        if self.rollRight == True: 
            self.camera.setR(self.camera, self.camera.getR(self.camera) 
                             + self.rollSens * dt) 
            
        self.time = task.time        
        return Task.cont 

    ## Start to control the camera 
    def start(self):    
        self.gameApp.disableMouse() 
        # hide mouse cursor, comment these 3 lines to see the cursor 
        props = WindowProperties() 
        props.setCursorHidden(True) 
        self.gameApp.win.requestProperties(props) 
        # reset mouse to start position: 
        self.gameApp.win.movePointer(0, self.centX, self.centY)              
        self.gameApp.taskMgr.add(self.cameraTask, 'HxMouseLook::cameraTask')        
        #Task for changing direction/position 
        self.accept("w", setattr, [self, "forward", True]) 
        self.accept("shift-w", setattr, [self, "forward", True]) 
        self.accept("w-up", setattr, [self, "forward", False]) 
        self.accept("s", setattr, [self, "backward", True]) 
        self.accept("shift-s", setattr, [self, "backward", True]) 
        self.accept("s-up", setattr, [self, "backward", False]) 
        self.accept("a", setattr, [self, "left", True]) 
        self.accept("shift-a", setattr, [self, "left", True]) 
        self.accept("a-up", setattr, [self, "left", False]) 
        self.accept("d", setattr, [self, "right", True]) 
        self.accept("shift-d", setattr, [self, "right", True]) 
        self.accept("d-up", setattr, [self, "right", False]) 
        self.accept("r", setattr, [self, "up", True]) 
        self.accept("shift-r", setattr, [self, "up", True]) 
        self.accept("r-up", setattr, [self, "up", False]) 
        self.accept("f", setattr, [self, "down", True]) 
        self.accept("shift-f", setattr, [self, "down", True]) 
        self.accept("f-up", setattr, [self, "down", False]) 
        self.accept("q", setattr, [self, "rollLeft", True]) 
        self.accept("q-up", setattr, [self, "rollLeft", False]) 
        self.accept("e", setattr, [self, "rollRight", True]) 
        self.accept("e-up", setattr, [self, "rollRight", False]) 
        self.accept("shift", setattr, [self, "fast", 5.0]) 
        self.accept("shift-up", setattr, [self, "fast", 1.0]) 
                
    ## Stop to control the camera  
    def stop(self): 
        self.gameApp.taskMgr.remove("HxMouseLook::cameraTask") 
        
        self.gameApp.enableMouse() 
        props = WindowProperties() 
        props.setCursorHidden(False) 
        self.gameApp.win.requestProperties(props)        
          
        self.forward = False 
        self.backward = False 
        self.left = False 
        self.right = False 
        self.up = False 
        self.down = False 
        self.rollLeft = False 
        
        self.ignore("w") 
        self.ignore("shift-w") 
        self.ignore("w-up") 
        self.ignore("s") 
        self.ignore("shift-s") 
        self.ignore("s-up") 
        self.ignore("a") 
        self.ignore("shift-a") 
        self.ignore("a-up") 
        self.ignore("d") 
        self.ignore("shift-d") 
        self.ignore("d-up") 
        self.ignore("r") 
        self.ignore("shift-r") 
        self.ignore("r-up") 
        self.ignore("f") 
        self.ignore("shift-f") 
        self.ignore("f-up") 
        self.ignore("q") 
        self.ignore("q-up") 
        self.ignore("e") 
        self.ignore("e-up") 
        self.ignore("shift") 
        self.ignore("shift-up")              
        
    ## Call to start/stop control system 
    def toggle(self): 
        if(self.running): 
            self.stop() 
            self.running = False 
        else: 
            self.start() 
            self.running = True 

from direct.showbase.ShowBase import ShowBase 
#import from FirstPersonCamera.py 
from FirstPersonCamera import FirstPersonCamera 

## Main game class. 
class TestCamera(ShowBase): 
    ''' 
    Main TestCamera class. 
    ''' 

    def __init__(self): 
        ''' 
        Constructor 
        ''' 
        ShowBase.__init__(self) 

        # Load the environment model. 
        self.environ = self.loader.loadModel("models/environment") 
        # Reparent the model to render. 
        self.environ.reparentTo(self.render) 
        # Apply scale and position transforms on the model. 
        self.environ.setScale(0.25, 0.25, 0.25) 
        self.environ.setPos(-8, 42, 0) 
          
        self.mouseLook = FirstPersonCamera(self, self.cam, self.render)          
          

if __name__ == '__main__': 
    gameApp = TestCamera() 
    gameApp.run() 

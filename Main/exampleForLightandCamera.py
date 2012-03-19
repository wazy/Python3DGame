# Definitions
class World(DirectObject):
	def __init__(self):
		self.LoadTerrain()

		# Lights
		self.LoadLight()

		# Camera
		self.LoadCamera()

        def LoadTerrain(self):
		self.counter = loader.loadModel('models/counter.egg')
        	self.counter.reparentTo(render)
        	base.setBackgroundColor(0.0,0.3,0.0)
	def LoadLight(self):
		''' Create an Ambient light as well as a point light
		'''
		plight = AmbientLight('my plight')
		plight.setColor(VBase4(0.12, 0.12, 0.12, 1))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)

		light2 = PointLight('pointlight')
		plnp2 = render.attachNewNode(light2)
		plnp2.setPos(2,2,2)
		render.setLight(plnp2)

	def LoadCamera(self):
		# Camera
		base.camera.setPos(4,-10,10)
		base.camera.lookAt(self.counter)
		mat=Mat4(camera.getMat())
		mat.invertInPlace()
		base.mouseInterfaceNode.setMat(mat)

# Application code
if __name__ == "__main__":
    w = World()
    run()

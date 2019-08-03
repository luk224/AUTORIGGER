import maya.cmds as maya
class SphereClass:
    def __init__(self):
        self.win = maya.window(t='Rigger', wh=(300,200))
        maya.columnLayout()
        self.numSpheres = maya.intField(minValue =1)
        maya.button(label = 'Make locators', command = self.makeLocators)
        maya.button(label = 'Make joints', command = self.makeJoints)
        #maya.showWindow(win)
        
        
    def makeSpheres(self, *args):           
        number = maya.intField(self.numSpheres, q=True, value=True)
        print number
        for i in range(0,number):
            maya.polySphere()
            maya.move(i*2,0,0)
            
            
    def makeLocators(self, *args):
        self.list_guias = []
        number = maya.intField(self.numSpheres, q=True, value=True)
        for i in range(0,number):
            guia = (maya.spaceLocator( n='spine_{0}'.format(i) + '_loc' ))[0]
            maya.xform(guia,t=[i*4,0,0])
            self.list_guias.append(guia)
            
    def makeJoints(self, *args):        
        maya.select(cl =1)
        for guia in self.list_guias:            
            name= guia.replace('loc','jnt')            
            jnt = maya.joint(n=name)            
            posGuia = maya.xform(guia, q=True, ws=True, t=True)#hace Query (q=True), encuentra el objeto con el nombre de la guia, y devuelve la transformacion (t=True) en coordenadas globales (ws=True), si 1=False, no busca un atributo, sino que lo modifica con uno dado.
            maya.delete(guia)
            maya.xform(jnt,ws=True,t=posGuia)
        
            
SphereClass()
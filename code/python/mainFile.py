from Escuela import splineJointsScript

reload(splineJointsScript)
from Escuela.splineJointsScript import splineJoints


# Este script permite crear 3 c cadenas de huesos(rotacion, posicion y bindeo) a partir de una curva, un control
# para cada uno de los huesos y uno general con conexion directa a todos ellos
# ejemplo de uso con una curva creada y un objeto que hara de control:
#Se ha usado en los tentaculos de Octo.


'''
import testScript
reload(testScript)
from testScript import mainClass

autorigger.testFunction(side="cn", name="bigote",zone="A")

#Select curve.#
###############
autorigger.defineCurve()

#Select ctlObject.#
###############
autorigger.defineCtlObject()

autorigger.spine.createPosOriBindChains()

'''



class mainClass:

    def __init__(self):
        print("init mainClass")

    def makeChain(self,side="cn", name="tentacle",zone="A"):

        self.spine= splineJoints( side=side, name=name,zone=zone)

    def defineCurve(self):
        self.spine.defineCurve()

    def defineCtlObject(self):
        self.spine.defineCtlObj()



from maya import cmds , OpenMaya
selection = cmds.ls(sl=1)
selection
posPole = getPolePosition(selection, 2)

def getPolePosition (chain=[] ,offset = 5) :
	''' Method to get poleVector position
	chain : (str) array of bones one chain
	offset :(int) distance to move the poleVector position
	
	ejemplo de uso:
    
	getPolePosition (chain = ['lf_LeftArm_jnt','lf_LeftForeArm_jnt','lf_LeftHand_jnt'],offset = 5)
	
	
	'''
        start = cmds.xform (chain[0], q = 1, ws =1, t = 1)
        mid = cmds.xform (chain[1], q = 1, ws =1, t = 1)
        end = cmds.xform (chain[2], q = 1, ws =1, t = 1)
        
        startV = OpenMaya.MVector(start[0] ,start[1],start[2])
        midV = OpenMaya.MVector(mid[0] ,mid[1],mid[2])
        endV = OpenMaya.MVector(end[0] ,end[1],end[2])
        startEnd = endV - startV
        startMid = midV - startV
        dotP = startMid * startEnd
        proj = float(dotP) / float(startEnd.length())
        startEndN = startEnd.normal()
        projV = startEndN * proj
        arrowV = startMid - projV
        arrowV*= offset
        finalV = arrowV + midV
        loc = cmds.spaceLocator()[0]
        cmds.xform(loc , ws =1 , t= (finalV.x , finalV.y ,finalV.z))  
        posPole = cmds.xform(loc , a =1 , q =1, t=1)  
        cmds.delete (loc)  
        return posPole 
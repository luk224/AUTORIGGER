import maya.cmds as cmds

'''
list = cmds.ls( sl=1)
for e in list:
    name= e.replace ('jnt', 'ctr')
    ctr = createControl(nameCtrl= name,rotateTo=e,translateTo=e, scale = 1, direccion = 'z')
    cmds.orientConstraint (ctr,e)
    
    
'''    



def createControl (


    nameCtrl='new',
    scale= 1,
    parentTo='',
    rotateTo='',
    translateTo='',
    direccion = 'x',
    scaleTo=''):
        
    if direccion == 'x':    
        ctr = cmds.circle (name=nameCtrl,c= (0,0,0),nr= (1,0,0),r = scale,ch= 1)[0]
    if direccion == 'y':    
        ctr = cmds.circle (name=nameCtrl,c= (0,0,0),nr= (0,1,0),r = scale,ch= 1)[0]    
    if direccion == 'z':    
        ctr = cmds.circle (name=nameCtrl,c= (0,0,0),nr= (0,0,1),r = scale,ch= 1)[0]
        
    ctrlOffset = cmds.group (em= 1,n= ctr +'_offset')
    cmds.parent (ctr,ctrlOffset)
   
    # color control
    ctrlShapes = cmds.listRelatives( ctr, s = 1 )
    [ cmds.setAttr( s + '.ove', 1 ) for s in ctrlShapes ]
    
    if nameCtrl.startswith( 'l_' ):
        
        [ cmds.setAttr( s + '.ovc', 6 ) for s in ctrlShapes ]
    
    elif nameCtrl.startswith( 'r_' ):
        
        [cmds.setAttr( s + '.ovc', 13 ) for s in ctrlShapes ]
    
    else:
        
        [cmds.setAttr( s + '.ovc', 22 ) for s in ctrlShapes ]    
   # translate control
    
    if cmds.objExists( translateTo ):
        
        cmds.delete( cmds.pointConstraint( translateTo, ctrlOffset ) )
    
    # rotate control
    
    if cmds.objExists( rotateTo ):
        
        cmds.delete( cmds.orientConstraint( rotateTo, ctrlOffset ) )
    
    # parent control
    
    if cmds.objExists( parentTo ):
        
        cmds.parent( ctrlOffset, parentTo )
    return ctr
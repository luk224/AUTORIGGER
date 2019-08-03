import maya.cmds as cmds
def chain_Oncurve (
        name = '',
        number_joints = 4,
        suffix = 'jnt',
        curva = '',
        axis = 'x',
        parentTo = '') :
            '''
            Method to create a number of joints on a curve
            example use:spine_joints=chain_Oncurve (
                                    name = 'spine',
                                    number_joints = 20,
                                    suffix = 'jnt',
                                    curva = 'spine',
                                    axis = 'x',
                                    parentTo = '')
            name (str) : name to joints
            number_joints (int) : number of joints you want created
            curva = name of curve to create onto
            
            '''
            if cmds.objExists (curva) :
                maxV_curve = cmds.getAttr (curva +'.maxValue') 
                shape_curve = cmds.listRelatives (curva, c = True, s = True) [0]
                dist_joints = maxV_curve/(number_joints - 1)
                i = 0
                chain_joints = []
                
                
                # create node to run parameter of curve
                POC = cmds.createNode ('pointOnCurveInfo', n='POC_' + curva)
                cmds.connectAttr ( shape_curve + '.worldSpace', POC + '.inputCurve' )
    
                
                for i in range (number_joints) :
                
                    
                    if i == 0 :
                        
                        cmds.select (cl = 1) 
                        cmds.setAttr (POC + '.parameter',0 )       
                        POC_jnt = 0
                        
                    else :
                        
                        POC_current = cmds.getAttr (POC + '.parameter')
                        POC_jnt = POC_current + dist_joints 
                        cmds.setAttr (POC + '.parameter',( POC_current + dist_joints ) )

                    cmds.select (cl = 1) 
                    
                    jnt = cmds.joint (name = name + str(i) +'_' + suffix )
                    
                    chain_joints.append (jnt)
                    
                    cmds.connectAttr (POC + '.position', jnt + '.translate', f = 1)    
                    cmds.disconnectAttr (POC + '.position', jnt + '.translate') 
                     
                    jnt_ant =  ( name + str(i-1) +'_' + suffix )
                    
                    if cmds.objExists (jnt_ant) :
                        cmds.parent (jnt, jnt_ant)
                        
                cmds.delete (POC)
                
                if axis =='x' :

                    cmds.joint (chain_joints[0], e= True, oj = 'xyz', secondaryAxisOrient = 'yup', ch = True)
                
                if axis =='y' :
                
                    cmds.joint (chain_joints[0], e= True, oj = 'yzx', secondaryAxisOrient = 'yup', ch = True)    
                
                if axis =='z' :
                
                    cmds.joint (chain_joints[0], e= True, oj = 'zxy', secondaryAxisOrient = 'yup', ch= True)    
                     
                if cmds.objExists (parentTo):
                    
                    cmds.parent ( chain_joints [0], parentTo )
                    
                return  chain_joints
            else :
                cmds.confirmDialog( title = 'Warnning', message = 'not exist a curve named' + curva, button = ['ok'])
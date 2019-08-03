
def chain_joint(
		ls_guias = [],
		parentTo ='',
		axis = 'x',
		side_chain = 'lf',
		pref ='',
		suffix ='jnt'
		):
        ''' Method : create chain of joints form array
        
        example use: chain_joint(
                        ls_guias = cmds.ls(sl=1),
                        parentTo ='',
                        axis = 'y',
                        side_chain = 'lf',
                        pref ='',
                        suffix ='jnt'
                        )

        ls_guias : (str) array of objects where to place the joints
        axis : (str) orientation axis of chain
        suffix : (str) suffix added to joint created
        parentTo : (str) name of object to parent chain joints created
		pref (str) : add prefix to name 
		suffix (str) : type of element
        
        return (str) : chain_joints
        '''
        chain_joints = []

        for elem in ls_guias:
            cmds.select (cl =True)
   
            name_jnt = side_chain + '_' + elem + '_' + suffix 
            
        
            if pref :
                name_jnt =  pref + '_' + side_chain + '_' + elem + '_' + suffix 

            #create joints        
            pos =cmds.xform (elem, q = 1,  ws = 1, t =1)
            
            jnt = cmds.joint (name = name_jnt , p = pos)
            
            if axis == '' :

        
                rotation = cmds.xform (elem, q = True, ws = True, ro = True)   
                 
                
                cmds.setAttr (jnt + '.jointOrientX', rotation [0])
                cmds.setAttr (jnt + '.jointOrientY', rotation [1])
                cmds.setAttr (jnt + '.jointOrientZ', rotation [2])
            

            
            chain_joints.append (jnt)
            
            if jnt == chain_joints[0] :
                if cmds.objExists (parentTo):  
                    cmds.parent (jnt,parentTo)
                parentJnt = jnt
            else:


                cmds.parent (jnt ,parentJnt)
                parentJnt = chain_joints[-1]
                            

            

        if axis =='x' :

            cmds.joint (chain_joints[0], e= True, oj = 'xyz', secondaryAxisOrient = 'yup', ch = True)
			
        
        if axis =='y' :
        
            cmds.joint (chain_joints[0], e= True, oj = 'yzx', secondaryAxisOrient = 'zup', ch = True)    
        
        if axis =='z' :
        
            cmds.joint (chain_joints[0], e= True, oj = 'zxy', secondaryAxisOrient = 'yup', ch= True)   

        
                       
                 
        # add orientation al last joint of chain created
        cmds.setAttr (chain_joints[-1] + '. jointOrientX', 0)    
        cmds.setAttr (chain_joints[-1] + '. jointOrientY', 0)        
        cmds.setAttr (chain_joints[-1] + '. jointOrientZ', 0)        
        
        return chain_joints
        
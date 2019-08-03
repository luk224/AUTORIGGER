def create_curve (
        ls_guias =[],
        degree = 2,
        **args ):
            
    	''' Method to create a curve with points given
    	example use : create_curve (
        ls_guias =cmds.ls(sl=1),
        degree = 2,
        name = 'spine'
        ) 
    	
    	ls_guias (list) : list of objects (points) to create the curve
    	degree (int): degree of curve
    	
    	return (str): name of curve created
    	''' 
        points = []           
        for elem in ls_guias :
            pos_elem = cmds.xform ( elem, q = 1, ws = 1, t = 1)
            points.append (pos_elem)
        	    
        name_curve = cmds.curve (p = points, d = degree, **args)
        return name_curve
        
       
def resetControls():
    controls = cmds.ls(sl = True, type='transform')
   
    for selCtrl in controls:

        attrReset = cmds.listAttr(selCtrl, k=True, u=True)
        for resetObj in attrReset:
            
            byDefault=cmds.attributeQuery( resetObj, node = selCtrl, listDefault = True)
            try:
                cmds.setAttr(selCtrl + "." + resetObj, byDefault[0])
            except:
                 pass
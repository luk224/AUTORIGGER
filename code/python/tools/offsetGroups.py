import maya.cmds as cmds

selection = cmds.ls(sl=1, fl=1, shapes=0)
print'\n' + str(len(selection)) + ' elements: \n' + str(selection) + '\n'

if len(selection) > 0:
    for i in range(len(selection)):
        cmds.select(cl=1)
        Tr = cmds.xform(selection[i], q=1, ws=1, t=1)
        Ro = cmds.xform(selection[i], q=1, ws=1, ro=1)
        parentt = cmds.listRelatives(selection[i], p=1)
        offsetGrp = cmds.group(em=1, n='{0}_{1}'.format(selection[i], 'offset'))

        cpc = cmds.parentConstraint(selection[i], offsetGrp, mo=0)[0]

        cmds.delete(cpc)

        if str(parentt) != 'None':
            cmds.parent(offsetGrp, parentt)

        cmds.parent(selection[i], offsetGrp)

    print '\nOffset Groups Created'
else:
    print'Select something'
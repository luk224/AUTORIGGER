import maya.cmds as cmds
sele = cmds.ls(sl=1)
print(len(sele))

def baseName(name):
    side, name, zone, type = name.split('_')
    return '{0}_{1}_{2}'.format(side,name,zone)
    
#######################
#Select Center Locator#
centerLoc = cmds.ls(sl=1, fl=1)[0]
centerPos = cmds.xform(centerLoc, q=1, ws=1, t=1)
print('Position of center ='+str(centerPos))

######################
#Select Upper Locator#
upperLoc = cmds.ls(sl =1, fl =1)[0]
upperPos = cmds.xform(upperLoc, q=1, ws=1, t=1)
print('Position of UpperLoc = ' + str(upperPos))
##############
#Select curve#
curva = cmds.ls(sl=1, fl =1)[0]
side = None
name = None
zone = None
type = None
side, name, zone, type = curva.split('_') 

cmds.select (curva + '.cv[*]')
vtxs = cmds.ls(sl =1, fl =1)
print(len(vtxs))
cmds.select(cl =1)


#Crear grupos.
locs = cmds.group (em =1,  n ='{0}_{1}_{2}_locsGrp'.format(side,name,zone))
#cmds.xform(locs,ws=True,t=centerPos)

jnts = cmds.group(em=1, n ='{0}_{1}_{2}_jntsGrp'.format(side,name,zone))
cmds.xform(jnts,ws=True,t=centerPos)

rig = cmds.group(em =1, n ='{0}_{1}_{2}_rig'.format(side,name,zone))
cmds.xform(rig,ws=True,t=centerPos)

ctls = cmds.group (em =1,  n ='{0}_{1}_{2}_ctlsGrp'.format(side,name,zone))
cmds.xform(ctls,ws=True,t=centerPos)

jointsCtrCurve = cmds.group (em =1,n= baseName(curva)+'_jntsCtlCurveGrp')
cmds.xform(ctls,ws=True,t=centerPos)

cmds.parent(locs, jnts, rig)

for i in range (len(vtxs)):
    cmds.select(cl =1)
    posCv = cmds.xform(vtxs[i], q =1, ws =1, t =1)
    jntCenter = cmds.joint(n ='{0}_{1}_{2}_{3}_aux'.format(side,name,zone,str(i)),p=(centerPos))
    jnt= cmds.joint(n='{0}_{1}_{2}_{3}_jnt'.format(side,name,zone,str(i)), p = posCv)
    #orientar
    cmds.joint(jntCenter, e=1, oj='xyz', secondaryAxisOrient = 'yup', ch= 1,zso =1)
    cmds.parent(jntCenter,jnts)
    
    loc= cmds.spaceLocator(n = '{0}_{1}_{2}_{3}_loc'.format(side,name,zone,str(i) ))[0]
    cmds.parent(loc, locs)
    ndCurInfo = cmds.createNode('pointOnCurveInfo', n = curva.replace('curve','nd'))
    
    cmds.connectAttr(curva + '.worldSpace[0]',ndCurInfo+'.inputCurve')
    cmds.setAttr(ndCurInfo +'.parameter', i)
    cmds.connectAttr(ndCurInfo+'.position', loc+'.translate')    
    
    cmds.select(loc, jntCenter)
    cnsAim = cmds.aimConstraint(offset = (0,0,0), w=1, aimVector=(1,0,0), upVector = (0,1,0), worldUpType ='objectrotation',worldUpVector = (0,1,0),worldUpObject = upperLoc)
    
    
print( 'Base curve finisshed')
print ('creating control curve...')
baseName(curva)
ctlCurve = cmds.duplicate(curva, n= baseName(curva)+'_ctlCurve', rr=1)[0]
cmds.rebuildCurve(ctlCurve, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=2, d=3, n= ctlCurve)
cmds.delete(ctlCurve, ch=1)

print 'adjust '+ctlCurve+' manually...'
cmds.wire(curva,w = ctlCurve)

#CREATE CLUSTERS to control de ctlCurve.
cmds.select (ctlCurve + '.cv[*]')
vtxs_ctl = cmds.ls(sl =1, fl =1)
print len(vtxs_ctl)

listaJointsCtrCurve = None
listaJointsCtrCurve = []
for i in range(len(vtxs_ctl)):
    cmds.select(cl=1)
    #cmds.select(ctlCurve+'.cv[{0}]'.format(i))
    posCv = cmds.xform(vtxs_ctl[i], q =1, ws =1, t =1)
    jointt =cmds.joint( n= baseName(curva)+'_'+str(i)+'_jntCtlCurve',p=(posCv))
    print jointt
    listaJointsCtrCurve.append(jointt)
    #listaClusters.append(cmds.cluster(n=baseName(curva)+'_'+str(i)+'_cluster')[1])
    cmds.parent(listaJointsCtrCurve[i], jointsCtrCurve)

#cmds.select(ctlCurve)    
#cmds.select(listaJointsCtrCurve,add=True)
ccls= cmds.skinCluster(listaJointsCtrCurve, ctlCurve, name = 'ctlCurve_skinCluster', toSelectedBones= True,bindMethod=0,normalizeWeights=1)[0]
print 'hi'
for c in listaJointsCtrCurve:
    #name= c.replace ('clusterHandle', 'ctl')
    name = c.replace('jntCtlCurve','ctl')
    print name
    ctl = createControl(nameCtrl= name,rotateTo=c,translateTo=c, scale = 1, direccion = 'z')
    cmds.pointConstraint (ctl,c)
    ctl_grp  = cmds.pickWalk(d='up')[0]
    cmds.parent(ctl_grp , ctls)
    
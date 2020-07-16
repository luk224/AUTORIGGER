import maya.cmds as cmds
#Se van a crear los huesos debajo de dos grupos:
    #Grupo SDK controlado por ParentConstraint a Jaw y Mouth
    #Grupo Attach controlado por la ribbon
#Despues de ejecutar el script habra que poner con driven key a un atributo los parent constraints y colocarlo con el GraphEditor.
#Para hacer la surface, se sacan 2 curves y se usa Loft del menu surface.

##Cargar esta funcion y CreateControl
def remap(OldMin, OldMax, NewMin,NewMax, OldValue):
	NewValue = 0
	OldRange = (OldMax - OldMin)
	if (OldRange == 0):
		NewValue = NewMin
	else:
		NewRange = (NewMax - NewMin)
		NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

	return NewValue




#################################################################
######Select Control of Jaw to add Sticky Lips Attributes#####
cn_jaw_ctl = cmds.ls(sl=1, fl =1)[0]


##############
#Select sdk_jaw_loc#
sdk_jaw_loc = cmds.ls(sl=1, fl =1)[0]


##############
#Select sdk_mouth_loc#
sdk_mouth_loc=cmds.ls(sl=1, fl =1)[0]


##############
#Select RibbonSurface#
ribbon_surface=cmds.ls(sl=1, fl =1)[0]

labioInferior =False

parentConstraintsToJaw = []
parentConstraintsToMouth = []


##############
#Select curve#
curva = cmds.ls(sl=1, fl =1)[0]

side = None
name = None
zone = None
type = None
side, name, zone, type = curva.split('_') 
#Se cogen sus vertices en vtxs
cmds.select (curva + '.cv[*]')
vtxs = cmds.ls(sl =1, fl =1)
print len(vtxs)
cmds.select(cl =1)


#Crear grupos.
jnts = cmds.group(em=1, n ='{0}_{1}_{2}_jntsGrp'.format(side,name,zone))
rig = cmds.group(em =1, n ='{0}_{1}_{2}_rig'.format(side,name,zone))
cmds.parent(jnts, rig)


for i in range (len(vtxs)):
	cmds.select(cl =1)    
	loca= cmds.spaceLocator()
	cmds.select(cl =1)
	posCv = cmds.xform(vtxs[i], q =1, ws =1, t =1) 
	jnt= cmds.joint(n='{0}_{1}_{2}_{3}_jnt'.format(side,name,zone,str(i)))
	cmds.select(cl =1)
	grupoAttach = cmds.group(em =1, n='{0}_{1}_{2}_{3}_attach'.format(side,zone,name,str(i)))
	cmds.select(cl =1)

	cmds.parent(jnt,grupoAttach)
	cmds.parent(loca,grupoAttach)


	#ES HORA DE SITUAR LOS HUESOS EN POSICIONES CONTROLABLES POR LA RIBBON:
	#Primero creo un grupo auxiliar en la posición de la curva, con el que sacar el closestPointOnSurface, que despues se borrará.
	currentAuxGrp  = cmds.group(em=1, n='thisShoulNotExists_{0}'.format(str(i)))
	cmds.xform(currentAuxGrp , ws =1 , t= posCv)  
	#Nodos en el node Editor.
	    #El DecomposeMatrix nos va a dar la posición en coordenadas globales del lugar donde tiene que ir el hueso(y por tanto su grupo _Attach y el pivot de _SDK).
	    #Nos sirve tambien para sacar las coordenadas UV con el ClosestPointOnSurface.
	currentCPOS = cmds.createNode( 'closestPointOnSurface')
	currentDM = cmds.createNode('decomposeMatrix')
	currentPOSI = cmds.createNode('pointOnSurfaceInfo')

	cmds.connectAttr(currentAuxGrp+'.worldMatrix[0]', currentDM +'.inputMatrix')
	cmds.connectAttr(currentDM+'.outputTranslate', currentCPOS +'.inPosition') 
	cmds.connectAttr(ribbon_surface+'.worldSpace[0]', currentCPOS+'.inputSurface')
	cmds.connectAttr(ribbon_surface+'.worldSpace[0]', currentPOSI+'.inputSurface')
	#Las coordenadas UV:
	cmds.connectAttr(currentCPOS+'.parameterU', currentPOSI +'.parameterU')
	cmds.connectAttr(currentCPOS+'.parameterV', currentPOSI +'.parameterV')    
	#Conectar la posicion al grupo Attach:
	cmds.connectAttr(currentPOSI+'.position', grupoAttach +'.translate')    

	#GrupoSDK con 0 0 0 en la posición del grupo Attach
	cmds.select(cl =1)  
	cmds.select(grupoAttach)  
	grupoSDK = cmds.group(n='{0}_{1}_{2}_{3}_sdk'.format(side,zone,name,str(i)))
	cmds.select(cl =1)
	cmds.parent(grupoSDK, jnts)

	cpc = cmds.parentConstraint(sdk_jaw_loc, sdk_mouth_loc, grupoSDK, mo=1)[0]
	#Primer peso es jaw, segundo es mouth, si es el labio de abajo distribuirá de la siguiente manera:
	if(labioInferior):
		parentConstraintsToJaw.append(cpc+'.'+(cmds.parentConstraint(cpc, q =True, wal=True)[0]))
		parentConstraintsToMouth.append(cpc+'.'+(cmds.parentConstraint(cpc, q =True, wal=True)[1]))
		if(len(vtxs)%2 != 0):
			#Si esta en la primera mitad y es impar:
			if(i<=(len(vtxs)/2)):
				cmds.setAttr(cpc+'.'+(cmds.parentConstraint(cpc, q =True, wal=True)[0]),remap(0.0,len(vtxs)/2, 0.0,1.0, i) )
				cmds.setAttr(cpc+'.'+(cmds.parentConstraint(cpc, q =True, wal=True)[1]),1-remap(0.0,len(vtxs)/2, 0.0,1.0, i) )
			else:
				cmds.setAttr(cpc+'.'+(cmds.parentConstraint(cpc, q =True, wal=True)[0]),1-remap(len(vtxs)/2,len(vtxs)-1, 0.0,1.0, i) )
				cmds.setAttr(cpc+'.'+(cmds.parentConstraint(cpc, q =True, wal=True)[1]),remap(len(vtxs)/2,len(vtxs)-1, 0.0,1.0, i) )


	#cmds.setAttr(cmds.parentConstraint(cpc, q =True, wal=True)[0],remap(OldMin, OldMax, NewMin,NewMax, OldValue) )


	cmds.delete(currentAuxGrp)
	cmds.delete(currentCPOS)
	cmds.select(cl=1)




#Para los driven keys:
cmds.select (cn_jaw_ctl)
#Si existen los atributos, borralos
if(cmds.attributeQuery('rightStickyLips',node=cn_jaw_ctl,exists =1 )): cmds.deleteAttr( cn_jaw_ctl, at='rightStickyLips' )
if(cmds.attributeQuery('leftStickyLips',node=cn_jaw_ctl,exists =1 )): cmds.deleteAttr( cn_jaw_ctl, at='leftStickyLips' )
cmds.addAttr( shortName='leftStickyLips', longName='LeftStickyLips',keyable=1, defaultValue=0.0, minValue=0.0, maxValue=1.0)
cmds.select(cl=1)
cmds.select(cn_jaw_ctl)
cmds.addAttr(shortName='rightStickyLips', longName='RightStickyLips',keyable=1, defaultValue=0.0, minValue=0.0, maxValue=1.0)
cmds.select(cl=1)
#Siguiente paso aqui es poner los driven keys
for i in range (len(vtxs)):
	if(i<(len(vtxs)/2)):
		cmds.setAttr(cn_jaw_ctl + '.leftStickyLips', 0)
		cmds.setDrivenKeyframe(parentConstraintsToJaw[i], currentDriver =cn_jaw_ctl + '.leftStickyLips')
		cmds.setDrivenKeyframe(parentConstraintsToMouth[i], currentDriver =cn_jaw_ctl + '.leftStickyLips')

		cmds.setAttr(cn_jaw_ctl + '.leftStickyLips', 1)
		cmds.setAttr(parentConstraintsToJaw[i],0)
		cmds.setAttr(parentConstraintsToMouth[i],1)
		cmds.setDrivenKeyframe(parentConstraintsToJaw[i], currentDriver =cn_jaw_ctl + '.leftStickyLips')
		cmds.setDrivenKeyframe(parentConstraintsToMouth[i], currentDriver =cn_jaw_ctl + '.leftStickyLips')
		cmds.setAttr(cn_jaw_ctl + '.leftStickyLips', 0)

	elif(i>(len(vtxs)/2)):
		cmds.setAttr(cn_jaw_ctl + '.rightStickyLips', 0)
		cmds.setDrivenKeyframe(parentConstraintsToJaw[i], currentDriver =cn_jaw_ctl + '.rightStickyLips')
		cmds.setDrivenKeyframe(parentConstraintsToMouth[i], currentDriver =cn_jaw_ctl + '.rightStickyLips')

		cmds.setAttr(cn_jaw_ctl + '.rightStickyLips', 1)
		cmds.setAttr(parentConstraintsToJaw[i],0)
		cmds.setAttr(parentConstraintsToMouth[i],1)
		cmds.setDrivenKeyframe(parentConstraintsToJaw[i], currentDriver =cn_jaw_ctl + '.rightStickyLips')
		cmds.setDrivenKeyframe(parentConstraintsToMouth[i], currentDriver =cn_jaw_ctl + '.rightStickyLips')
		cmds.setAttr(cn_jaw_ctl + '.rightStickyLips', 0)
		
	elif(i==(len(vtxs)/2)):
		nodoMedia = cmds.createNode( 'plusMinusAverage')
		cmds.setAttr(nodoMedia+'.operation', 3)#Operacion Average
		cmds.connectAttr(cn_jaw_ctl + '.leftStickyLips', nodoMedia+'.input1D[0]')
		cmds.connectAttr(cn_jaw_ctl + '.rightStickyLips', nodoMedia+'.input1D[1]')

		unoMenos = cmds.createNode( 'plusMinusAverage')
		cmds.setAttr(unoMenos+'.operation', 2)#Operacion minus

		cmds.connectAttr(nodoMedia+'.output1D', parentConstraintsToMouth[i])
		cmds.connectAttr(nodoMedia+'.output1D', unoMenos+'.input1D[1]')
		cmds.setAttr(unoMenos+'.input1D[0]', 1)#Operacion minus
		cmds.connectAttr(unoMenos+'.output1D',parentConstraintsToJaw[i] )








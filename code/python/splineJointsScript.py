import maya.cmds as cmds
import operator
class splineJoints:
    def __init__(self, side="cn", name="tentacle",zone="A"):
        self.side=side
        self.name=name
        self.zone=zone


    def defineCurve(self):
        self.curva = cmds.ls(sl=1, fl=1)[0]
        cmds.select(cl=1)
        #Vertex of the curve:
        cmds.select(self.curva + '.cv[*]')
        self.vtxs = cmds.ls(sl=1, fl=1)
        cmds.select(cl=1)
        print("curve loaded is {} and it has {} vertex".format(self.curva, len(self.vtxs)))

    def defineCtlObj(self):
        self.ctlObject = cmds.ls(sl=1, fl=1, sn=1)[0]
        cmds.select(cl=1)
        print("Control Object loaded is {}".format(self.ctlObject))


    #Return 1. List of joints, 2. List of Groups
    def createJoints(self,suffix='suffix', createUpAxis=False):
        JointsGrps =[]
        Joints = []
        upVectors = []
        upAxixGrp=''
        if(createUpAxis):
            cmds.select(cl=1)
            upAxixGrp = cmds.group(em=1,n='upAxisGroup')

        posX  = None
        posZ  = None
        posCv = None
        posY  = None
        jnt =None
        for i in range(len(self.vtxs)+1):
            cmds.select(cl=1)


            if(i<len(self.vtxs)):

                posCv = cmds.xform(self.vtxs[i], q =1, ws =1, t =1)
                posX=posCv[0]
                posY=posCv[1]
                posZ=posCv[2]
                jnt = cmds.joint(n='{0}_{1}_{2}_{3}_{4}'.format(self.side, self.name, self.zone, str(i), suffix),
                                 p=posCv, a=1)
            else:
                posBeforeLastCv = cmds.xform(self.vtxs[i-2], q=1, ws=1, t=1)
                posLastCv = cmds.xform(self.vtxs[i - 1], q=1, ws=1, t=1)
                r = map(operator.sub, posLastCv, posBeforeLastCv)
                l = map(operator.add,posLastCv, r)
                posCv = l
                posX = posCv[0]
                posY = posCv[1]
                posZ = posCv[2]
                jnt = cmds.joint(n='{0}_{1}_{2}_{3}_{4}_end'.format(self.side, self.name, self.zone, str(i), suffix),
                                 p=posCv, a=1)
            if(createUpAxis):
                cmds.select(cl=1)
                loc = cmds.spaceLocator()
                loc=cmds.rename(loc, '{0}_{1}_{2}_{3}_{4}_upAxis'.format(self.side,self.name,self.zone,str(i),suffix))
                cmds.xform(loc,ws=1, t=(posX,posY+5, posZ))
                upVectors.append(loc)

            Joints.append(jnt)
            cmds.select(cl =1)
            cmds.select(jnt)




        for i in range(len(Joints)):

            cmds.select(cl=1)
            nGroup= cmds.group(em =1, n='{0}_{1}_{2}_{3}_{4}Grp'.format(self.side,self.name,self.zone,str(i),suffix))
            cpc = cmds.parentConstraint(Joints[i], nGroup, mo=0)[0]
            cmds.select(cl =1)
            JointsGrps.append(nGroup)
            cmds.delete(cpc)
            if(i>0):
                cmds.parent(nGroup,Joints[i-1])
            cmds.parent(Joints[i],nGroup)
            if(createUpAxis):
                cmds.parent(upVectors[i],upAxixGrp)
            cmds.select(cl=1)
            cmds.select(Joints[0])
            cmds.joint(e=1, oj='xyz', secondaryAxisOrient = 'yup', ch=1, zso=1)

        if(createUpAxis):
            return Joints, JointsGrps,upVectors
        else:
            return Joints,JointsGrps


    def  createJointChain(self,suffix='suffix'):
        #Only create a joint chain in curve vtx positions.
        Joints = []
        posX = None
        posZ = None
        posCv = None
        posY = None
        jnt = None
        for i in range(len(self.vtxs)):
            cmds.select(cl=1)
            posCv = cmds.xform(self.vtxs[i], q=1, ws=1, t=1)
            posX = posCv[0]
            posY = posCv[1]
            posZ = posCv[2]
            jnt = cmds.joint(n='{0}_{1}_{2}_{3}_{4}'.format(self.side, self.name, self.zone, str(i), suffix),
                             p=posCv, a=1)
            Joints.append(jnt)
        for i in range(len(Joints)):

            cmds.select(cl=1)
            if (i > 0):
                cmds.parent(Joints[i], Joints[i - 1])
        return Joints



    def createControls(self,suffix,thingsToControl,parentUpVectors=False,upVectors=''):
        offsetGrps =[]
        controls = []
        inputTransformGrps=[]
        lastControl =''
        for i in range(len(thingsToControl)):
            cmds.select(cl=1)
            nControl= cmds.circle(nr=(1,0,0),n='{0}_{1}_{2}_{3}_{4}'.format(self.side,self.name,self.zone,str(i),suffix))[0]
            nGroup= cmds.group( n='{0}_{1}_{2}_{3}_offset'.format(self.side,self.name,self.zone,str(i)))
            cpc= cmds.parentConstraint(thingsToControl[i],nGroup)
            cmds.delete(cpc)
            cmds.select(cl=1)

            iGrp =cmds.group(em=1, n='{0}_{1}_{2}_{3}_inputGrp'.format(self.side,self.name,self.zone,str(i)))



            cpc= cmds.parentConstraint(nGroup,iGrp)
            cmds.delete(cpc)



            cmds.parent(iGrp,nGroup)
            cmds.parent(nControl,iGrp)
            cpc=cmds.parentConstraint(nControl, thingsToControl[i])

            if cmds.objExists(lastControl):

                cmds.parent(nGroup,lastControl)
                cmds.parent(upVectors[i],lastControl)



            offsetGrps.append(nGroup)
            inputTransformGrps.append(iGrp)
            lastControl=nControl
            controls.append(nControl)

        return controls,inputTransformGrps,offsetGrps

    def createNormaLControls(self,suffix,thingsToControl):
        offsetGrps =[]
        controls = []
        inputTransformGrps=[]
        lastControl =''
        for i in range(len(thingsToControl)):
            cmds.select(cl=1)
            nControl= cmds.circle(nr=(1,0,0),n='{0}_{1}_{2}_{3}_{4}'.format(self.side,self.name,self.zone,str(i),suffix))[0]
            nGroup= cmds.group( n='{0}_{1}_{2}_{3}_offset'.format(self.side,self.name,self.zone,str(i)))
            cpc= cmds.parentConstraint(thingsToControl[i],nGroup)
            cmds.delete(cpc)
            cmds.select(cl=1)


            cpc=cmds.parentConstraint(nControl, thingsToControl[i])


            if cmds.objExists(lastControl):
                cmds.parent(nGroup,lastControl)

            offsetGrps.append(nGroup)
            lastControl=nControl
            controls.append(nControl)

        return controls,offsetGrps
    def connectMasterControl(self,ctlObject,thingsToControl):
        #Create direct connections with a multiplier from the ctlObject to the list of things to Control.

        translateMultNode = cmds.createNode('multiplyDivide')
        rotateMultNode = cmds.createNode('multiplyDivide')

        if(cmds.attributeQuery('trans_multiplier',node=ctlObject,exists =1 )): cmds.deleteAttr( ctlObject, at='trans_multiplier' )
        if(cmds.attributeQuery('rot_multiplier',node=ctlObject,exists =1 )): cmds.deleteAttr( ctlObject, at='rot_multiplier' )
        cmds.select(cl=1)
        cmds.select(ctlObject)
        cmds.addAttr( shortName='trans_multiplier', longName='trans_multiplier',keyable=1, defaultValue=1.0, minValue=0.001, maxValue=999.0)
        cmds.select(cl=1)
        cmds.select(ctlObject)
        cmds.addAttr( shortName='rot_multiplier', longName='rot_multiplier',keyable=1, defaultValue=1.0, minValue=0.001, maxValue=999.0)

        cmds.connectAttr(ctlObject+'.translate',translateMultNode+'.input1')
        cmds.connectAttr(ctlObject+'.trans_multiplier',translateMultNode+'.input2.input2X')
        cmds.connectAttr(ctlObject+'.trans_multiplier',translateMultNode+'.input2.input2Y')
        cmds.connectAttr(ctlObject+'.trans_multiplier',translateMultNode+'.input2.input2Z')

        cmds.connectAttr(ctlObject+'.rotate',rotateMultNode+'.input1')
        cmds.connectAttr(ctlObject+'.rot_multiplier',rotateMultNode+'.input2.input2X')
        cmds.connectAttr(ctlObject+'.rot_multiplier',rotateMultNode+'.input2.input2Y')
        cmds.connectAttr(ctlObject+'.rot_multiplier',rotateMultNode+'.input2.input2Z')

        for i in range(len(thingsToControl)):
            if(i>0):
                cmds.connectAttr(translateMultNode+'.output',thingsToControl[i]+'.translate')
            cmds.connectAttr(rotateMultNode+'.output',thingsToControl[i]+'.rotate')


    def createPosOriBindChains(self):
        self.posJoints, self.posJointsGroup, self.UpAxisList = self.createJoints(suffix='pos', createUpAxis=True)
        self.oriJoints, self.oriJointsGroup = self.createJoints(suffix='ori')
        self.bindJoints, self.bindJointsGroup = self.createJoints(suffix='jnt')

        self.pointAndParentConstraints()

        self.controls, self.inputTransformCtls, self.ctlsOffsetGrps  = self.createControls(suffix='ctl', thingsToControl=self.posJoints, parentUpVectors=True, upVectors=self.UpAxisList)

        self.connectMasterControl(self.ctlObject,self.inputTransformCtls)
    def pointAndParentConstraints(self):
        for i in range(len(self.posJoints)):
            cmds.pointConstraint(self.posJoints[i], self.oriJointsGroup[i], mo=0)
            cmds.parentConstraint(self.oriJoints[i], self.bindJointsGroup[i], mo=1)

    def AimConstraints(self):
        for i in range(len(self.oriJoints) - 1):
            cmds.select(cl=1)
            cmds.select(self.oriJoints[i])
            print('aim Constraint from ' + self.oriJoints[i] + ' to ' + self.oriJoints[i + 1])
            cmds.select(self.oriJoints[i + 1], add=1)

            cmds.aimConstraint(offset=(0, 0, 0), weight=1, aimVector=(-1, 0, 0), upVector=(0, 1, 0),
                               worldUpType='object', worldUpObject=self.UpAxisList[i])

   





# for i in range(len(posJoints)):

#     cmds.select(posJoints[i], add=1)
    


# print(posJointsGroup) 
side = 'lf'
ikfk = cmds.getAttr ('switch_Arm.fk_ik')
Fk_controls = [side  + '_shoulderFk_ctl',side  + '_elbowFk_ctl', side  + '_wristFk_ctl']
Ik_controls = [side  + '_wristIk_ctl',side  + '_poleArm_ctl']
joints = [side + '_shoulder_jnt', side + '_elbow_jnt' ]

if ikfk == 1 :
    sx,sy,sz = cmds.xform(joints[0], q=1, ws=1, s =1)
    cmds.xform(Fk_controls[0], ws=1, s=(sx, sy, sz))
    
    sx,sy,sz = cmds.xform(joints[1], q=1, ws=1, s =1)
    cmds.xform(Fk_controls[1], ws=1, s=(sx, sy, sz))    
       
    for ctl in Fk_controls:
    
        rx, ry, rz = cmds.xform(ctl + '_switch', q=1, ws=1, ro=1)
        cmds.xform(ctl, ws=1, ro=(rx, ry, rz))


    cmds.setAttr("switch_Arm.fk_ik", 0)
else:
 
    tx, ty, tz = cmds.xform(Ik_controls [0] + '_switch', q=1, ws=1, t=1)
    cmds.xform(Ik_controls [0], ws=1, t=(tx, ty, tz))
    
    rx, ry, rz = cmds.xform(Ik_controls [0] + '_switch', q=1, ws=1, ro=1)
    cmds.xform(Ik_controls [0], ws=1, ro=(rx, ry, rz))
    
    tx, ty, tz = cmds.xform(Ik_controls [1] + '_switch', q=1, ws=1, t=1)
    cmds.xform(Ik_controls [1], ws=1, t=(tx, ty, tz))
    
    cmds.setAttr("switch_Arm.fk_ik", 1)

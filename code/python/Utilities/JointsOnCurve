import maya.cmds as mc
import re

# recuperation des curves et du nombre de joints voulut
sel = mc.ls(sl=True)
if sel == []:
    mc.confirmDialog(title='No selection', message='you must select curve(s)', button=['OK'], defaultButton='OK')
else:
    chaine = ""
    expression = r"^[0-9]+$"
    while re.search(expression, chaine) is None:
        prompt = mc.promptDialog(
            title="Joint On Curve",
            message="number of bones",
            button=['OK', 'Cancel'],
            defaultButton="OK",
            dismissString='Cancel')
        if prompt == "OK":
            chaine = mc.promptDialog(query=True, text=True)
        elif prompt == "Cancel":
            chaine = "0"
    if chaine == "0":
        print("Cancelado")
    else:
        chaine = int(chaine)

for elt in sel:
    mc.duplicate(elt, n=elt + "NewCurveTemp")
    mc.rebuildCurve(elt + "NewCurveTemp", ch=False, rpo=True, rt=False, end=True, kr=False, kcp=False, kep=True,
                    kt=True, s=chaine, d=3, tol=0.01)
    mc.rebuildCurve(elt + "NewCurveTemp", ch=True, rpo=True, rt=False, end=True, kr=False, kcp=False, kep=True,
                    kt=False, s=0, d=3, tol=0.01)
    ep = chaine + 1
    i = 0
    SK = []
    CL = []
    while ep > 0:
        mc.select(elt + "NewCurveTemp.ep[" + str(i) + "]")
        mc.cluster(name="CL_Temp_" + str(i))
        CL.append("CL_Temp_" + str(i) + "Handle")
        pos = mc.xform("CL_Temp_" + str(i) + "Handle", query=True, rp=True, ws=True)
        mc.select(clear=True)
        mc.joint(p=(pos[0], pos[1], pos[2]), name="SK_joc_" + elt + "_" + str(i))
        SK.append("SK_joc_" + elt + "_" + str(i))
        ep -= 1
        i += 1
    i -= 1
    while "SK_joc_" + elt + "_" + str(i) != "SK_joc_" + elt + "_0":
        mc.parent("SK_joc_" + elt + "_" + str(i), "SK_joc_" + elt + "_" + str(i - 1))
        i -= 1
    mc.joint("SK_joc_" + elt + "_0", e=True, oj="xyz", secondaryAxisOrient="yup", ch=True, zso=True)
    mc.delete(CL)
    mc.delete(elt + "NewCurveTemp")
mc.select(clear=True)

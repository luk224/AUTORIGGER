import json
import maya.cmds as cmds

def copySelection():
    selection = cmds.ls(sl=1)
    jObject= json.dumps(selection)

    print('Copy this:')
    print("'"+jObject+"'")



def pasteSelection(string):
    saved= json.loads(string)
    cmds.select(saved)


copySelection()

string = "paste here"

pasteSelection(string)

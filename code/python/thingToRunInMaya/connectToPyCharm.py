import ptvsd
ptvsd.enable_attach(secret="my_secret",address=('0.0.0.0',3000))

import maya.cmds as cmds

if not cmds.commandPort(':4434', query=True):
    cmds.commandPort(name=':4434')
    print("port opened")

import pymel.core as pm

def normCrv():
    
    # Get the selected curve and create a duplicate.
    crv = pm.selected()[0].getShape()
    dupCrv = pm.duplicate(crv)[0]
    pm.rename(dupCrv, str(crv) + "_normal")
    
    # Get number of CVs on this curve
    cvs = crv.numCVs()
    
    # Iterate over every CV
    for cv in range(0, cvs):
        # Get CV position
        pos = crv.cv[cv].getPosition(space = "object")
        # The position we got is of a Pymel.dt.Vector type so ve can use all its methods like normalize
        pos.normalize() # This normalizes the position vector and by doing that we make its distance from the pivot be 1
        # This new Vectors magnitude (length) is equal to 1 but it needs to be moved to our curves pivot point
        # We do that by adding it to the pivot position
        objectSpacePos = dupCrv.getTranslation(space = "world") + pos
        # And finally we apply this calculated position to out vertex
        pm.move(objectSpacePos[0], objectSpacePos[1], objectSpacePos[2], dupCrv.cv[cv])
        
if __name__ == "__main__":
    normCrv()
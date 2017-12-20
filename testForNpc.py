### Test for existing NPCs on the actively selected object

import maya.cmds as cmds
import maya.api.OpenMaya as om2

###------------------------------------------------------###

# Get the active selection as an MFnDependencyNode
# i:[]
# o:[MFnDependencyNode]
def getActiveSel():
    # Get selection
    sel = om2.MGlobal.getActiveSelectionList()
    
    # Create an empty MObject
    activeSelMob = None
    
    # Check for an existing selection. If there is, set activeSelMob equal to the existing selection.
    if sel.length():
        selActive = ((sel.length()) - 1)
        activeSelMob = sel.getDependNode(selActive)
        activeSelDep = om2.MFnDependencyNode(activeSelMob)
        return(activeSelDep)
    else:
        print('No active selection')
        return None


# Get the source node of the given attribute. 
# To check if the source is a certain type of node, set testName as the desired type of node.
# To check if the source's name matches another, set testName as the desired node name, and set nodeName to True.
# *If the attr is an array, the desired index must be defined.
# i:[MFnDependencyNode, string, string, *int, *bool]
# o:[(bool, MFnDependencyNode)]
def checkSrcNode(input, attr, testName, index = None, nodeName = None):
    # Get the MPlug of the given attribute.
    plug = om2.MPlug(input.findPlug(attr, False))
    # If index was given, use to find source. Otherwise find source as usual.
    if index != None:
        sourcePlug = plug.elementByLogicalIndex(index).source()
    else:
        sourcePlug = plug.source()
    sourceMob = sourcePlug.node()
    sourceDep = om2.MFnDependencyNode(sourceMob)
    
    if nodeName == True:
        if sourceDep.name() == testName:
            return (True, sourceDep)
        else:
            return (False, sourceDep)
    
    if sourceDep.typeName == testName:
        return (True, sourceDep)
    else:
        return (False, sourceDep)


# Tests the active selection for an existing NPC
# i:[]
# o:[None OR list[(string, string)]]
def test4npc():
    # Get the active selection as an MFnDependencyNode
    sel = getActiveSel()
    
    # Check that the active selection exists
    if sel == None:
        return None
    
    # Check that the active selection is a transform node
    if sel.typeName != 'transform':
        print('The active selection is not a transform node.')
        return None
    
    # Create an empty list to return
    existingNpcArray = []
    
    # 
    for attr in ('translate', 'tx', 'ty', 'tz', 'rotate', 'rx', 'ry', 'rz', 'scale', 'sx', 'sy', 'sz'):
        # Check the source of the active selection's given attribute for a decomposeMatrix node
        selSource = checkSrcNode(sel, attr, 'decomposeMatrix')
        if selSource[0] == True:
            # Check the source of the decomposeMatrix node's inputMatrix for a multMatrix node
            decompSource = checkSrcNode(selSource[1], 'inputMatrix', 'multMatrix')
            if decompSource[0] == True:
                # Check that the source of the multMatrix node's matrixIn is the active selection
                multSource = checkSrcNode(decompSource[1], 'matrixIn', sel.name(), index = 2, nodeName = True)
                if multSource[0] == True:
                    parent = checkSrcNode(decompSource[1], 'matrixIn', sel.name(), index = 1, nodeName = True)
                    existingNpcArray.append((attr, parent[1].name()))
    
    if len(existingNpcArray) == 0:
        print('There are no NPC connections driving this transform node.')
    else:
        for connection in existingNpcArray:
            print("This transform node's {} attribute is driven by {}".format(connection[0], connection[1]))
    
    return existingNpcArray

### Test for an existing NPC

import maya.cmds as cmds
import maya.api.OpenMaya as om2

###------------------------------------------------------###

# Gets the source of an MFnDep's attribute. If the inputAttr is an array, the desired index must be defined.
# i:[MFnDependencyNode, string, *int]
# o:[MFnDependencyNode]
def destination2Source(destDep, inputAttr, index = None):
    plug = om2.MPlug(destDep.findPlug(inputAttr, False))
    # If index was given, use to find source. Otherwise find source as usual.
    if index != None:
        sourcePlug = plug.elementByPhysicalIndex(index).source()
    else:
        sourcePlug = plug.source()
    sourceMob = sourcePlug.node()
    sourceDep = om2.MFnDependencyNode(sourceMob)
    return sourceDep

# Checks if the objects are connected by an NPC for the given attribute.
# i:[MFnDependencyNode, MFnDependencyNode, string]
# o:[string]
def test4npc(parent, child, inputAttr):
    # Get the MPlug of the given child's attribute, and set its source node to an MFnDependencyNode.
    childSourceDep = destination2Source(child, inputAttr)
    
    # Continue if the source is a decomposeMatrix node.
    if childSourceDep.typeName == 'decomposeMatrix':
        decompSourceDep = destination2Source(childSourceDep, 'inputMatrix')
        
        # Continue if the source is a multMatrix node.
        if decompSourceDep.typeName == 'multMatrix':
            
            # Continue if the source is the same as the parent.
            if destination2Source(decompSourceDep, 'matrixIn', 1).name() == parent.name():
                return inputAttr
    else:
        return

###------------------------------------------------------###

# Get selection
sel = om2.MGlobal.getActiveSelectionList()

# Create empty MObjects
parentMob = None
childMob = None

# Check that exactly two objects are selected. If there are, set them equal to the empty MObjects.
if sel.length() == 2:
    parentMob = sel.getDependNode(0)
    childMob = sel.getDependNode(1)

else:
    print('Invalid Selection')

# If the MObjects have been populated by the previous if statement, test for an existing NPC connection.
if (parentMob is not None and childMob is not None):
    # Create MFnDependencyNode objects from the selected MObjects
    parentDep = om2.MFnDependencyNode(parentMob)
    childDep = om2.MFnDependencyNode(childMob)
    
    # Create an empty array for existing NPC connections
    existingNpcArray = []
    
    # Test for any NPC connections
    for attr in ('translate', 'tx', 'ty', 'tz', 'rotate', 'rx', 'ry', 'rz', 'scale', 'sx', 'sy', 'sz'):
        existingConnection = test4npc(parentDep, childDep, attr)
        if existingConnection != None:
            existingNpcArray.append(existingConnection)
    
    # If an NPC does exist, print what attributes are connected. Otherwise print that none exists.
    if len(existingNpcArray) > 0:
        print('NPC exists for the following attributes: {}'.format(existingNpcArray))
    else:
        print('No NPC exists.')

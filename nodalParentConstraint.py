### Nodal Parent Constraint Tool.

import maya.cmds as cmds
import maya.api.OpenMaya as om2

###------------------------------------------------------###

# Creates the Nodal Parent Constraint User Interface (Window, buttons, etc.)
# i:[]
# o:[]
def npcUI():
    # Check to see if the window already exists
    if cmds.window('npcUI', exists = True):
        cmds.deleteUI('npcUI')
    
    # Create the window
    npcWindow = cmds.window('npcUI', title = 'Nodal Parent Constraint', w = 360, h = 300, mxb = False)
    
    # Create the main layout
    mainLayout = cmds.columnLayout('mainLayout', w = 360, h = 50)
    cmds.separator(h = 10)
    
    ###------------------###
    
    # Create moRow layout
    moRow = cmds.rowLayout('moRow', nc = 2, cw = [(1, 183), (2, 177)])
    
    # Create maintain offset label and checkbox
    cmds.text(l = 'Maintain offset:', w = 172, al = 'right', p = moRow)
    maintainOffset = cmds.checkBox('maintainOffset', l = '', p = moRow, v = True)
    
    ###------------------###
    
    # Create overrideExisting layout
    oeRow = cmds.rowLayout('overrideExisting', nc = 2, cw = [(1, 183), (2, 177)], p = mainLayout)
    
    # Create Override Existing Connections label and checkbox
    cmds.text(l = 'Override existing connections:', w = 172, al = 'right', p = oeRow)
    overrideExisting = cmds.checkBox('overrideExisting', l = '', p = oeRow, v = False)
    
    ###------------------###
    
    # Create constraint axes frame
    cmds.separator(h = 10, p = mainLayout)
    cmds.frameLayout('constraintAxes', l = 'Constraint axes:', w = 358, h = 20, p = mainLayout)
    cmds.separator(h = 3, p = mainLayout)
    
    ###------------------###
    
    # Create tRowAll layout
    tRowAll = cmds.rowLayout('tRowAll', nc = 2, cw = [(1, 100), (2, 260)], p = mainLayout)
    
    # Create translate label and All checkbox
    cmds.text(l = 'Translate:', w = 90, al = 'right', p = tRowAll)
    tAll = cmds.checkBox('tAll', l = 'All', p = tRowAll, v = True, onc = 'cmds.checkBoxGrp("tXYZ", e = True, va3 = [False, False, False])')
        
    
    # Create tRow layout
    tRow = cmds.rowLayout('tRow', nc = 4, cw = [(1, 100), (2, 80), (3, 80), (4, 80)], p = mainLayout)
    
    # Create checkboxes for translate axes
    cmds.text(l = '', p = tRow)
    tXYZ = cmds.checkBoxGrp('tXYZ', la3 = ['X', 'Y', 'Z'], ncb = 3, cw3 = [80, 80, 80], onc = 'cmds.checkBox("tAll", e = True, v = False)')
    
    ###------------------###
    
    # Create rRowAll layout
    rRowAll = cmds.rowLayout('rRowAll', nc = 2, cw = [(1, 100), (2, 240)], p = mainLayout)
    
    # Create rotate label and All checkbox
    cmds.text(l = 'Rotate:', w = 90, al = 'right', p = rRowAll)
    rAll = cmds.checkBox('rAll', l = 'All', p = rRowAll, v = True, onc = 'cmds.checkBoxGrp("rXYZ", e = True, va3 = [False, False, False])')
    
    
    # Create rRow layout
    rRow = cmds.rowLayout('rRow', nc = 4, cw = [(1, 100), (2, 80), (3, 80), (4, 80)], p = mainLayout)
    
    # Create checkboxes for rotate axes
    cmds.text(l = '', p = rRow)
    rXYZ = cmds.checkBoxGrp('rXYZ', la3 = ['X', 'Y', 'Z'], ncb = 3, cw3 = [80, 80, 80], onc = 'cmds.checkBox("rAll", e = True, v = False)')
    
    ###------------------###
    
    # Create sRowAll layout
    sRowAll = cmds.rowLayout('sRowAll', nc = 2, cw = [(1, 100), (2, 240)], p = mainLayout)
    
    # Create scale label and All checkbox
    cmds.text(l = 'Scale:', w = 90, al = 'right', p = sRowAll)
    sAll = cmds.checkBox('sAll', l = 'All', p = sRowAll, v = True, onc = 'cmds.checkBoxGrp("sXYZ", e = True, va3 = [False, False, False])')
    
    
    # Create sRow layout
    sRow = cmds.rowLayout('sRow', nc = 4, cw = [(1, 100), (2, 80), (3, 80), (4, 80)], p = mainLayout)
    
    # Create checkboxes for scale axes
    cmds.text(l = '', p = sRow)
    sXYZ = cmds.checkBoxGrp('sXYZ', la3 = ['X', 'Y', 'Z'], ncb = 3, cw3 = [80, 80, 80], onc = 'cmds.checkBox("sAll", e = True, v = False)')
    
    ###------------------###
    
    # Create constrain button
    cmds.separator(h = 15, p = mainLayout)
    constrain = cmds.button('constrain', l = 'Constrain', p = mainLayout, h = 27, w = 360, c = 'getUIValues()')
    
    ###------------------###
    
    # Show the window
    cmds.showWindow('npcUI')


# Creates variables from all of the npcUI values, then runs the createNpc function with them.
# i:[]
# o:[]
def getUIValues():
    mo = cmds.checkBox("maintainOffset", q = True, v = True)
    override = cmds.checkBox("overrideExisting", q = True, v = True)
    tAll = cmds.checkBox("tAll", q = True, v = True)
    tXYZ = cmds.checkBoxGrp("tXYZ", q = True, va3 = True)
    rAll = cmds.checkBox("rAll", q = True, v = True)
    rXYZ = cmds.checkBoxGrp("rXYZ", q = True, va3 = True)
    sAll = cmds.checkBox("sAll", q = True, v = True)
    sXYZ = cmds.checkBoxGrp("sXYZ", q = True, va3 = True)
    
    createNpc(mo, override, tAll, tXYZ, rAll, rXYZ, sAll, sXYZ)


# Gets the MDagPath of the given string
# i:[string]
# o:[MDagPath]
def getDagPath(node=None):
    sel = om2.MSelectionList()
    sel.add(node)
    d = sel.getDagPath(0)
    return d


# Gets the local offset between two given transform nodes based on their names.
# i:[string, string]
# o:[matrix]
def getLocalOffset(parent, child):
    parentWorldMatrix = getDagPath(parent).inclusiveMatrix()
    childWorldMatrix = getDagPath(child).inclusiveMatrix()
    
    return childWorldMatrix * parentWorldMatrix.inverse()


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


# Get the source node of the given attribute and check if it matches the given name or node type.
# To check if the source is a certain type of node, set testName as the desired type of node.
# To check if the source's name matches another, set testName as the desired node name, and set nodeName to True.
# To check if the source exists, set exists to True. False will be returned if there is no source node, True will be returned if there is a source node.
    # *When checking if there is a source node, an input is required for testName, but will have no effect on the output.
# *If the attr is an array, the desired index must be defined.
# i:[MFnDependencyNode, string, string, *int, *bool, *bool]
# o:[(bool, MFnDependencyNode)]
def checkSrcNode(input, attr, testName, index = None, nodeName = False, exists = None):
    # Get the MPlug of the given attribute.
    plug = om2.MPlug(input.findPlug(attr, False))
    # If index was given, use to find source. Otherwise find source as usual.
    if index != None:
        sourcePlug = plug.elementByLogicalIndex(index).source()
    else:
        sourcePlug = plug.source()
    sourceMob = sourcePlug.node()
    sourceDep = om2.MFnDependencyNode(sourceMob)
    
    if exists == True:
        if sourceDep.name() == 'NULL':
            return(False, sourceDep)
        else:
            return(True, sourceDep)
    
    if nodeName == True:
        if sourceDep.name() == testName:
            return(True, sourceDep)
        else:
            return(False, sourceDep)
    
    if sourceDep.typeName == testName:
        return(True, sourceDep)
    else:
        return(False, sourceDep)


# Tests the active selection for an existing NPC
# i:[]
# o:[list[(boolean, string)]]
def test4npc():
    # Get the active selection as an MFnDependencyNode
    sel = getActiveSel()
    
    # Create an empty list to return
    existingNpcArray = []
    
    # Check to see if the source of each transform is from an NPC connection. Yes: Append (True, attr) to the list. No: Append (False, attr) to the list.
    for attr in ('t', 'tx', 'ty', 'tz', 'r', 'rx', 'ry', 'rz', 's', 'sx', 'sy', 'sz'):
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
                    existingNpcArray.append((True, attr))
                
                else:
                    existingNpcArray.append((False, attr))
            
            else:
                existingNpcArray.append((False, attr))
        
        else:
            existingNpcArray.append((False, attr))
    
    return existingNpcArray


# Tests the active selection for an existing NPC Blend
# i:[]
# o:[list[(boolean, string, int)]]
def test4npcBlend():
    
    # Get the active selection as an MFnDependencyNode
    sel = getActiveSel()
    
    # Create an empty list to return
    existingNpcBlendArray = []
    
    # Checks the source node of each Matrix In attribute for a wtAddMatrix node
    def checkWtSrc(input, testName, index):
        # Get the MPlug of the given attribute.
        plugArray = om2.MPlug(input.findPlug('wtMatrix', False))
        plugParent = plugArray.elementByLogicalIndex(index)
        plug = plugParent.child(0)
        
        # Get the MFnDependencyNode of the plug
        sourcePlug = plug.source()
        sourceMob = sourcePlug.node()
        sourceDep = om2.MFnDependencyNode(sourceMob)
        
        # Check that the source node's type matches the given testName.
        if sourceDep.typeName == testName:
            return(True, sourceDep)
        else:
            return(False, sourceDep)
    
    # Counts a wtAddMatrix node's incoming Matrix In connections
    def countDrivers(driverCount):
        
        if (checkWtSrc(decompSource[1], 'multMatrix', index = driverCount))[0] == False:
            return(driverCount)
        
        else:
            return(countDrivers(driverCount + 1))
    
    # Check to see if the source of each transform is from an NPC Blend connection. Yes: Append (True, attr, # of drivers) to the list. No: Append (False, attr, # of drivers) to the list.
    for attr in ('t', 'tx', 'ty', 'tz', 'r', 'rx', 'ry', 'rz', 's', 'sx', 'sy', 'sz'):
        
        drivers = 0
        
        # Check the source of the active selection's given attribute for a decomposeMatrix node
        selSource = checkSrcNode(sel, attr, 'decomposeMatrix')
        
        if selSource[0] == True:
            decompSource = checkSrcNode(selSource[1], 'inputMatrix', 'wtAddMatrix')
            
            if decompSource[0] == True:
                drivers = countDrivers(0)
                print(type(drivers))
                if drivers == 0:
                    existingNpcBlendArray.append((False, attr, drivers))
                
                else:
                    existingNpcBlendArray.append((True, attr, drivers))
            
            else:
                existingNpcBlendArray.append((False, attr, drivers))
        
        else:
            existingNpcBlendArray.append((False, attr, drivers))
    
    print(existingNpcBlendArray)
    return existingNpcBlendArray


# Tests the active selection for incoming connections
# i:[]
# o:[list[(boolean, string)]]
def test4connection():
    # Get the active selection as an MFnDependencyNode
    sel = getActiveSel()
    
    # Create an empty list to return
    existingConnectionArray = []
    
    # Check to see if the source of each transform exists. Yes: Append (True, attr) to the list. No: Append (False, attr) to the list.
    for attr in ('t', 'tx', 'ty', 'tz', 'r', 'rx', 'ry', 'rz', 's', 'sx', 'sy', 'sz'):
        # Check if a source node exists for the given attribute of the active selection
        selSource = checkSrcNode(sel, attr, '', exists = True)
        
        if selSource[0] == True:
            existingConnectionArray.append((True, attr))
        
        else:
            existingConnectionArray.append((False, attr))
    
    return existingConnectionArray


# Creates a parent constraint between two selected transform nodes.
# i:[bool, bool, bool, [bool, bool, bool], bool, [bool, bool, bool], bool, [bool, bool, bool], *args]
# o:[]
def createNpc(mo, override, tAll, tXYZ, rAll, rXYZ, sAll, sXYZ, *args):
    # Get the selected nodes
    sel = cmds.ls(sl = True)
    
    # Check that exactly two nodes are selected
    if len(sel) <= 1:
        print('Must select two or more nodes')
        return
    
    # Check that the nodes selected are transform nodes
    for i in sel:
        if cmds.nodeType(i) != 'transform':
            if cmds.nodeType(i) != 'joint':
                print('Must select two transform or joint nodes.')
                return
    
    # Make a list of the translate / rotate / scale checkBox booleans
    trsBools = []
    for i in ((tAll, tXYZ), (rAll, rXYZ), (sAll, sXYZ)):
        trsBools.append(i[0])
        for xyz in i[1]:
            trsBools.append(xyz)
    
    # If override = False, check for existing connections that overlap with selected transforms.
    if override == False:
        transformBool = False
        for iAttr, existingConnection in zip(trsBools, test4connection()):
            if len(existingConnection[1]) == 1:
                if iAttr == True:
                    transformBool = True
                elif existingConnection[0] == True:
                    transformBool = True
                else:
                    transformBool = False
                if iAttr == True and iAttr == existingConnection[0]:
                    print('The .{} attribute is already being driven by another connection'.format(existingConnection[1]))
                    return
                else:
                    continue
            
            if iAttr == True and iAttr == existingConnection[0]:
                print('The .{} attribute is already being driven by another connection'.format(existingConnection[1]))
                return
            
            if transformBool == True and transformBool == iAttr:
                print('The .{} attribute is already being driven by another connection'.format(existingConnection[1]))
                return
            
            if transformBool == True and transformBool == existingConnection[0]:
                print('The .{} attribute is already being driven by another connection'.format(existingConnection[1]))
                return
    
    # Create a list of the transform input/output strings (The rotation outputs are long hand because decomposeMatrix abbreviates it to .or, while quatToEuler abbrevaites it to .ort).
    trsIo = [('t', 'ot'), ('tx', 'otx'), ('ty', 'oty'), ('tz', 'otz'), ('r', 'outputRotate'), ('rx', 'outputRotateX'), ('ry', 'outputRotateY'), ('rz', 'outputRotateZ'), ('s', 'os'), ('sx', 'osx'), ('sy', 'osy'), ('sz', 'osz')]
    
    if len(sel) == 2:
        # Create variables for the two selected nodes.
        parent = sel[0]
        child = sel[1]
        
        # Create a variable for reference to know if the driven node is a joint, and if so, check if rotations are being constrained.
        isJnt = False
        constrainRotate = False
        if cmds.nodeType(child) == 'joint':
            isJnt = True
            for r in trsBools[4:7]:
                if r == True:
                    constrainRotate = True
        
        # Create multMatrix and decomposeMatrix nodes
        multMtx = cmds.shadingNode('multMatrix', asUtility = True, n = '{}_mtxOffset'.format(child))
        decompMtx = cmds.shadingNode('decomposeMatrix', asUtility = True, n = '{}_mtx2srt'.format(child))
        
        # Connect multMatrix and decomposeMatrix nodes
        cmds.connectAttr('{}.wm[0]'.format(parent), '{}.i[1]'.format(multMtx), f = True)
        cmds.connectAttr('{}.pim[0]'.format(child), '{}.i[2]'.format(multMtx), f = True)
        cmds.connectAttr('{}.o'.format(multMtx), '{}.imat'.format(decompMtx), f = True)
        
        # Check for maintain offset, and calculate if True
        if mo == True:
            localOffset = getLocalOffset(parent, child)
            cmds.setAttr('{}.matrixIn[0]'.format(multMtx), localOffset, type = 'matrix')
        
        # Check if the driven node is a joint and if rotations are being constrained, and compensate if True
        if isJnt == True and constrainRotate == True:
            # Create quaternion nodes
            quatProd = cmds.shadingNode('quatProd', asUtility = True, n = '{}_jointOrient_quatProd'.format(child))
            quatInvert = cmds.shadingNode('quatInvert', asUtility = True, n = '{}_jointOrient_quatInvert'.format(child))
            euler2Quat = cmds.shadingNode('eulerToQuat', asUtility = True, n = '{}_jointOrient_euler2Quat'.format(child))
            quat2Euler = cmds.shadingNode('quatToEuler', asUtility = True, n = '{}_jointOrient_quat2Euler'.format(child))
            
            # Connect quaternion nodes
            cmds.connectAttr('{}.oq'.format(decompMtx), '{}.iq1'.format(quatProd), f = True)
            cmds.connectAttr('{}.oq'.format(quatInvert), '{}.iq2'.format(quatProd), f = True)
            cmds.connectAttr('{}.oq'.format(euler2Quat), '{}.iq'.format(quatInvert), f = True)
            cmds.connectAttr('{}.jo'.format(child), '{}.irt'.format(euler2Quat), f = True)
            cmds.connectAttr('{}.oq'.format(quatProd), '{}.iq'.format(quat2Euler), f = True)
        
        # Connect all outputs to the driven node
        for bools, io in zip(trsBools, trsIo):
            if bools == True:
                if io[0][0] == 'r' and isJnt == True:
                    cmds.connectAttr('{}.{}'.format(quat2Euler, io[1]), '{}.{}'.format(child, io[0]), f = True)
                else:
                    cmds.connectAttr('{}.{}'.format(decompMtx, io[1]), '{}.{}'.format(child, io[0]), f = True)
    
    else:
        child = sel[-1]
        
        # Create and connect the wtAddMatrix and decomposeMatrix nodes
        mtxBlend = cmds.shadingNode('wtAddMatrix', asUtility = True, n = '{}_mtxBlend'.format(child))
        decompMtx = cmds.shadingNode('decomposeMatrix', asUtility = True, n = '{}_mtx2srt'.format(child))
        cmds.connectAttr('{}.o'.format(mtxBlend), '{}.imat'.format(decompMtx), f = True)
        
        for s, i in zip(sel, range(len(sel))):
            if s == child:
                print('This is the child')
                continue
            else:
                # Create a multMatrix node
                multMtx = cmds.shadingNode('multMatrix', asUtility = True, n = '{}_mtxOffset{}'.format(child, i))
                
                # Connect the driver, multMtx, and mtxBlend nodes
                cmds.connectAttr('{}.wm[0]'.format(s), '{}.i[1]'.format(multMtx), f = True)
                cmds.connectAttr('{}.pim[0]'.format(child), '{}.i[2]'.format(multMtx), f = True)
                cmds.connectAttr('{}.o'.format(multMtx), '{}.i[{}].m'.format(mtxBlend, i), f = True)
                
                # Check for maintain offset, and calculate if True
                if mo == True:
                    localOffset = getLocalOffset(parent, child)
                    cmds.setAttr('{}.matrixIn[0]'.format(multMtx), localOffset, type = 'matrix')
                
        
        # Connect all outputs to the driven node
        for bools, io in zip(trsBools, trsIo):
            if bools == True:
                cmds.connectAttr('{}.{}'.format(decompMtx, io[1]), '{}.{}'.format(child, io[0]), f = True)

###------------------------------------------------------###

npcUI()

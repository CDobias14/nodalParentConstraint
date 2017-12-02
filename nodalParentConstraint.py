### Nodal Parent Constraint Tool.
# Tool provides a UI to create node based parent constraints using nodes and matrix math.
# As with a standard parent constraint, select the driver first and the driven second.
# In the current version, you cannot constrain an object to multiple drivers. A driven object can only accept a single driver via the tool.
###

import maya.cmds as cmds

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
    moRow = cmds.rowLayout('moRow', nc = 2, cw = [(1, 100), (2, 260)])
    
    # Create maintain offset label and checkbox
    cmds.text(l = 'Maintain offset:', w = 90, al = 'right', p = moRow)
    maintainOffset = cmds.checkBox('maintainOffset', l = '', p = moRow, v = True)
    
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
    constrain = cmds.button('constrain', l = 'Constrain', p = mainLayout, h = 27, w = 360, c = 'nodalParentConstraint(cmds.checkBox("maintainOffset", q = True, v = True), cmds.checkBox("tAll", q = True, v = True), cmds.checkBoxGrp("tXYZ", q = True, va3 = True), cmds.checkBox("rAll", q = True, v = True), cmds.checkBoxGrp("rXYZ", q = True, va3 = True), cmds.checkBox("sAll", q = True, v = True), cmds.checkBoxGrp("sXYZ", q = True, va3 = True))')
    
    ###------------------###
    
    # Show the window
    cmds.showWindow('npcUI')
    


def nodalParentConstraint(mo, tAll, tXYZ, rAll, rXYZ, sAll, sXYZ, *args):
    # Get the selected nodes
    sel = cmds.ls(sl = True)
    
    # Check that exactly two nodes are selected
    if len(sel) != 2:
        print("Must select exactly two nodes")
        return
    
    # Create rotation output variable in case driven node is a joint
    rOut = ('{}_mtx2srt.outputRotate'.format(sel[1]))
    
    # Create and connect multMatrix and decomposeMatrix nodes
    cmds.shadingNode('decomposeMatrix', asUtility = True, n = '{}_mtx2srt'.format(sel[1]))
    cmds.shadingNode('multMatrix', asUtility = True, n = '{}_mtxOffset'.format(sel[1]))
    cmds.connectAttr('{}.wm[0]'.format(sel[0]), '{}_mtxOffset.i[1]'.format(sel[1]), f = True)
    cmds.connectAttr('{}.pim[0]'.format(sel[1]), '{}_mtxOffset.i[2]'.format(sel[1]), f = True)
    cmds.connectAttr('{}_mtxOffset.o'.format(sel[1]), '{}_mtx2srt.imat'.format(sel[1]), f = True)
    
    
    # Check for maintain offset, and calculate if True
    if mo == True:
        # Get offset
        cmds.connectAttr('{}.wim[0]'.format(sel[1]), '{}_mtxOffset.i[2]'.format(sel[1]), f = True)
        cmds.shadingNode('multMatrix', asUtility = True, n = '{}_tempForOffset'.format(sel[1]))
        cmds.connectAttr('{}.wm[0]'.format(sel[1]), '{}_tempForOffset.i[0]'.format(sel[1]), f = True)
        cmds.connectAttr('{}.wim[0]'.format(sel[0]), '{}_tempForOffset.i[1]'.format(sel[1]), f = True)
        offset = cmds.getAttr('{}_tempForOffset.o'.format(sel[1]))
        
        # Set offset
        cmds.setAttr('{}_mtxOffset.i[0]'.format(sel[1]), offset, type = 'matrix')
        
        # Clean up (Delete temp node and reconnect the driven's parent inverse matrix)
        cmds.delete('{}_tempForOffset'.format(sel[1]))
        cmds.connectAttr('{}.pim[0]'.format(sel[1]), '{}_mtxOffset.i[2]'.format(sel[1]), f = True)
    
    
    # Check if the driven node is a joint, and compensate if True
    if cmds.objectType(sel[1], i = 'joint'):
        # Create quaternion nodes
        cmds.shadingNode('quatProd', asUtility = True, n = '{}_jointOrient_quatProd'.format(sel[1]))
        cmds.shadingNode('quatInvert', asUtility = True, n = '{}_jointOrient_quatInvert'.format(sel[1]))
        cmds.shadingNode('eulerToQuat', asUtility = True, n = '{}_jointOrient_euler2Quat'.format(sel[1]))
        cmds.shadingNode('quatToEuler', asUtility = True, n = '{}_jointOrient_quat2Euler'.format(sel[1]))
        
        # Connect quaternion nodes
        cmds.connectAttr('{}_mtx2srt.oq'.format(sel[1]), '{}_jointOrient_quatProd.iq1'.format(sel[1]), f = True)
        cmds.connectAttr('{}_jointOrient_quatInvert.oq'.format(sel[1]), '{}_jointOrient_quatProd.iq2'.format(sel[1]), f = True)
        cmds.connectAttr('{}_jointOrient_euler2Quat.oq'.format(sel[1]), '{}_jointOrient_quatInvert.iq'.format(sel[1]), f = True)
        cmds.connectAttr('{}.jo'.format(sel[1]), '{}_jointOrient_euler2Quat.irt'.format(sel[1]), f = True)
        cmds.connectAttr('{}_jointOrient_quatProd.oq'.format(sel[1]), '{}_jointOrient_quat2Euler.iq'.format(sel[1]), f = True)
        
        # Update rotation output variable
        rOut = ('{}_jointOrient_quat2Euler.outputRotate'.format(sel[1]))
    
    # Connect all outputs to the driven node
    for var in [(tAll, tXYZ, '{}_mtx2srt.outputTranslate'.format(sel[1]), 't'), (rAll, rXYZ, rOut, 'r'), (sAll, sXYZ, '{}_mtx2srt.outputScale'.format(sel[1]), 's')]:
        if var[0] == True:
            cmds.connectAttr('{}'.format(var[2]), '{}.{}'.format(sel[1], var[3]), f = True)
        else:
            for axis in [(0, 'X', 'x'), (1, 'Y', 'y'), (2, 'Z', 'z')]:
                if var[1][axis[0]] == True:
                    cmds.connectAttr('{}{}'.format(var[2], axis[1]), '{}.{}{}'.format(sel[1], var[3], axis[2]), f = True)


npcUI()

# nodalParentConstraint
This tool lets you create node-based parent constraints with the click of a button, which will calculate much faster than your standard Maya parent constraints. Additionally, these constraints won't clutter up your outliner! Though to be fair, they may clutter up your node editor.

Use:
The Nodal Parent Constraint interface works almost identically to the standard Maya Parent Constraint interface. Maintaining offset and defining constrained axes works the same.

It does, however, have some limitations. As of the current version, you're unable to constrain an object to multiple drivers. It is possible to blend between two node-based constraints, but you would have to implement that manually, as the tool does not currently create such a system. Therefore, tool only works if you have exactly two objects selected: the driver, and the driven.

If you want to remove a constraint, you'll need to use the node editor to graph the downstream or upstream connections of the driver or driven node, respectively. It's best practice to first disconnect the driven node from the system, and then delete the associated math nodes, therefore ensuring none of your values go haywire during the removal. If you try to recreate the parent constraint while the original math nodes still exist, the function will fail.

Python module for Windows Server Failover Clustering
=====

This module manage the Windows Server Failover Clustering using the Windows API.

Features
--------
* List cluster nodes, resources and group
* Get node, resource and group status
* Move group between nodes
* Start and stop resources and group

Install
--------
::

    pip install pymscluster`

Example
--------
.. code-block:: python

    import mscluster

    c = Cluster()

    print('Cluster name: {}'.format(c.name))
    
    for Gname in c.groups:
        G = c.openGroup(Gname)
        Gnode = G.node
        Gstate = G.state
        print('ResourceGroup[%s] state[%s] ownerNode[%s]' % (Gname, Gstate.name, Gnode))

    for Nname in c.nodes:
        N = c.openNode(Nname)
        Nstate = N.state
        print('Node[%s] state[%s]' % (Nname, Nstate.name))

    for Rname in c.resources:
        R = c.openResource(Rname)
        Rstate = R.state
        Rgroup = R.state.group
        Rnode = Rstate.node
        Rtype = R.type
        print("Resource[%s] Type[%s] State[%s] OwnedBy[%s] Group[%s]"
              % (Rname, Rtype, Rstate.state.name, Rnode, Rgroup))

    r = c.openResource("IP Address 192.168.12.236")
    r.takeOffline()
    t.takeOnline()
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
    
    c = mscluster.Cluster("localhost")

    print('Cluster name: {}'.format(c.name))
    
    for gname in c.groups:
        g = c.openGroup(gname)
        gnode = g.node
        gstate = g.state
        print('Resource Group: {}, state: {}, owner node: {}'.format(gname, gstate.name, gnode))

    for nname in c.nodes:
        n = c.openNode(nname)
        nstate = n.state
        print('Node: {}, state: {}'.format(nname, nstate.name))

    for rname in c.resources:
        r = c.openResource(rname)
        rstate = r.state
        print('Resource: {}, state: {}, node: {}, group: {}'.format(rname, rstate.state.name, rstate.node, rstate.group))

    r = c.openResource("IP Address 192.168.12.236")
    r.takeOffline()
    t.takeOnline()

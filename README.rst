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
    # Sample:
    # Resource[ICDB] Type[SQL Server Availability Group] State[ClusterResourceOnline] OwnedBy[srv-icdb02] Group[ICDB]
    # Resource[Cluster Name] Type[Network Name] State[ClusterResourceOnline] OwnedBy[srv-icdb1] Group[Cluster Group]
    # Resource[ICDB_2620:10d:c081:3::e16] Type[IPv6 Address] State[ClusterResourceFailed] OwnedBy[srv-icdb2] Group[ICDB]
    # Resource[ICDB_2620:10d:c085:106::203] Type[IPv6 Address] State[ClusterResourceOffline] OwnedBy[srv-icdb2] Group[ICDB]
    # Resource[ICDB_2620:10d:c0a8:1e::222] Type[IPv6 Address] State[ClusterResourceOnline] OwnedBy[srv-icdb2] Group[ICDB]


    r = c.openResource("IP Address 192.168.12.236")
    r.takeOffline()
    t.takeOnline()
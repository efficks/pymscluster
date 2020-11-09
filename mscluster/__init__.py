#!/usr/bin/env python3

"""Windows Clustering API for Python.

Based on https://github.com/efficks/pymscluster, revamped by frembiakowski@fb.com.

Vast majority of this code is just wrappers around native API described here:
    https://docs.microsoft.com/en-us/windows/win32/api/_mscs/

>>> import mscluster
>>> c = mscluster.Cluster()

"""

import doctest
import sys
from ctypes import Structure, WinError, byref, create_unicode_buffer, sizeof, windll
from ctypes.wintypes import BOOL, DWORD, HANDLE, LONG, LPCWSTR, LPDWORD, LPVOID, LPWSTR
from enum import IntEnum, IntFlag
from winreg import (
    HKEY_LOCAL_MACHINE,
    EnumKey,
    OpenKey,
    QueryInfoKey,
    QueryValueEx,
)


# import DLLs. if this fails, all the rest fails.
clusapi = windll.clusapi

# Define ClusAPI enums & structs. TODO: Import this from system instead.


class CLUSTER_ENUM(IntFlag):
    """https://docs.microsoft.com/en-us/windows/win32/api/clusapi/ne-clusapi-cluster_enum"""

    CLUSTER_ENUM_NODE = 2 ** 0
    CLUSTER_ENUM_RESTYPE = 2 ** 1
    CLUSTER_ENUM_RESOURCE = 2 ** 2
    CLUSTER_ENUM_GROUP = 2 ** 3
    CLUSTER_ENUM_NETWORK = 2 ** 4
    CLUSTER_ENUM_NETINTERFACE = 2 ** 5
    CLUSTER_ENUM_SHARED_VOLUME_GROUP = 2 ** 29
    CLUSTER_ENUM_SHARED_VOLUME_RESOURCE = 2 ** 30
    CLUSTER_ENUM_INTERNAL_NETWORK = 2 ** 31
    CLUSTER_ENUM_ALL = 2 ** 32 - 1


class CLUSTER_GROUP_STATE(IntEnum):
    """https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-getclustergroupstate"""

    ClusterGroupStateUnknown = -1
    ClusterGroupOnline = 0
    ClusterGroupOffline = 1
    ClusterGroupFailed = 2
    ClusterGroupPartialOnline = 3
    ClusterGroupPending = 4


class CLUSTER_NODE_STATE(IntEnum):
    """https://docs.microsoft.com/en-us/windows/win32/api/clusapi/ne-clusapi-cluster_node_state"""

    ClusterNodeStateUnknown = -1
    ClusterNodeUp = 0
    ClusterNodeDown = 1
    ClusterNodePaused = 2
    ClusterNodeJoining = 3


class CLUSTER_RESOURCE_STATE(IntEnum):
    """https://docs.microsoft.com/en-us/windows/win32/api/clusapi/ne-clusapi-cluster_resource_state"""

    ClusterResourceStateUnknown = -1
    ClusterResourceInherited = 0
    ClusterResourceInitializing = 1
    ClusterResourceOnline = 2
    ClusterResourceOffline = 3
    ClusterResourceFailed = 4
    ClusterResourcePending = 128
    ClusterResourceOnlinePending = 129
    ClusterResourceOfflinePending = 130


# Define function wrappers.

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-closecluster
CloseCluster = clusapi.CloseCluster
CloseCluster.argtypes = [HANDLE]
CloseCluster.restype = BOOL

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-closeclustergroup
CloseClusterGroup = clusapi.CloseClusterGroup
CloseClusterGroup.argtypes = [HANDLE]
CloseClusterGroup.restype = BOOL

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-closeclusternode
CloseClusterNode = clusapi.CloseClusterNode
CloseClusterNode.argtypes = [HANDLE]
CloseClusterNode.restype = BOOL

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-closeclusterresource
CloseClusterResource = clusapi.CloseClusterResource
CloseClusterResource.argtypes = [HANDLE]
CloseClusterResource.restype = BOOL

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clustercloseenum
ClusterCloseEnum = clusapi.ClusterCloseEnum
ClusterCloseEnum.argtypes = [HANDLE]
ClusterCloseEnum.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clusterenum
ClusterEnum = clusapi.ClusterEnum
ClusterEnum.argtypes = [HANDLE, DWORD, LPDWORD, LPWSTR, LPDWORD]
ClusterEnum.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clustergroupcloseenum
ClusterGroupCloseEnum = clusapi.ClusterGroupCloseEnum
ClusterGroupCloseEnum.argtypes = [HANDLE]
ClusterGroupCloseEnum.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clustergroupenum
ClusterGroupEnum = clusapi.ClusterGroupEnum
ClusterGroupEnum.argtypes = [HANDLE, DWORD, LPDWORD, LPWSTR, LPDWORD]
ClusterGroupEnum.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clustergroupopenenum
ClusterGroupOpenEnum = clusapi.ClusterGroupOpenEnum
ClusterGroupOpenEnum.argtypes = [HANDLE, DWORD]
ClusterGroupOpenEnum.restype = HANDLE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clusteropenenum
ClusterOpenEnum = clusapi.ClusterOpenEnum
ClusterOpenEnum.argtypes = [HANDLE, DWORD]
ClusterOpenEnum.restype = HANDLE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clusterresourcetypecloseenum
ClusterResourceTypeCloseEnum = clusapi.ClusterResourceTypeCloseEnum
ClusterResourceTypeCloseEnum.argtypes = [HANDLE]
ClusterResourceTypeCloseEnum.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clusterresourcetypeenum
ClusterResourceTypeEnum = clusapi.ClusterResourceTypeEnum
ClusterResourceTypeEnum.argtypes = [HANDLE, DWORD, LPDWORD, LPWSTR, LPDWORD]
ClusterResourceTypeEnum.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clusterresourcetypeopenenum
ClusterResourceTypeOpenEnum = clusapi.ClusterResourceTypeOpenEnum
ClusterResourceTypeOpenEnum.argtypes = [HANDLE, LPCWSTR, DWORD]
ClusterResourceTypeOpenEnum.restype = HANDLE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-getclustergroupstate
GetClusterGroupState = clusapi.GetClusterGroupState
GetClusterGroupState.argtypes = [HANDLE, LPWSTR, LPDWORD]
GetClusterGroupState.restype = CLUSTER_GROUP_STATE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-getclusterinformation
GetClusterInformation = clusapi.GetClusterInformation
GetClusterInformation.argtypes = [HANDLE, LPWSTR, LPDWORD, LPVOID]
GetClusterInformation.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-getclusternodeid
GetClusterNodeId = clusapi.GetClusterNodeId
GetClusterNodeId.argtypes = [HANDLE, LPWSTR, LPDWORD]
GetClusterNodeId.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-getclusternodestate
GetClusterNodeState = clusapi.GetClusterNodeState
GetClusterNodeState.argtypes = [HANDLE]
GetClusterNodeState.restype = CLUSTER_NODE_STATE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-getclusterresourcestate
GetClusterResourceState = clusapi.GetClusterResourceState
GetClusterResourceState.argtypes = [HANDLE, LPWSTR, LPDWORD, LPWSTR, LPDWORD]
GetClusterResourceState.restype = CLUSTER_RESOURCE_STATE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-offlineclusterresource
OfflineClusterResource = clusapi.OfflineClusterResource
OfflineClusterResource.argtypes = [HANDLE]
OfflineClusterResource.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-onlineclusterresource
OnlineClusterResource = clusapi.OnlineClusterResource
OnlineClusterResource.argtypes = [HANDLE]
OnlineClusterResource.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-opencluster
OpenCluster = clusapi.OpenCluster
OpenCluster.argtypes = [LPCWSTR]
OpenCluster.restype = HANDLE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-openclustergroup
OpenClusterGroup = clusapi.OpenClusterGroup
OpenClusterGroup.argtypes = [HANDLE, LPCWSTR]
OpenClusterGroup.restype = HANDLE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-openclusternode
OpenClusterNode = clusapi.OpenClusterNode
OpenClusterNode.argtypes = [HANDLE, LPCWSTR]
OpenClusterNode.restype = HANDLE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-openclusterresource
OpenClusterResource = clusapi.OpenClusterResource
OpenClusterResource.argtypes = [HANDLE, LPCWSTR]
OpenClusterResource.restype = HANDLE

# mscluster classes


class Cluster(object):
    """
    >>> import mscluster
    >>> C = mscluster.Cluster()
    """

    def __init__(self, address: str = None):
        self.__address = address
        self.__handle = OpenCluster(address)
        if not self.__handle:
            raise WinError()

    @property
    def handle(self):
        return self.__handle

    @property
    def name(self):
        name = create_unicode_buffer(255)
        count = DWORD(sizeof(name))
        if 0 != GetClusterInformation(self.handle, name, byref(count), None):
            raise WinError()
        return name.value

    @property
    def groups(self):
        for g in self.__enum(CLUSTER_ENUM.CLUSTER_ENUM_GROUP):
            yield g

    @property
    def nodes(self):
        for g in self.__enum(CLUSTER_ENUM.CLUSTER_ENUM_NODE):
            yield g

    @property
    def resources(self):
        for g in self.__enum(CLUSTER_ENUM.CLUSTER_ENUM_RESOURCE):
            yield g

    @property
    def resourcetypes(self):
        pass
        # ClusterResourceTypeOpenEnum?

    @property
    def networks(self):
        for n in self.__enum(CLUSTER_ENUM.CLUSTER_ENUM_NETWORK):
            yield n

    def __enum(self, type: CLUSTER_ENUM):
        objectType = DWORD(type)
        name = create_unicode_buffer(0)
        count = DWORD(0)
        index = 0

        enum = ClusterOpenEnum(self.handle, objectType)
        if not enum:
            raise WinError()
        try:
            while True:
                result = ClusterEnum(enum, index, objectType, name, count)
                if result == 234:  # ERROR_MORE_DATA
                    count.value += 1
                    name = create_unicode_buffer(count.value)
                    result = ClusterEnum(enum, index, objectType, name, count)
                if result == 259:  # ERROR_NO_MORE_ITEMS
                    break
                yield name.value
                index += 1
        finally:
            ClusterCloseEnum(enum)

    def openGroup(self, name: LPCWSTR):
        """
        >>> import mscluster
        >>> C = mscluster.Cluster()
        >>> Cg = next(C.groups)
        >>> Gh = C.openGroup(Cg)
        """
        gh = OpenClusterGroup(self.handle, name)
        if not gh:
            raise WinError()
        return Group(gh, name)

    def openResource(self, name: LPCWSTR):
        """
        >>> import mscluster
        >>> C = mscluster.Cluster()
        >>> Cr = next(C.resources)
        >>> R = C.openResource(Cr)
        """
        rh = OpenClusterResource(self.handle, name)
        if not rh:
            raise WinError()
        return Resource(rh, name)

    def openNode(self, name: LPCWSTR):
        """
        >>> import mscluster
        >>> C = mscluster.Cluster()
        >>> Cn = next(C.nodes)
        >>> Nh = C.openNode(Cn)
        """
        nh = OpenClusterNode(self.handle, name)
        if not nh:
            raise WinError()
        return Node(nh, name)

    def __del__(self):
        if self.handle:
            CloseCluster(self.handle)

    @property
    def clusternodeid(self):
        buf = create_unicode_buffer(255)
        count = DWORD(sizeof(buf))
        res = GetClusterNodeId(None, buf, byref(count))
        return buf.value


class Group(object):
    """
    >>> import mscluster
    >>> C = mscluster.Cluster()
    >>> Cgroup = next(C.groups)
    >>> G = C.openGroup(Cgroup)
    >>> Gstate = G.state
    >>> Gnode = G.node
    >>> Gresources = G.resources
    >>> list(Gresources)
    ['AG-LABC_2620:10d:c085:106::1da', 'AG-LABC', 'AG-LABC_2620:10d:c0a8:1d::166', 'AG-LABC_2620:10d:c085:206::1c0', 'AG-LABC_cn-labc']
    """

    def __init__(self, handle: HANDLE, name: LPCWSTR):
        self.__handle = handle
        self.__name = name

    @property
    def handle(self):
        return self.__handle

    @property
    def name(self):
        return self.__name

    @property
    def state(self):
        state = GetClusterGroupState(self.__handle, None, None)
        return CLUSTER_GROUP_STATE(state)

    def takeOffline(self):
        result = OfflineClusterGroup(self.__handle)
        if result != 0:
            raise WinError()

    def takeOnline(self):
        result = OnlineClusterGroup(self.__handle)
        if result != 0:
            raise WinError()

    def moveTo(self, node: "Node"):
        result = MoveClusterGroup(self.__handle, node.handle)
        if result != 0:
            raise WinError()

    @property
    def node(self):
        name = create_unicode_buffer(255)
        count = DWORD(sizeof(name))
        GetClusterGroupState(self.__handle, name, byref(count))
        return name.value

    @property
    def resources(self):
        """Enumerate resource names within group."""
        dwType = DWORD(1)
        enum = ClusterGroupOpenEnum(self.handle, dwType)
        if not enum:
            raise WinError()

        index = 0
        try:
            while True:
                buf = create_unicode_buffer(255)
                buflen = DWORD(sizeof(buf))
                result = ClusterGroupEnum(
                    enum, index, byref(dwType), buf, byref(buflen)
                )
                if result == 234:  # ERROR_MORE_DATA
                    raise RuntimeError(
                        "buffer overflow - ClusterGroupEnum returns ERROR_MORE_DATA"
                    )
                if result == 259:  # ERROR_NO_MORE_ITEMS
                    break
                yield buf.value
                index += 1
        finally:
            ClusterGroupCloseEnum(enum)

    def __del__(self):
        if self.__handle:
            CloseClusterGroup(self.handle)


class ResourceState(object):
    def __init__(self, state: CLUSTER_RESOURCE_STATE, node: LPCWSTR, group: LPCWSTR):
        self.__state = state
        self.__node = node
        self.__group = group

    @property
    def state(self):
        return self.__state

    @property
    def node(self):
        return self.__node

    @property
    def group(self):
        return self.__group


class Resource(object):

    """WFC cluster resource object."""

    def __init__(self, handle: HANDLE, name: LPCWSTR):
        self.__handle = handle
        self.__name = name

    @property
    def handle(self):
        return self.__handle

    @property
    def name(self):
        return self.__name

    @property
    def state(self):
        """Get cluster resource state.

        Returns a ResourceState object with 3 properties:
            * state: current state of the specified resource, part of CLUSTER_RESOURCE_STATE enum.
            * node: name of the specified resource's current owner node.
            * group: name of the group that contains the specified resource.
        """
        _node = create_unicode_buffer(255)
        _group = create_unicode_buffer(255)
        _state = GetClusterResourceState(
            self.handle,
            _node,
            byref(DWORD(sizeof(_node))),
            _group,
            byref(DWORD(sizeof(_group))),
        )
        return ResourceState(_state, _node.value, _group.value)

    @property
    def type(self):
        """Get resource type.

        NOTE: this winreg-based method enumerates all resources which makes it a bit slower. But, IT WORKS.

        >>> import mscluster
        >>> C = mscluster.Cluster()
        >>> while (True):
        ...     Cr = next(C.resources)
        ...     if Cr == 'AG-LABC':
        ...         R = C.openResource(Cr)
        ...         Rtype = R.type
        ...         break
        >>> Rtype
        'SQL Server Availability Group'
        """
        with OpenKey(HKEY_LOCAL_MACHINE, "Cluster\Resources") as rsKey:
            (rskeys, rsvals, rsmod) = QueryInfoKey(rsKey)
            for n in range(rskeys):
                rid = EnumKey(rsKey, n)
                with OpenKey(rsKey, rid) as rKey:
                    (rname, rname_t) = QueryValueEx(rKey, "Name")
                    if rname == self.name:
                        (rtype, rtype_t) = QueryValueEx(rKey, "Type")
                        return rtype
        raise RuntimeError("Unable to find resource type for [{}]".format(self.name))

    def takeOffline(self):
        result = OfflineClusterResource(self.__handle)
        if result != 0:
            raise WinError()

    def takeOnline(self):
        result = OnlineClusterResource(self.__handle)
        if result != 0:
            raise WinError()

    def __del__(self):
        if self.__handle:
            CloseClusterResource(self.__handle)


class Node(object):

    """WFC cluster node object.

    >>> import mscluster
    >>> C = mscluster.Cluster()
    >>> Cnode = next(C.nodes)
    >>> N = C.openNode(Cnode)
    >>> Nstate = N.state
    >>> Nstate.name
    'ClusterNodeUp'
    """

    def __init__(self, handle: HANDLE, name: LPCWSTR):
        self.__handle = handle
        self.__name = name

    @property
    def handle(self):
        return self.__handle

    @property
    def name(self):
        return self.__name

    @property
    def state(self):
        return GetClusterNodeState(self.__handle)

    def __del__(self):
        if self.__handle:
            CloseClusterNode(self.__handle)


if __name__ == "__main__":
    if sys.platform != "win32":
        raise RuntimeError("This program is for Windows only")
    doctest.testmod()

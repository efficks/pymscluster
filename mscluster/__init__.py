#!/usr/bin/env python3

"""Windows Clustering API for Python.

Based on https://github.com/efficks/pymscluster, revamped by frembiakowski@fb.com.

Vast majority of this code is just wrappers around native API described here:
    https://docs.microsoft.com/en-us/windows/win32/api/_mscs/

"""

import ctypes
from ctypes.wintypes import *
import unittest
from enum import IntEnum


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
    ClusterResourceStateUnknown    = -1
    ClusterResourceInherited       = 0
    ClusterResourceInitializing    = 1
    ClusterResourceOnline          = 2
    ClusterResourceOffline         = 3
    ClusterResourceFailed          = 4
    ClusterResourcePending         = 128
    ClusterResourceOnlinePending   = 129
    ClusterResourceOfflinePending  = 130


class CLUSTER_ENUM(IntEnum):
    """https://docs.microsoft.com/en-us/windows/win32/api/clusapi/ne-clusapi-cluster_enum"""
    CLUSTER_ENUM_NODE                   = 2 ** 0
    CLUSTER_ENUM_RESTYPE                = 2 ** 1
    CLUSTER_ENUM_RESOURCE               = 2 ** 2
    CLUSTER_ENUM_GROUP                  = 2 ** 3
    CLUSTER_ENUM_NETWORK                = 2 ** 4
    CLUSTER_ENUM_NETINTERFACE           = 2 ** 5
    CLUSTER_ENUM_SHARED_VOLUME_GROUP    = 2 ** 29
    CLUSTER_ENUM_SHARED_VOLUME_RESOURCE = 2 ** 30
    CLUSTER_ENUM_INTERNAL_NETWORK       = 2 ** 31
    CLUSTER_ENUM_ALL                    = 2 ** 32 - 1


# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-opencluster
OpenCluster = ctypes.windll.ClusAPI.OpenCluster
OpenCluster.argtypes = [LPCWSTR]
OpenCluster.restype = HANDLE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-closecluster
CloseCluster = ctypes.windll.ClusAPI.CloseCluster
CloseCluster.argtypes = [HANDLE]
CloseCluster.restype = BOOL

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-getclusterinformation
GetClusterInformation = ctypes.windll.ClusAPI.GetClusterInformation
GetClusterInformation.argtypes = [HANDLE, LPWSTR, LPDWORD, LPVOID]
GetClusterInformation.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clusteropenenum
ClusterOpenEnum = ctypes.windll.ClusAPI.ClusterOpenEnum
ClusterOpenEnum.argtypes = [HANDLE, DWORD]
ClusterOpenEnum.restype = HANDLE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clustercloseenum
ClusterCloseEnum = ctypes.windll.ClusAPI.ClusterCloseEnum
ClusterCloseEnum.argtypes = [HANDLE]
ClusterCloseEnum.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clusterenum
ClusterEnum = ctypes.windll.ClusAPI.ClusterEnum
ClusterEnum.argtypes = [HANDLE, DWORD, LPDWORD, LPWSTR, LPDWORD]
ClusterEnum.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clustergroupopenenum
ClusterGroupOpenEnum = ctypes.windll.ClusAPI.ClusterGroupOpenEnum
ClusterGroupOpenEnum.argtypes = [HANDLE, DWORD]
ClusterGroupOpenEnum.restype = HANDLE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clustergroupcloseenum
ClusterGroupCloseEnum = ctypes.windll.ClusAPI.ClusterGroupCloseEnum
ClusterGroupCloseEnum.argtypes = [HANDLE]
ClusterGroupCloseEnum.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clustergroupenum
ClusterGroupEnum = ctypes.windll.ClusAPI.ClusterGroupEnum
ClusterGroupEnum.argtypes = [HANDLE, DWORD, LPDWORD, LPWSTR, LPDWORD]
ClusterGroupEnum.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-openclustergroup
OpenClusterGroup = ctypes.windll.ClusAPI.OpenClusterGroup
OpenClusterGroup.argtypes = [HANDLE, LPCWSTR]
OpenClusterGroup.restype = HANDLE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-closeclustergroup
CloseClusterGroup = ctypes.windll.ClusAPI.CloseClusterGroup
CloseClusterGroup.argtypes = [HANDLE]
CloseClusterGroup.restype = BOOL

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-getclustergroupstate
GetClusterGroupState = ctypes.windll.ClusAPI.GetClusterGroupState
GetClusterGroupState.argtypes = [HANDLE, LPWSTR, LPDWORD]
GetClusterGroupState.restype = CLUSTER_GROUP_STATE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-openclusterresource
OpenClusterResource = ctypes.windll.ClusAPI.OpenClusterResource
OpenClusterResource.argtypes = [HANDLE, LPCWSTR]
OpenClusterResource.restype = HANDLE

CloseClusterResource = ctypes.windll.ClusAPI.CloseClusterResource
CloseClusterResource.argtypes = [HANDLE]
CloseClusterResource.restype = BOOL

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-getclusterresourcestate
GetClusterResourceState = ctypes.windll.ClusAPI.GetClusterResourceState
GetClusterResourceState.argtypes = [HANDLE, LPWSTR, LPDWORD, LPWSTR, LPDWORD]
GetClusterResourceState.restype = CLUSTER_RESOURCE_STATE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-offlineclusterresource
OfflineClusterResource = ctypes.windll.ClusAPI.OfflineClusterResource
OfflineClusterResource.argtypes = [HANDLE]
OfflineClusterResource.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-onlineclusterresource
OnlineClusterResource = ctypes.windll.ClusAPI.OnlineClusterResource
OnlineClusterResource.argtypes = [HANDLE]
OnlineClusterResource.restype = DWORD

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-openclusternode
OpenClusterNode = ctypes.windll.ClusAPI.OpenClusterNode
OpenClusterNode.argtypes = [HANDLE, LPCWSTR]
OpenClusterNode.restype = HANDLE

CloseClusterNode = ctypes.windll.ClusAPI.CloseClusterNode
CloseClusterNode.argtypes = [HANDLE]
CloseClusterNode.restype = BOOL

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-getclusternodestate
GetClusterNodeState = ctypes.windll.ClusAPI.GetClusterNodeState
GetClusterNodeState.argtypes = [HANDLE]
GetClusterNodeState.restype = CLUSTER_NODE_STATE

# https://docs.microsoft.com/en-us/windows/win32/api/clusapi/nf-clusapi-clustercontrol
ClusterControl = ctypes.windll.ClusAPI.ClusterControl
ClusterControl.argtypes = [HANDLE, HANDLE, DWORD, LPVOID, DWORD, LPVOID, DWORD, LPDWORD]
ClusterControl.restype = DWORD


class Cluster(object):

    def __init__(self, address: str):
        self.__address = address
        self.__handle = OpenCluster(address)
        if not self.__handle:
            raise ctypes.WinError()

    @property
    def name(self):
        count = DWORD(255)
        name = ctypes.create_unicode_buffer(255)
        if 0 != GetClusterInformation(self.__handle, name, ctypes.byref(count), None):
            raise ctypes.WinError()
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
    def networks(self):
        for n in self.__enum(CLUSTER_ENUM.CLUSTER_ENUM_NETWORK):
            yield n

    def __enum(self, type: CLUSTER_ENUM):
        objectType = DWORD(type)
        name = ctypes.create_unicode_buffer(0)
        count = DWORD(0)
        index = 0

        enum = ClusterOpenEnum(self.__handle, objectType)
        if not enum:
            raise ctypes.WinError()
        try:
            while True:
                result = ClusterEnum(enum, index, objectType, name, count)
                if result == 234: #ERROR_MORE_DATA
                    count.value += 1
                    name = ctypes.create_unicode_buffer(count.value)
                    result = ClusterEnum(enum, index, objectType, name, count)
                if result == 259: #ERROR_NO_MORE_ITEMS
                    break
                yield name.value
                index += 1
        finally:
            if enum:
                ClusterCloseEnum(enum)

    def openGroup(self, name: LPCWSTR):
        handle = OpenClusterGroup(self.__handle, name)
        if not handle:
            raise ctypes.WinError()
        return Group(handle, name)

    def openResource(self, name: LPCWSTR):
        handle = OpenClusterResource(self.__handle, name)
        if not handle:
            raise ctypes.WinError()
        return Resource(handle, name)

    def openNode(self, name: LPCWSTR):
        handle = OpenClusterNode(self.__handle, name)
        if not handle:
            raise ctypes.WinError()
        return Node(handle, name)

    def __del__(self):
        if self.__handle:
            CloseCluster(self.__handle)


class Group(object):

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
            raise ctypes.WinError()

    def takeOnline(self):
        result = OnlineClusterGroup(self.__handle)
        if result != 0:
            raise ctypes.WinError()

    def moveTo(self, node: Node):
        result = MoveClusterGroup(self.__handle, node.handle)
        if result != 0:
            raise ctypes.WinError()

    @property
    def node(self):
        name = ctypes.create_unicode_buffer(255)
        count = DWORD(255)
        GetClusterGroupState(self.__handle, name, ctypes.byref(count))
        return name.value

    @property
    def resources(self):
        objectType = DWORD(8)
        name = ctypes.create_unicode_buffer(0)
        count = DWORD(0)
        index = 0

        enum =  ClusterGroupOpenEnum(self.__handle, 1)
        if not enum:
            raise ctypes.WinError()

        try:
            while True:
                result = ClusterGroupEnum(enum, index, objectType, name, count)
                if result == 234: #ERROR_MORE_DATA
                    count.value += 1
                    name = ctypes.create_unicode_buffer(count.value)
                    result = ClusterEnum(enum, index, objectType, name, count)
                if result == 259: #ERROR_NO_MORE_ITEMS
                    break
                yield name.value
                index += 1
        finally:
            if enum:
                ClusterGroupCloseEnum(enum)

    def __del__(self):
        if self.__handle:
            CloseClusterGroup(self.__handle)


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
        _node = ctypes.create_unicode_buffer(255)
        _group = ctypes.create_unicode_buffer(255)
        _size = DWORD(255)
        _state = GetClusterResourceState(self.__handle, _node, ctypes.byref(_size), _group, ctypes.byref(_size))
        return ResourceState(_state, _node.value, _group.value)

    def __del__(self):
        if self.__handle:
            CloseClusterResource(self.__handle)

    def takeOffline(self):
        result = OfflineClusterResource(self.__handle)
        if result != 0:
            raise ctypes.WinError()

    def takeOnline(self):
        result = OnlineClusterResource(self.__handle)
        if result != 0:
            raise ctypes.WinError()


class Node(object):

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


if __name__ == '__main__':
    unittest.main();
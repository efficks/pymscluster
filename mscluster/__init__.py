import ctypes
import ctypes.wintypes
import unittest
from enum import IntEnum

if not hasattr(ctypes.wintypes, 'LPDWORD'):
    ctypes.wintypes.LPDWORD = ctypes.POINTER(ctypes.wintypes.DWORD)

ClusterOpenEnum = ctypes.windll.ClusAPI.ClusterOpenEnum
ClusterOpenEnum.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD]
ClusterOpenEnum.restype = ctypes.wintypes.HANDLE

ClusterCloseEnum = ctypes.windll.ClusAPI.ClusterCloseEnum
ClusterCloseEnum.argtypes = [ctypes.wintypes.HANDLE]

ClusterEnum = ctypes.windll.ClusAPI.ClusterEnum
ClusterEnum.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD, ctypes.wintypes.LPDWORD, ctypes.wintypes.LPWSTR, ctypes.wintypes.LPDWORD]
ClusterEnum.restype = ctypes.wintypes.DWORD

ClusterGroupOpenEnum = ctypes.windll.ClusAPI.ClusterGroupOpenEnum
ClusterGroupOpenEnum.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD]
ClusterGroupOpenEnum.restype = ctypes.wintypes.HANDLE

ClusterGroupCloseEnum = ctypes.windll.ClusAPI.ClusterGroupCloseEnum
ClusterGroupCloseEnum.argtypes = [ctypes.wintypes.HANDLE]

ClusterGroupEnum = ctypes.windll.ClusAPI.ClusterGroupEnum
ClusterGroupEnum.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD, ctypes.wintypes.LPDWORD, ctypes.wintypes.LPWSTR, ctypes.wintypes.LPDWORD]
ClusterGroupEnum.restype = ctypes.wintypes.DWORD

OpenClusterGroup = ctypes.windll.ClusAPI.OpenClusterGroup
OpenClusterGroup.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.LPCWSTR]
OpenClusterGroup.restype = ctypes.wintypes.HANDLE

GetClusterGroupState = ctypes.windll.ClusAPI.GetClusterGroupState
GetClusterGroupState.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.LPWSTR, ctypes.wintypes.LPDWORD]
GetClusterGroupState.restype = ctypes.wintypes.DWORD

OpenClusterResource = ctypes.windll.ClusAPI.OpenClusterResource
OpenClusterResource.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.LPCWSTR]
OpenClusterResource.restype = ctypes.wintypes.HANDLE

OpenClusterNode = ctypes.windll.ClusAPI.OpenClusterNode
OpenClusterNode.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.LPCWSTR]
OpenClusterNode.restype = ctypes.wintypes.HANDLE

class Cluster(object):
    def __init__(self, address):
        self.__address = address
        self.__handle = None

        fn_openCluster = ctypes.windll.ClusAPI.OpenCluster
        fn_openCluster.restype = ctypes.c_void_p
        self.__handle = ctypes.windll.ClusAPI.OpenCluster(address)

        if not self.__handle:
            raise ctypes.WinError()
    
    @property
    def name(self):
        count = ctypes.wintypes.DWORD(255)
        name = ctypes.create_unicode_buffer(255)
        if 0 != ctypes.windll.ClusAPI.GetClusterInformation(self.__handle, name, ctypes.byref(count), None):
            raise ctypes.WinError()
        return name.value
    
    @property
    def groups(self):
        for g in self.__enum(8):
            yield g

    @property
    def nodes(self):
        for g in self.__enum(1):
            yield g
    
    @property
    def resources(self):
        for g in self.__enum(4):
            yield g

    def __enum(self, type):
        objectType = ctypes.wintypes.DWORD(type)
        name = ctypes.create_unicode_buffer(0)
        count = ctypes.wintypes.DWORD(0)
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
                index+=1

        finally:
            if enum:
                ClusterCloseEnum(enum)

    def openGroup(self, groupName):
        handle = OpenClusterGroup(self.__handle, groupName)
        if not handle:
            raise ctypes.WinError()
        return Group(handle, groupName)
    
    def openResource(self, name):
        handle = OpenClusterResource(self.__handle, name)
        if not handle:
            raise ctypes.WinError()
        return Resource(handle, name)
    
    def openNode(self, name):
        handle = OpenClusterNode(self.__handle, name)
        if not handle:
            raise ctypes.WinError()
        return Node(handle, name)

    def __del__(self):
        if self.__handle:
            ctypes.windll.ClusAPI.CloseCluster(self.__handle)

class CLUSTER_GROUP_STATE(IntEnum):
    ClusterGroupStateUnknown = -1
    ClusterGroupOnline = 0
    ClusterGroupOffline = 1
    ClusterGroupFailed = 2
    ClusterGroupPartialOnline = 3
    ClusterGroupPending = 4

class Group(object):
    def __init__(self, groupHandle, name):
        self.__handle = groupHandle
        self.__name = name
    
    @property
    def name(self):
        return self.__name

    @property
    def state(self):
        state = ctypes.windll.ClusAPI.GetClusterGroupState(self.__handle, None, None)
        return CLUSTER_GROUP_STATE(state)

    def takeOffline(self):
        result = ctypes.windll.ClusAPI.OfflineClusterGroup(self.__handle)
        if result != 0:
            raise ctypes.WinError()
    
    def takeOnline(self):
        result = ctypes.windll.ClusAPI.OnlineClusterGroup(self.__handle)
        if result != 0:
            raise ctypes.WinError()
        
    def moveTo(self, node):
        result = ctypes.windll.ClusAPI.MoveClusterGroup(self.__handle, node.handle)
        if result != 0:
            raise ctypes.WinError()
    
    @property
    def node(self):
        name = ctypes.create_unicode_buffer(255)
        count = ctypes.wintypes.DWORD(255)
        ctypes.windll.ClusAPI.GetClusterGroupState(self.__handle, name, ctypes.byref(count))
        return name.value

    @property
    def resources(self):
        objectType = ctypes.wintypes.DWORD(8)
        name = ctypes.create_unicode_buffer(0)
        count = ctypes.wintypes.DWORD(0)
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
                index+=1

        finally:
            if enum:
                ClusterGroupCloseEnum(enum)

    def __del__(self):
        if self.__handle:
            ctypes.windll.ClusAPI.CloseClusterGroup(self.__handle)

class CLUSTER_RESOURCE_STATE(IntEnum):
    ClusterResourceStateUnknown    = -1
    ClusterResourceInherited       = 0
    ClusterResourceInitializing    = 1
    ClusterResourceOnline          = 2
    ClusterResourceOffline         = 3
    ClusterResourceFailed          = 4
    ClusterResourcePending         = 128
    ClusterResourceOnlinePending   = 129
    ClusterResourceOfflinePending  = 130

class Resource(object):
    def __init__(self, handle, name):
        self.__handle = handle
        self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def state(self):
        state = ctypes.windll.ClusAPI.GetClusterResourceState(self.__handle, None, None, None, None)
        return CLUSTER_RESOURCE_STATE(state)

    def __del__(self):
        if self.__handle:
            ctypes.windll.ClusAPI.CloseClusterResource(self.__handle)
    
    def takeOffline(self):
        result = ctypes.windll.ClusAPI.OfflineClusterResource(self.__handle)
        if result != 0:
            raise ctypes.WinError()
    
    def takeOnline(self):
        result = ctypes.windll.ClusAPI.OnlineClusterResource(self.__handle)
        if result != 0:
            raise ctypes.WinError()

class Node(object):
    def __init__(self, handle):
        self.__handle = handle
    
    @property
    def handle(self):
        return self.__handle

    def __del__(self):
        if self.__handle:
            ctypes.windll.ClusAPI.CloseClusterNode(self.__handle)

if __name__ == '__main__':
    unittest.main();
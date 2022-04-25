import errno
import rados,sys
from package.HelperServices.Helper import *

#Press enter for skip

## FOR POOL
# List pool :
def listPool(cluster):
    try:
        print("\nAvailable Pools")
        print("----------------")
        pools = cluster.list_pools()

        for pool in pools:
            print(pool)
    except rados.Error as e:
        print("Rados command error : {}".format(e))

## FOR ioctx
# Write Object :
def writeObject(ioctx):
    try:
        fileLocation = input("\nInput file [Example : /path/to/file] : ")
        objectName = input("Input Object Name : ")
        file = convertFileToByte(fileLocation)
        ioctx.write_full(objectName,file)
        return objectName
    except rados.Error as e:
        print("Rados command error : {}".format(e))

# List Object : 
def listObjects(ioctx):
    try:
        print("\nAvailable Objects in cephfs_data pool")
        print("----------------")
        object_iterator = ioctx.list_objects()
        while True :
            rados_object = object_iterator.__next__()
            print("Object contents = {}".format(rados_object.read()))
    except StopIteration :
        print("Unexpected error")
    except rados.Error as e:
        print("Rados command error : {}".format(e))

# Get Object :
def getObject(ioctx):
    try:
        print("\nGet Object out from cephfs_data pool")
        print("----------------")
    except rados.Error as e:
        print("Rados command error : {}".format(e))

# Read Object : 
# def readUnscannedObject(ioctx):
#     try:

#     except rados.Error as e :
#         print("Rados command error : {}".format(e))
def readObject(ioctx):
    try:
        defaultLength = 8192
        print("\nRead Object out from cephfs_data pool")
        print("----------------")
        key = input("\nInput name of object :")
        length = input("\nLength :")
        fileName = input("\nOutput file name :")
        if (length):
            content = ioctx.read(key,length,0)
        else:
            content = ioctx.read(key)
        
    except rados.Error as e :
        print("Rados command error : {}".format(e))

# Remove Object : 
def removeObject(ioctx):
    try:
        print("\nRemove Object out from cephfs_data pool")
        print("----------------")
        key = input("\nInput name of object :")
        ioctx.read(key)
    except rados.Error as e:
        print("Rados command error : {}".format(e))

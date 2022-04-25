import sys, rados, pyclamd
from package.RadosFunction.RadosServices import *

def executeCephCommand():
    return 0

def menu():
    print("CEPH COMMAND MENU")
    print("[1] List objects")
    print("[2] Put Objects to pool")
    print("[3] Get Object from pool")
    print("[4] List pools")
    print("[5] Put Object to pool with AV scan")
    print("[0] Exit the proram")

def connectToRados():
    cluster = rados.Rados(conffile='ceph.conf')
    print("\nlibrados version: {}".format(str(cluster.version())))
    print("Will attempt to connect to: {}".format(str(cluster.conf_get('mon host'))))

    cluster.connect()
    print("\nCluster ID: {}".format(cluster.get_fsid()))

    print("\n\nCluster Statistics")
    print("==================")
    cluster_stats = cluster.get_cluster_stats()
    return cluster
    

def main():
    scanning_location = "/home/mons-2/for-scanning/"
    print("Check ClamAV : ")
    clamDev = pyclamd.ClamAgnostic()
    clamDev.ping()
    print(clamDev.version())
    print("Connect to Cluster : ")
    cluster = rados.Rados(conffile='')
    print("\nlibrados version: {}".format(str(cluster.version())))
    print("Will attempt to connect to: {}".format(str(cluster.conf_get('mons-1'))))

    cluster.connect()
    print("\nCluster ID: {}".format(cluster.get_fsid()))

    print("\n\nCluster Statistics")
    print("==================")
    cluster_stats = cluster.get_cluster_stats()

    for key, value in cluster_stats.items():
        print(key, value)
    
    #For input and output only
    ioctx = cluster.open_ioctx('cephfs_data')
    unscanIoctx = cluster.open_ioctx('for_scanning')
    # ioctx.write_full("hw", "Hello World!")
    # ioctx.write_full("hw1", "Hello World!1")
    # ioctx.write_full("hw2", "Hello World!2")
    
    #For menu
    menu()
    option = int(input("Enter your option : "))
    while option != 0:
        if option == 1 :
            #Do option 1
            listObjects(ioctx)
            pass
        elif option == 2 :
            print("\nPut Object to pool")
            print("----------------")
            writeObject(ioctx)
            pass
        elif option == 3 :
            print("\nGet Object from pool")
            print("----------------")
            getObject(ioctx)
            pass
        elif option == 4 :
            listPool(cluster)
            pass
        elif option == 5 :
            print("\nPut Object to pool")
            print("----------------")
            #Input object in unscanned pool
            objectName = writeObject(unscanIoctx)
            result = outputObjectFromUnscannedToMachine(scanning_location, objectName)
            if result == 1:
                print("No threat found in file")
            #Output object to scanning folder
            else:
                print(f"Threat found : {result}")
            pass
        else:
            print("Invalid option !")
        input("Press Enter to continue...")
        print("***************************************************")
        menu()
        option = int(input("Enter your option : "))



if __name__ == "__main__":
    main()
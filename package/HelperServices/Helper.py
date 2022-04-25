import sys, subprocess, pyclamd, os

#Convert file to byte

def convertFileToByte(fileLocation):
    f = open(fileLocation,"rb")
    return f.read()

def inputContentToFile(fileLocation, content):
    f = open(f"/home/mons-2/for-scanning/{fileLocation}","rb")
    f.write(content)
    f.close()

def outputObjectFromUnscannedToMachine(fileLocation,objectName ):
    subprocess.Popen(['ls', '-la'], shell=False)
    print("\nGet object to scanned folder")
    subprocess.Popen(['sudo','rados get', f'{objectName}',f'{fileLocation}{objectName}','--pool=for-scan'])
    print("\nScan file and change name file(scanned) if virus annouce to user")
    cd = pyclamd.ClamdAgmpstic()
    result = cd.scan_file(f'{fileLocation}{objectName}')
    if result is None:
        os.rename(f'{fileLocation}{objectName}',f'{fileLocation}{objectName}(CLEAN)')
        print("\nPut clean scanned object to pool")
        subprocess.Popen(['sudo','rados put', f'{fileLocation}{objectName}(CLEAN)', f'{fileLocation}{objectName}(CLEAN)','--pool=cephfs-data'])
        return 1

    else:
        print(f'{result}')
        os.rename(f'{fileLocation}{objectName}',f'{fileLocation}{objectName}(NOT-CLEAN)')
        print("\nPut not clean scanned object to pool")
        subprocess.Popen(['sudo','rados put', f'{fileLocation}{objectName}(NOT-CLEAN)',f'{fileLocation}{objectName}(NOT-CLEAN)','--pool=cephfs-data'])
        return result
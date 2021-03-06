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
    subprocess.Popen(['ls', '-la'], shell=False).wait()
    print("\nGet object to scanned folder")
    pGet = subprocess.Popen(f'rados get {objectName} {fileLocation}{objectName} --pool=for_scanning', shell = True)
    pGet.wait()
    print("\nScan file and change name file(scanned) if virus annouce to user")
    cd = pyclamd.ClamdAgnostic()
    result = cd.scan_file(f'{fileLocation}{objectName}')
    if result is None:
        os.rename(f'{fileLocation}{objectName}',f'{fileLocation}{objectName}_CLEAN')
        print("\nPut clean scanned object to pool")
        subprocess.Popen(f'rados put {objectName}_CLEAN {fileLocation}{objectName}_CLEAN --pool=cephfs_data', shell = True).wait()
        return 1

    else:
        print(f'{result}')
        os.rename(f'{fileLocation}{objectName}',f'{fileLocation}{objectName}_NOT_CLEAN')
        print("\nPut not clean scanned object to pool")
        subprocess.Popen(f'rados put {objectName}_NOT_CLEAN {fileLocation}{objectName}_NOT_CLEAN --pool=cephfs_data', shell = True).wait()
        return result
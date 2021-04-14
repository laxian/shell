import os
import zipfile

class ZipCompress(object):
    def __init__(self):
        pass

    @staticmethod
    def zip_file(dirName, zipFileName):
        fileList = []
        if os.path.isfile(dirName):
            fileList.append(dirName)
        else:
            for root, dirs, files in os.walk(dirName):
                fileList.extend([os.path.join(root, name) for name in files])
        zf = zipfile.ZipFile(zipFileName, "w", zipfile.zlib.DEFLATED)
        [zf.write(tar) for tar in fileList]
        zf.close()

    @staticmethod
    def unzip_file(zipFileName, unzipDir):
        if not os.path.exists(unzipDir): os.mkdir(unzipDir)
        zf = zipfile.ZipFile(zipFileName)
        for name in zf.namelist():
            if name.endswith("/"):
                os.mkdir(os.path.join(unzipDir, name))
            else:
                ext_fileName = os.path.join(unzipDir, name)
                ext_dir = os.path.dirname(ext_fileName)
                if not os.path.exists(ext_dir): os.makedirs(ext_dir)
                open(ext_fileName, "wb").write(zf.read(name))

    @staticmethod
    def add_file(zipFileName, fileName):
        zf = zipfile.ZipFile(zipFileName, "a", zipfile.zlib.DEFLATED)
        zf.write(fileName)
        zf.close()

    @staticmethod
    def get_file(zipFileName, unzipDir, fileName):
        if not os.path.exists(unzipDir): os.makedirs(unzipDir)
        zf = zipfile.ZipFile(zipFileName, "r")
        name = os.path.basename(fileName)
        open(os.path.join(unzipDir, name), "wb").write(zf.read(fileName))

    @staticmethod
    def add_dir(zipFileName, dirName):
        zf = zipfile.ZipFile(zipFileName, "a", zipfile.zlib.DEFLATED)
        for root, dirs, files in  os.walk(dirName):
            [zf.write(os.path.join(root, fileName)) for fileName in files]
        zf.close()

    @staticmethod
    def get_dir(zipFileName, dirName, unzipDir):
        if not os.path.exists(unzipDir): os.makedirs(unzipDir)
        zf = zipfile.ZipFile(zipFileName, "r")
        for fileName in zf.namelist():
            zipFilePath = os.path.normpath(os.path.dirname(fileName))
            dirName = os.path.normpath(dirName)
            if zipFilePath[:len(dirName)] == dirName:
                name = os.path.join(unzipDir, fileName)
                dirPath = os.path.dirname(name)
                if not os.path.exists(dirPath): os.makedirs(dirPath)
                open(fileName, "wb").write(zf.read(fileName))
        zf.close()

if __name__ == "__main__":
    dirName = r"."
    zipFileName = "test.zip"

    ZipCompress.zip_file(dirName, zipFileName)

    # ZipCompress.unzip_file(zipFileName, ".")

    # ZipCompress.add_file("test.zip", "compressFile.py")

    # ZipCompress.get_file("test.zip", "F:/", "compressFile.py")

    # ZipCompress.add_dir("test.zip", r"F:\dll")

    # ZipCompress.get_dir("test.zip", "dll", ".")
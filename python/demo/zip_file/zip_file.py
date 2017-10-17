#-*- encoding：utf--*-

import os
import zipfile

class ZipFile(object):
    """ 将文件压缩成zip包 """
    def __init__(self, zipfilename):
        """ 初始化变量 """
        self.zipfilename = zipfilename
        self.mode = "w"
        self.zf = zipfile.ZipFile(self.zipfilename, self.mode, compression = zipfile.zlib.DEFLATED)

    def zip_file(self, abs_filename, relative_filename):
        """ 压缩文件，第一个参数代表要压缩的源文件，第二个参数代表压缩到压缩包里的相对路径的文件名称 """
        self.zf.write(abs_filename, relative_filename, zipfile.ZIP_DEFLATED)

    def close(self):
        """ 关闭打开的文件对象 """
        self.zf.close()

		
if __name__ == "__main__":
    src = r"/home/goland/develop/flask/DVDFab_Auto_Test"
    zipfile = os.path.join(src, "test.zip")
    zf = ZipFile(zipfile)
    for roots, dirs, files in os.walk(src):
        for each_file in files:
            filename = os.path.join(roots, each_file)
            zf.zip_file(filename, filename[len(src):])
    zf.close()
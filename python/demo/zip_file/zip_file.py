#-*- encoding��utf--*-

import os
import zipfile

class ZipFile(object):
    """ ���ļ�ѹ����zip�� """
    def __init__(self, zipfilename):
        """ ��ʼ������ """
        self.zipfilename = zipfilename
        self.mode = "w"
        self.zf = zipfile.ZipFile(self.zipfilename, self.mode, compression = zipfile.zlib.DEFLATED)

    def zip_file(self, abs_filename, relative_filename):
        """ ѹ���ļ�����һ����������Ҫѹ����Դ�ļ����ڶ�����������ѹ����ѹ����������·�����ļ����� """
        self.zf.write(abs_filename, relative_filename, zipfile.ZIP_DEFLATED)

    def close(self):
        """ �رմ򿪵��ļ����� """
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
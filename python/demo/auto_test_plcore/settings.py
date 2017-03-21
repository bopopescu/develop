#-*- encoding:utf-8-*-

import os

EXCEL_FILE = r"plcore_auto_test.xls"
MOVIE_EXCEL_FILE = r"movie.xls"

PLAYBACK_XML = r"info.xml"

""" log文件的扩展名 """
EXTEND_NAME = "log"

""" player log的存放路径 """
LOG_PATH_IN_BOX = "/mnt/sdcard/Android/data/org.vidonme.vvplayer/Log/"
LOG_PATH = r"D:/build_scripts/auto_test_plcore/logfile/"


""" player的info文件 """
INFO_FILE = "player-info.log"

""" player log的后半部分名字 """
PLAYER_LOG_EXTEND_NAME = "player.log"

""" 所有的log的压缩后的文件名的后半部分 """
POSTFIX_ZIPFILENAME = r"player.zip"

""" 上传log压缩包的http路径 """
HTTP_URL = "log_url"

""" ping盒子的次数 """
PING_COUNT = 4


""" 上传log文件的路径 """
REMOTE_LOG_PATH = r"/Logstash"
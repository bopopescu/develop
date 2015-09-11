import os,sys
path = "/home/goland/test_crash_log"
if path not in sys.path:
    sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_crash_log.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

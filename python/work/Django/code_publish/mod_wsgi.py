import os,sys
sys.path.append("/home/goland/develop/code_publish")
os.environ["DJANGO_SETTINGS_MODULE"] = "code_publish.settings"
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

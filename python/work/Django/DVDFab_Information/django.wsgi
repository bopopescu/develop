import os,sys
django_path = "/Library/Python/2.7/site-packages/django"
if django_path not in sys.path:
    sys.path.append(django_path)

project_path = "/Users/DVDFab/DVDFab_Information"
if project_path not in sys.path:
    sys.path.append(project_path)

os.environ['DJANGO_SETTINGS_MODULE'] = "DVDFab_Information.settings"
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

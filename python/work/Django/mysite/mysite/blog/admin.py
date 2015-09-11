from django.contrib import admin
from models import *

admin.site.register(Client)
admin.site.register(Web_params)
admin.site.register(Versions)
admin.site.register(Case)

admin.site.register(Samples)
admin.site.register(DVD_samples)
admin.site.register(BD3D_samples)
admin.site.register(Session)
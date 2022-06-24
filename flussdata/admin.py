from django.contrib import admin

from .models import *

# informational tables
admin.site.register(River)
admin.site.register(Campaign)
admin.site.register(MeasStation)


# data valued tables
admin.site.register(Freezecore)
admin.site.register(IDOC)
admin.site.register(Kf)
admin.site.register(ShovelSample)
admin.site.register(FreezePanel)
admin.site.register(LineSampling)
admin.site.register(Flow)



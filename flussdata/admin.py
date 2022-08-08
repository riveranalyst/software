from django.contrib import admin

from .models import *

# informational tables
admin.site.register(River)
admin.site.register(Campaign)
admin.site.register(MeasStation)


# data valued tables
admin.site.register(SubsurfaceSed)
admin.site.register(SurfaceSed)
admin.site.register(SedSamplTechnique)
admin.site.register(IDOC)
admin.site.register(Kf)
admin.site.register(Flow)
admin.site.register(CollectedData)


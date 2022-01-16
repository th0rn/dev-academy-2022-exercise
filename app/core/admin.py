from django.contrib import admin

from .models import Farm
from .models import FarmReport
from .models import Temperature
from .models import Ph
from .models import Rainfall


class SensorReadingsInline(admin.TabularInline):
    max_num = 1


class TemperatureInline(SensorReadingsInline):
    model = Temperature


class PhInline(SensorReadingsInline):
    model = Ph


class RainfallInline(SensorReadingsInline):
    model = Rainfall


class FarmReportAdmin(admin.ModelAdmin):
    inlines = [TemperatureInline, PhInline, RainfallInline, ]


admin.site.register(Farm)
admin.site.register(FarmReport, FarmReportAdmin)
admin.site.register(Temperature)
admin.site.register(Ph)
admin.site.register(Rainfall)

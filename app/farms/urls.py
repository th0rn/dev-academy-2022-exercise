"""URL Configuration """

from django.contrib import admin
from django.urls import include
from django.urls import path
#  from django.urls import url

from rest_framework import routers

#  from core.views import FarmReportListView
from core import views

# Automatic API URL routing
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'farmreports', views.FarmReportViewSet)
router.register(r'selectreports', views.SelectReportViewSet)
#  router.register(r'stats', views.StatsReportView)

# End points for login URLs and for the browsable API
urlpatterns = [
    path('admin/', admin.site.urls),
    #  path('farms/', FarmReportListView.as_view()),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', views.index, name='farmreports'),
    #  path('selectreports', views.index, name='farmreports'),
]

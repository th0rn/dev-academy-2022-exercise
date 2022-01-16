#  from django.views.generic import ListView
from collections import OrderedDict
import sys
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.db.models import Avg
from django.db.models import Min
from django.db.models import Max

from django_tables2 import SingleTableView
from rest_framework import viewsets
from rest_framework import permissions
#  from rest_framework import generics

from core.models import FarmReport
from core.tables import FarmReportsTable
from core.serializers import UserSerializer
from core.serializers import GroupSerializer
from core.serializers import FarmReportSerializer
#  from core.serializers import StatsSerializer


def index(request):
    return render(request, 'index.html')


class UserViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows users to be viewed or edited. """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class FarmReportViewSet(viewsets.ModelViewSet):
    """API endpoint for farm reports. """
    queryset = FarmReport.objects.all()
    serializer_class = FarmReportSerializer
    #  permission_classes = [permissions.IsAuthenticated]


# Note: There are obviously negative performance implications when calculating stats on
#       all (filtered) queries, but perhaps the case could be made that in most cases a
#       user fetching the data would be interested in seeing them.
class MultiFilterFarmMixin:
    """
    Mixin to modify get_queryset method that does backend filtering based on url params.

    """

    def get_queryset(self):
        """ Override the get_queryset method to provide the required backend filtering.

            Allows for filtering by any or all of the following:
                farm_id, year, month, temperature, ph, rainfall
        """

        # Get the base queryset, accessing directly to avoid infinite loop.
        objs = self.queryset
        for k, v in self.request.query_params.items():
            print(f'{k}: {v}', file=sys.stderr)

            match k:
                case 'farm_id':
                    objs = objs.filter(farm_id=v)
                case 'year':
                    objs = objs.filter(date__year=v)
                case 'month':
                    # Month is queried without year, allowing to fetch data f. ex. for
                    # all Februaries.
                    objs = objs.filter(date__month=v)
                case 'temperature':
                    objs = objs.filter(temperature__temperature__isnull=False)
                case 'ph':
                    objs = objs.filter(ph__ph__isnull=False)
                case 'rainfall':
                    objs = objs.filter(rainfall__rainfall__isnull=False)
                case _:
                    pass

        return objs


# Note: This tries to address the following backend requirements from the specs:
#
#  - Endpoints to fetch data from farms with different granularities (by month, by
#    metric)
#  - Aggregate calculation endpoints, endpoint which returns monthly averages, min/max
#    and other statistical analysis
#
#  However, it's unclear what "granularity" means in this context.
class SelectReportViewSet(MultiFilterFarmMixin, viewsets.ModelViewSet):
    """ Get a limited set of data, with stats, limited by any combination of:
        - farm_id
        - year
        - month
        - (the existance of a) temperature measurement
        - (the existance of a) pH measurement
        - (the existance of a) rainfall measurement
    """

    def list(self, request, *args, **kwargs):
        """ Override list method to add stats to response. """
        response = super().list(request, args, kwargs)
        qset = self.get_queryset()
        aggregates = [
            qset.aggregate(mean_temperature=Avg('temperature__temperature')),
            qset.aggregate(min_temperature=Min('temperature__temperature')),
            qset.aggregate(max_temperature=Max('temperature__temperature')),
            qset.aggregate(mean_ph=Avg('ph__ph')),
            qset.aggregate(min_ph=Min('ph__ph')),
            qset.aggregate(max_ph=Max('ph__ph')),
            qset.aggregate(mean_rainfall=Avg('rainfall__rainfall')),
            qset.aggregate(min_rainfall=Min('rainfall__rainfall')),
            qset.aggregate(max_rainfall=Max('rainfall__rainfall')),
        ]
        stats = {}
        [stats.update(a) for a in aggregates]
        response.data.update(stats)
        return response

    # Our base queryset to be filtered by our mixin (does not hit the database).
    queryset = FarmReport.objects.all()
    serializer_class = FarmReportSerializer
    #  permission_classes = [permissions.IsAuthenticated]


class FarmReportListView(SingleTableView):
    model = FarmReport
    table_class = FarmReportsTable
    template_name = 'core/farms.html'

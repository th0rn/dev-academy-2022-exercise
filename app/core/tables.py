#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Our customized django-tables2 table with bootstrap. """

import django_tables2 as tables
from .models import FarmReport
#  from .models import Temperature


class FarmReportsTable(tables.Table):
    date = tables.DateTimeColumn(format='d.m.y H:i')
    temperature = tables.Column(
        verbose_name='Temperature',
        accessor=tables.A('temperature.temperature'),
        #  accessor='farm_report.temperature',
        linkify=True,
    )
    ph = tables.Column(verbose_name='pH')
    rainfall = tables.Column(verbose_name='Rainfall')

    class Meta:
        model = FarmReport
        template_name = "django_tables2/bootstrap.html"
        fields = ("farm", "date", "temperature.tostr", 'ph', "rainfall", )
        #  fields = ("farm", "date", "ph", "rainfall", )

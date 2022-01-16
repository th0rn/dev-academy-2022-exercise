#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for CSV parsing, validation, and importing data from .csv files into our
database.

"""

import csv
import os.path
from decimal import Decimal
from decimal import InvalidOperation

from django.db.utils import IntegrityError

from core.models import Farm
from core.models import FarmReport
from core.models import Temperature
from core.models import Ph
from core.models import Rainfall


def import_csv(farm_id, filepath):
    """ Function to import a single csv-file.

    From each row, we take the date(time), sensor type, and measurement. We ignore the
    farm name, since presumably there's no good reason for farms to report data for
    other farms, and makes our database more vulnerable to bad imports.
    """

    print('Importing csv…')
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', )
        # Gives us rows like this:
        # ['PartialTech Research Farm', '2018-12-31T22:00:00.000Z', 'rainFall', '1.4']
        next(reader)  # Skip first (header) row.
        for row in reader:
            print(row)
            # TODO: Not sure why this is borked, but look at that later.
            try:
                obj, created = FarmReport.objects.get_or_create(
                    farm=Farm.objects.get(pk=farm_id),
                    date=row[1],
                )
            except IntegrityError as e:
                print(f'Ignoring {e}')
            if obj is None and created is False:
                print('Failed to get or create, moving on…')
                next
            match row[2]:
                case 'temperature':
                    try:
                        value = Decimal(row[3])
                        assert value >= -50 and value <= 100
                        Temperature.objects.get_or_create(
                            farm_report=obj,
                            temperature=value,
                        )
                    except (InvalidOperation, AssertionError):
                        print('Invalid temperature, ignoring…')
                case 'pH':
                    try:
                        value = Decimal(row[3])
                        assert value >= 0 and value <= 14
                        Ph.objects.get_or_create(
                            farm_report=obj,
                            ph=value,
                        )
                    except (InvalidOperation, AssertionError):
                        print('Invalid pH, ignoring…')
                case 'rainFall':
                    try:
                        value = Decimal(row[3])
                        assert value >= 0 and value <= 500
                        Rainfall.objects.get_or_create(
                            farm_report=obj,
                            rainfall=value,
                        )
                    except (InvalidOperation, AssertionError):
                        print('Invalid rainfall value, ignoring…')
                case _:
                    print('Found a non-meaningful metric, ignoring…')


def import_all():
    """ Imports all the data from all the CSV files. """
    for farm in Farm.objects.all():
        print(farm.input_file)
        filename = farm.input_file
        rel_path = os.path.dirname(__file__) + '/../../' + filename
        import_csv(farm.id, rel_path)
        print('ok')

""" Database model abstractions for the application. """

from django.db import models


class Farm(models.Model):
    """ The meta information relating to a farm. """

    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=64)
    input_file = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class FarmReport(models.Model):
    """ A time at which a farm has reported one or more pieces of data.

    Fields:
        primary key (int) - automatic (hidden)
        farm (int) - value corresponding to one of the four farms
        date (datetime) - reported time of measurement
        time_reported (bool) - whether the date field has a meaningful time component
    """

    class Meta:
        """By default, sort readings by date, latest first. """
        ordering = ['-date']

    #  # Since there are so few farms, we store them as integers and look them up.
    #  FARMS = (
        #  (0, 'Noora\'s farm'),
        #  (1, 'Friman Metsola collective'),
        #  (2, 'Organic Ossi\'s Impact That Lasts plantation'),
        #  (3, 'PartialTech Research Farm'),
    #  )
    #  farm = models.PositiveSmallIntegerField(choices=FARMS)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)

    # Data without a date is useless, so we do not allow that.
    date = models.DateTimeField()
    # Rather than two separate fields, one for datetime and one for date, since input
    # could be either, we simply record whether the time component of the datetime was
    # reported. Looking at the data, it appears that farms typically do report datetime
    # rather than date, so we default to True.
    # TODO: Implement this.
    time_reported = models.BooleanField(default=True)

    def friendly(self):
        return self.date.strftime('%d.%m.%Y %H:%M')

    def __str__(self):
        return f'Report for {self.farm} from {self.date.strftime("%d.%m.%Y %H:%M")}'


class Temperature(models.Model):
    """The temperature measurement of a farm report. """

    farm_report = models.OneToOneField(
        FarmReport,
        related_name='temperature',
        on_delete=models.CASCADE,
    )
    # Each datum point could have any one of these three (but not the other two).
    # Hottest temperature ever recorded is 56.7°C, so 99.9°C rather than 100.0°C should
    # be a sufficient upper limit for our farm weather software.
    temperature = models.DecimalField(max_digits=3, decimal_places=1)

    def tostr(self):
        return '{:0.2f}'.format(self.temperature)
        #  return str(self.temperature)

    def __str__(self):
        return f'{self.temperature}°C'


class Ph(models.Model):
    """The pH measurement of a farm report. """

    farm_report = models.OneToOneField(
        FarmReport,
        related_name='ph',
        on_delete=models.CASCADE,
    )
    # f.ex. pH 12.34.
    ph = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f'pH {self.ph}'


class Rainfall(models.Model):
    """The rainfall measurement of a farm report. """

    class Meta:
        verbose_name = 'Rainfall'

    farm_report = models.OneToOneField(
        FarmReport,
        related_name='rainfall',
        on_delete=models.CASCADE,
    )
    # f.ex. 333.3 mm.
    rainfall = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return f'{self.rainfall} mm'

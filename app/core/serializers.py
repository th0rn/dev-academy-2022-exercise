from django.contrib.auth.models import User, Group

from rest_framework import serializers

from core.models import Farm
from core.models import FarmReport


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['name', ]
    #  temperature = serializers.CharField(max_length=5)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class FarmReportSerializer(serializers.ModelSerializer):
    farm = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    # Here we directly give the string representation of our values, for (our)
    # convenience, but of course if our API had other users, this might be very
    # inconvenient for them - in which case we'd return numerical values, and just
    # format in whatever views we needed.
    temperature = serializers.StringRelatedField()
    ph = serializers.StringRelatedField()
    rainfall = serializers.StringRelatedField()

    class Meta:
        model = FarmReport
        fields = ['date', 'farm', 'temperature', 'ph', 'rainfall', ]

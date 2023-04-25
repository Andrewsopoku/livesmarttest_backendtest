from rest_framework import serializers


class TestRangeFloatField(serializers.FloatField):

    def to_representation(self, value):
        if value:
            return int(value)
        return value




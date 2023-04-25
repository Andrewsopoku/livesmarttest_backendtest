from rest_framework import serializers
from bloodtests.models import Test
from bloodtests.validators import RangeValidator


class TestRangeFloatField(serializers.FloatField):
    """ Float field which returns int representation of the value"""
    def to_representation(self, value):
        if value:
            return int(value)
        return value


class TestSerializer(serializers.ModelSerializer):
    ideal_range = serializers.ReadOnlyField()
    lower = TestRangeFloatField(min_value=0, required=False, allow_null=True)
    upper = TestRangeFloatField(min_value=0, required=False, allow_null=True)

    class Meta:
        model = Test
        fields = "__all__"
        validators = [RangeValidator()]


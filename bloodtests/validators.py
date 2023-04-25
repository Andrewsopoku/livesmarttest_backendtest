from rest_framework import serializers


class RangeValidator:
    """ Validate Blood test range fields """

    def __init__(self, lower_field="lower", upper_field="upper"):
        self.lower = lower_field
        self.upper = upper_field

    def __call__(self, attrs):
        # raise exception when lower and upper are
        # present and lower is greater than upper
        if attrs.get(self.lower) and attrs.get(self.upper):
            if attrs.get(self.lower) > attrs.get(self.upper):
                raise serializers.ValidationError(
                        "Lower value can't exceed upper value"
                    )

        # raise exception when both lower and upper are missing
        elif not attrs.get(self.lower) and not attrs.get(self.upper):
            raise serializers.ValidationError(
                "Lower and upper cannot both be null"
            )






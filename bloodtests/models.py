from django.db import models
from django.db.models import Q
from django.db.models import F


class Test(models.Model):
    """
    Model for storing Blood test data
    """
    code = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)
    lower = models.FloatField(null=True)
    upper = models.FloatField(null=True)

    @property
    def ideal_range(self):
        if self.lower and self.upper:
            return f'{self.lower} <= value <= {self.upper}'
        if self.lower:
            return f'value >= {self.lower}'
        else:
            return f'value <= {self.upper}'

    class Meta:
        constraints = [
            # Constraint to check:
            # - Empty lower or upper but not both
            # - When both lower and upper both should be
            # positive and upper should be greater than lower
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_positive_lower_and_or_higher",
                check=(
                        Q(Q(lower__isnull=True) & Q(upper__isnull=False)) |
                        Q(Q(lower__isnull=False) & Q(upper__isnull=True)) |
                        Q(Q(Q(lower__isnull=False) & Q(upper__isnull=False)) &
                          Q(upper__gte=F('lower')) & Q(Q(upper__gte=0) & Q(lower__gte=0))
                          )
                ),
            ),
        ]

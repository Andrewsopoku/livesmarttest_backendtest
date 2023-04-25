import pytest
from django.db import IntegrityError
from bloodtests.models import Test


@pytest.fixture()
def test_data():
    return {'code': 'CHO',
            'name': 'Cholesterol',
            'unit': 'g/M',
            'upper': 99,
            'lower': 45
            }


@pytest.mark.django_db
class TestBloodTestsModel:
    """ Test model constraints against specifications"""

    def test_valid_data(self, test_data):
        # Create test object and check against test_data
        test = Test.objects.create(**test_data)

        assert test.code == test_data["code"]
        assert test.name == test_data["name"]
        assert test.unit == test_data["unit"]
        assert test.upper == test_data["upper"]
        assert test.lower == test_data["lower"]
        assert test.ideal_range == f'{test_data["lower"]} <= value <= {test_data["upper"]}'

    def test_code_duplication(self, test_data):
        # check when same code value is used twice
        with pytest.raises(IntegrityError):
            Test.objects.create(**test_data)
            Test.objects.create(**test_data)

    def test_lower_gte_upper(self, test_data):
        # check when lower is greater than upper
        test_data['lower'] = 70
        test_data['upper'] = 69

        with pytest.raises(IntegrityError):
            Test.objects.create(**test_data)

    def test_without_upper_lower(self, test_data):
        # check when lower and upper are absent
        del test_data['lower']
        del test_data['upper']

        with pytest.raises(IntegrityError):
            Test.objects.create(**test_data)

    def test_without_upper(self, test_data):
        # check when upper is absent
        del test_data['upper']

        test = Test.objects.create(**test_data)
        assert test.upper is None
        assert test.ideal_range == f'value >= {test_data["lower"]}'

    def test_without_lower(self, test_data):
        # check when lower is absent
        del test_data['lower']

        test = Test.objects.create(**test_data)
        assert test.lower is None
        assert test.ideal_range == f'value <= {test_data["upper"]}'

    def test_with_neg_lower_upper(self, test_data):
        # check when lower and upper are non-positive
        test_data['lower'] = -70
        test_data['upper'] = -69

        with pytest.raises(IntegrityError):
            Test.objects.create(**test_data)

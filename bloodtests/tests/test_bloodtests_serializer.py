import pytest
from bloodtests.models import Test
from bloodtests.serializers import TestSerializer


@pytest.fixture()
def test_data():
    return {'code': 'CHO',
            'name': 'Cholesterol',
            'unit': 'g/M',
            'upper': 70,
            'lower': 45
            }


@pytest.fixture()
def get_test(test_data):
    return Test.objects.create(**test_data)


@pytest.fixture()
def get_serializer_instance(get_test):
    return TestSerializer(instance=get_test)


@pytest.mark.django_db
class TestBloodTestsSerializer:
    """ Test serializer constraints against specifications"""

    def test_contains_expected_fields(self, get_serializer_instance):
        # Check serializer keys against expected keys
        data = get_serializer_instance.data

        assert set(data.keys()) == set(['lower', 'unit',
                                        'upper', 'name',
                                        'ideal_range', 'code'
                                        ])

    def test_content(self, test_data, get_serializer_instance):
        # Check serializer instance data against test_data
        data = get_serializer_instance.data

        assert data['code'] == test_data['code']
        assert data['name'] == test_data['name']
        assert data['unit'] == test_data['unit']
        assert data['upper'] == test_data['upper']
        assert data['lower'] == test_data['lower']

    def test_valid_data(self, test_data):
        # Validated valid test_data
        serializer = TestSerializer(data=test_data)

        assert serializer.is_valid() is True

    def test_higher_lower(self, test_data):
        # Check when lower ranger is higher than upper range
        test_data['lower'] = 90
        serializer = TestSerializer(data=test_data)

        assert serializer.is_valid() is False
        assert str(serializer.errors['non_field_errors'][0]) == "Lower value can't exceed upper value"

    def test_missing_code_field(self, test_data):
        # Check without code field
        del test_data['code']
        serializer = TestSerializer(data=test_data)

        assert serializer.is_valid() is False
        assert 'code' in serializer.errors

    def test_missing_lower_upper_fields(self, test_data):
        # Check when both lower and upper are absent
        del test_data['lower']
        del test_data['upper']
        serializer = TestSerializer(data=test_data)

        assert serializer.is_valid() is False
        assert str(serializer.errors['non_field_errors'][0]) == "Lower and upper cannot both be null"

    def test_missing_lower_field(self, test_data):
        # Check when lower is absent
        del test_data['lower']
        serializer = TestSerializer(data=test_data)

        assert serializer.is_valid() is True

    def test_missing_upper_field(self, test_data):
        # Check when upper is absent
        del test_data['upper']
        serializer = TestSerializer(data=test_data)

        assert serializer.is_valid() is True

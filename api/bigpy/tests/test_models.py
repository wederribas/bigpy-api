import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


def test_customerreports():
    obj = mixer.blend('bigpy.CustomerReports')
    assert obj.pk > 0, 'Should be True when model CustomerReports is created'


def test_companyreports():
    obj = mixer.blend('bigpy.CompanyReports')
    assert obj.pk > 0, 'Should be True when model CompanyReports is created'

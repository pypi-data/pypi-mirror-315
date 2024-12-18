from datagarden_models.models import DemographicsV1, EconomicsV1, HealthV1, HouseholdV1, WeatherV1


def test_demographics_v1():
    assert DemographicsV1() is not None


def test_economics_v1():
    assert EconomicsV1() is not None


def test_health_v1():
    assert HealthV1() is not None


def test_household_v1():
    assert HouseholdV1() is not None


def test_weather_v1():
    assert WeatherV1() is not None

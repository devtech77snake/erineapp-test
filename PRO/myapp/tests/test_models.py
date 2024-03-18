import pytest
from django.utils import timezone
from myapp.models import Bus, Driver
import uuid

@pytest.mark.django_db
def test_driver_model():
    driver = Driver.objects.create(
        uuid=uuid.uuid4(),
        first_name="John",
        last_name="Doe",
        birth_date="1980-01-01",
        years_of_experience=5,
        date_joined=timezone.now()
    )

    assert driver.first_name == "John"
    assert driver.years_of_experience == 5

@pytest.mark.django_db
def test_bus_model():
    driver = Driver.objects.create(
        uuid=uuid.uuid4(),
        first_name="John",
        last_name="Doe",
        birth_date="1980-01-01",
        years_of_experience=7,
        date_joined=timezone.now()
    )

    bus = Bus.objects.create(
        uuid=uuid.uuid4(),
        registration_plate="XYZ 1234",
        driver=driver,
        end_destination="Springfield",
        time_of_departure="12:00:00",
        create_date=timezone.now(),
        update_date=timezone.now(),
        max_seats=50,
        seats_available=50,
        status=0
    )

    assert bus.registration_plate == "XYZ 1234"
    assert bus.max_seats == 50
    assert bus.status == 0
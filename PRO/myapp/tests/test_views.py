import pytest
from django.urls import reverse
from django.utils import timezone
from myapp.models import Bus, Driver
import uuid

@pytest.mark.django_db
def test_bus_list(client):
    # Setup test data
    driver = Driver.objects.create(
        uuid=uuid.uuid4(),
        first_name="John",
        last_name="Doe",
        birth_date="1980-01-01",
        years_of_experience=5,
        date_joined=timezone.now()
    )
    Bus.objects.create(
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
    
    url = reverse('bus_list')  # Make sure to name your URL in urls.py
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['driver_name'] == driver.first_name + " " + driver.last_name
    
@pytest.mark.django_db
def test_reserve_seat_success(client, mocker):
    driver = Driver.objects.create(
        uuid=uuid.uuid4(),
        first_name="John",
        last_name="Doe",
        birth_date="1980-01-01",
        years_of_experience=5,
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
    url = reverse('reserve_seat')  # Make sure to name your URL in urls.py
    response = client.post(url, {'id': str(bus.uuid), 'flag': 1}, content_type='application/json')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == "success"
    assert data['data']['available_seats'] == bus.seats_available - 1

@pytest.mark.django_db
def test_reserve_seat_fail(client, mocker):
    driver = Driver.objects.create(
        uuid=uuid.uuid4(),
        first_name="John",
        last_name="Doe",
        birth_date="1980-01-01",
        years_of_experience=5,
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
        seats_available=0,
        status=0
    )
    url = reverse('reserve_seat')  # Make sure to name your URL in urls.py
    response = client.post(url, {'id': str(bus.uuid), 'flag': 1}, content_type='application/json')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == "fail"
    assert "No available seat in this bus" in data['err_msg']
    
@pytest.mark.django_db
def test_unreserve_seat_success(client, mocker):
    driver = Driver.objects.create(
        uuid=uuid.uuid4(),
        first_name="John",
        last_name="Doe",
        birth_date="1980-01-01",
        years_of_experience=5,
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
        seats_available=0,
        status=0
    )
    url = reverse('reserve_seat')  # Make sure to name your URL in urls.py
    response = client.post(url, {'id': str(bus.uuid), 'flag': -1}, content_type='application/json')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == "success"
    assert data['data']['available_seats'] == bus.seats_available + 1

@pytest.mark.django_db
def test_unreserve_seat_fail(client, mocker):
    driver = Driver.objects.create(
        uuid=uuid.uuid4(),
        first_name="John",
        last_name="Doe",
        birth_date="1980-01-01",
        years_of_experience=5,
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
    url = reverse('reserve_seat')  # Make sure to name your URL in urls.py
    response = client.post(url, {'id': str(bus.uuid), 'flag': -1}, content_type='application/json')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == "fail"
    assert "No available seat in this bus" in data['err_msg']
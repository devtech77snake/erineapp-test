import json
from django.middleware.csrf import get_token
from django.core import serializers
from django.http import HttpResponse
from .models import Bus, Driver


# Create your views here.
def hello(request):
    return HttpResponse("hello world")


def bus_list(request):
    print(request.META['HTTP_HOST'])
    csrf_token = get_token(request)
    buses = Bus.objects.all()
    bus_list = []
    for i, bus in enumerate(buses):
        bus_list.append(
            {
                "id": str(bus.uuid),
                "number": i + 1,
                "driver_name": bus.driver.first_name + " " + bus.driver.last_name,
                "max_seats": bus.max_seats,
                "available_seats": bus.seats_available,
                "status": bus.status,
                "status_display": bus.get_status_display(),
            }
        )
    response = HttpResponse(json.dumps({'csrftoken': csrf_token, 'bus_list': bus_list}), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = '*, X-CSRFToken'
    print(csrf_token)
    return response


def reserve_seat(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    print(body)
    response = Bus.objects.filter(uuid=body['id'])
    print(response)
    return HttpResponse(
        json.dumps("this is reserve seat"), content_type="application/json"
    )


def unreserve_seat(request):
    return HttpResponse(
        json.dumps("this is unreserve seat"), content_type="application/json"
    )

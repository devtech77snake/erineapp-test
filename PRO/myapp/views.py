import json
from django.middleware.csrf import get_token
from django.core import serializers
from django.http import HttpResponse
from .models import Bus, Driver


# Create your views here.
def hello(request):
    return HttpResponse("hello world")


def bus_list(request):
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
    response = HttpResponse(json.dumps(bus_list), content_type="application/json")
    return response


def reserve_seat(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        busId = body['id']
        flag = body['flag']
        print(body)
        bus = Bus.objects.get(uuid=busId)
        if (bus.seats_available == 0):
            response = HttpResponse(json.dumps({"status": "fail", "err_msg": "No available seat in this bus"}), content_type="application/json", status=200)
        else:
            if flag == 1:
                bus.seats_available -= 1
            elif flag == -1:
                bus.seats_available += 1
            bus.save()
            print(bus)
            response = HttpResponse(json.dumps({"status": "success", "data": {"available_seats": bus.seats_available, "max_seats": bus.max_seats}, "err_msg": ""}), content_type="application/json", status=200)
            return response
    except IntegrityError as e:
        print(f"Integrity error occurred: {e}")
        response = HttpResponse(json.dumps({"status": "fail", "err_msg": e}), content_type="application/json", status=400)
    except Exception as e:
        print(f"An error occurred: {e}")
        response = HttpResponse(json.dumps({"status": "fail", "err_msg": e}), content_type="application/json", status=400)
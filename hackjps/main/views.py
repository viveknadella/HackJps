from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import RegisterForm
from django.contrib.auth import login as loginn, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User as user
from django.contrib.auth.decorators import login_required, permission_required
from .models import DriverLocation
from math import radians, sin, cos, sqrt, atan2


def home(request):

    template = loader.get_template("index.html")
    context = {
    }
    return HttpResponse(template.render(context, request))

from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                loginn(request, user)
                # Authentication successful
                # Redirect the user to a success page or do something else
                return redirect('/dashboard')
            # Authentication successful
            # Redirect the user to a success page or do something else
            
    else:
        
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def sign_up(request): 
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            loginn(request, user)
            return redirect('/dashboard')

    else:
        form = RegisterForm()
    
    template = loader.get_template("sign-up.html")
    context = {
        "form": form
    }
    return HttpResponse(template.render(context, request))

def about(request):
    template = loader.get_template("About us.html")
    context = {
    }
    return HttpResponse(template.render(context, request))

from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/login")
def dashboard(request):
    if request.user.username == "busdriver1": 
        return redirect("/dashboard/drivers")

    else: 
        return redirect("/dashboard/all")
@login_required(login_url="/login")
def dashboard_drivers(request):
        stops = {
            "addresses": {
                "stoplist1": {
                    "addresses": [
                        'Grove Ave and Wintergreen Ave. West',
                        'Rollingbrook Dr. & Lyle Place',
                        'Rahway Rd & Madaline Dr.',
                        'Rahway Rd & MaryEllen Dr.',
                        'Old Raritan Road & Webb St.',
                        'Old Raritan Rd & Wright St.',
                        'Old Raritan Rd and King St.',
                        'Old Raritan Rd & Inman Ave.',
                        'Tingley Ln & Inman Ave.',
                        'Tingley Ln & Timber Oaks Rd.',
                        'Woodland Ave & Fairview Ave.'
                    ],
                    "points": [
                        [40.59109857762286, -74.36105823371278],
                        [40.593202880468255, -74.36807433871225],
                        [40.598626796900675, -74.37261624691347],
                        [40.60231311292229, -74.37276546040472],
                        [40.601148222969634, -74.38652224691327],
                        [40.60305325778882, -74.38558183527515],
                        [40.599819086274955, -74.38734984691337],
                        [40.5979497594545, -74.38952853156866],
                        [40.596697834211824, -74.37373860458592],
                        [40.586290379177264, -74.37379620273289],
                        [40.560101685502, -74.57742496038142]
                    ]
                }
            }
        }

        import geocoder
        import folium
        import os
        import requests

        api_key = "prj_live_pk_fff0398252df0c8d8d89d153606524b5a2564a24"
        url = "https://api.radar.io/v1/geocode/ip"
        headers = {
            "Authorization": f"{api_key}"
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        ip_address = data["ip"]
        g = geocoder.ip(ip_address)

        latitude = g.latlng[0]
        longitude = g.latlng[1]

        location = f"{latitude},{longitude}"
        g = geocoder.osm(location)
        myAddress = g.latlng

        if myAddress is not None:
            coordinates = [
                [40.59109857762286, -74.36105823371278],
                [40.593202880468255, -74.36807433871225],
                [40.598626796900675, -74.37261624691347],
                [40.60231311292229, -74.37276546040472],
                [40.601148222969634, -74.38652224691327],
                [40.60305325778882, -74.38558183527515],
                [40.599819086274955, -74.38734984691337],
                [40.5979497594545, -74.38952853156866],
                [40.596697834211824, -74.37373860458592],
                [40.586290379177264, -74.37379620273289],
                [40.560101685502, -74.37742496038142]
            ]
            my_map = folium.Map(location=myAddress, zoom_start=12)
            for coordinate in coordinates:
                folium.CircleMarker(location=coordinate, radius=10, popup='Marker', fill=True).add_to(my_map)
            folium.CircleMarker(location=[latitude, longitude], radius=10, popup='Marker', fill=True, color='red').add_to(my_map)
            folium.PolyLine(locations=coordinates, color='red', weight=2.5).add_to(my_map)
            map_html = my_map._repr_html_()
        
        DriverLocation.objects.filter(user=request.user).delete()
        driver_location = DriverLocation(user=request.user, latitude=latitude, longitude=longitude)
        driver_location.save()

        template = loader.get_template("dashboard-all.html")
        context = {
            "map": map_html,
        }
        return HttpResponse(template.render(context, request))

def round_to_nearest_tenth(value):
    rounded_value = round(value, 1)
    return rounded_value

def calculate_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    radius = 3959.0

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radius * c
    time = distance * 6 
    rounded_time = round_to_nearest_tenth(time)
    print("It is " + str(rounded_time) + " minutes away.")

    return rounded_time

def dashboard_all(request):          
    import geocoder
    import folium
    import os
    import requests

    api_key = "prj_live_sk_54bbc5d2dbb79d8d947c533d799840609f208a2a"
    url = "https://api.radar.io/v1/geocode/ip"
    headers = {
    "Authorization": f"{api_key}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    # latitude = float(data["address"]["latitude"])
    # longitude = float(data["address"]["longitude"])

    ip_address = data["ip"]
    g = geocoder.ip(ip_address)

    latitude = g.latlng[0]
    longitude = g.latlng[1]


    location = f"{latitude},{longitude}"
    g = geocoder.osm(location)
    myAddress = g.latlng

    if myAddress is not None:
        coordinates = [
            [40.59109857762286, -74.36105823371278],
            [40.593202880468255, -74.36807433871225],
            [40.598626796900675, -74.37261624691347],
            [40.60231311292229, -74.37276546040472],
            [40.601148222969634, -74.38652224691327],
            [40.60305325778882, -74.38558183527515],
            [40.599819086274955, -74.38734984691337],
            [40.5979497594545, -74.38952853156866],
            [40.596697834211824, -74.37373860458592],
            [40.586290379177264, -74.37379620273289]
        ]
        my_map = folium.Map(location=myAddress, zoom_start=12)
        for coordinate in coordinates:
            folium.CircleMarker(location=coordinate, radius=10, popup='Marker', fill=True).add_to(my_map)
        folium.CircleMarker(location=[latitude, longitude], radius=10, popup='Marker', fill=True, color='red').add_to(my_map)
        driveruser = user.objects.filter(username="busdriver1").last()
        driver = DriverLocation.objects.filter(user=driveruser).first()
        folium.CircleMarker(location=[driver.latitude, driver.longitude], radius=10, popup='Marker', fill=True, color='green').add_to(my_map)
        folium.PolyLine(locations=coordinates, color='red', weight=2.5).add_to(my_map)
        map_html = my_map._repr_html_()

        # Calculate the time
        lat2, lon2 = coordinates[0][0], coordinates[0][1]
        time = calculate_distance(latitude, longitude, lat2, lon2)

        template = loader.get_template("dashboard-drivers.html")
        context = {
            "map": map_html,
            "time": time,  # Add the 'time' variable to the context
        }
        return HttpResponse(template.render(context, request))

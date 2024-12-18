import datetime
import glob
from django.shortcuts import redirect, render
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .AiModel import accPredict, conPredict, density, green_signal_time
from .forms import *
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import os
import random



# Views
def index(request):
    return render(request, 'traffic_light/index.html')

# Register a user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
         form = CreateUserForm(request.POST)
         if form.is_valid():
              form.save()
              return redirect('login')
    
    context = {'form': form}
    return render(request, 'traffic_light/register.html', context=context)

# Login 
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')            
    context = {'form': form}
    return render(request, 'traffic_light/login.html', context=context)

# Logout 
def logout(request):
    auth.logout(request)
    return redirect('login')

# Base HTML page
def base(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    return render(request, 'traffic_light/base.html', {
        first_name:first_name, last_name:last_name })

# Dashboard page
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'traffic_light/dashboard.html',{"first_name": request.user.first_name, "last_name": request.user.last_name})

# def display_traffic_information(request):
#     return render(request, 'traffic_light/traffic_info.html', 
#                   {"first_name": request.user.first_name, "last_name": request.user.last_name})

def get_traffic_information(request):
    if request.method == 'GET':
        image_path = process_random_image(request)
        accPrediction = accPredict(image_path)
        conPrediction = conPredict(image_path)
        is_accident = True if len(accPrediction[0].boxes.xyxy) > 0 else False
        number_of_vehicles = len(conPrediction[0].boxes.xyxy)
        traffic_density = density(number_of_vehicles)
        is_congestion = False if traffic_density == "Low" else True
        GLT = green_signal_time(number_of_vehicles)
        # Prepare the traffic information to be sent as a response
        traffic_info = {
            'is_accident': is_accident,
            'is_congestion': is_congestion,
            #'traffic_density': traffic_density,
            'new_green_light_time': GLT
        }
        return JsonResponse(traffic_info, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
def process_random_image(request):

    # Get the path to the directory containing the images
    image_dir = os.path.join(settings.BASE_DIR, 'traffic_light/TestImages')
    # Get a list of all image files in the directory
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]  
    # Select a random image file
    random_image_file = random.choice(image_files)
    image_path = os.path.join(image_dir, random_image_file)
    return image_path


def system_check(request):
    if request.method == 'POST':
        form2 = IncidentForm(request.POST)
        if form2.is_valid():
            form2.save()
            return HttpResponse('<h1>Hello World</h1>')
    else:
        form = IncidentForm()
        return render(request, 'traffic_light/system_check.html', {'form': form, 'first_name': request.user.first_name, 'last_name': request.user.last_name})
    

def predict_incident(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the image form
            image_instance = form.save()
            # Get the saved image path
            image_path = image_instance.image.path
            selected_choice = form.cleaned_data['choice_field']

            # Prepare the initial data for IncidentForm
            incident_data = {
                'IsAccident': 1 if selected_choice == 'Accident' else 0,
                'IsCongestion': 0 if selected_choice == 'Accident' else 1,
                'IntersectionID': 2,
                'Date': datetime.date.today(),
                'Time': datetime.datetime.now().time(),
                # Remove 'Image' field if it's not in the model
            }
            if selected_choice == 'Accident':
                # Pass the image to the models for prediction
                accPrediction = accPredict(image_path)
                is_accident = 1 if len(accPrediction[0].boxes.xyxy) > 0 else 0

                
                 # Update incident data based on prediction
                incident_data['IsAccident'] = is_accident
                incident_form = IncidentForm({**request.POST, **incident_data})
                print(incident_form.is_valid())
                print(incident_form.errors)
                # if incident_form.is_valid():
                    # Save the incident form
                    # incident_form.save()
               
                return render(request, 'traffic_light/prediction_result.html',
                              {'image_path': image_path, 'selected_choice': selected_choice,
                               'accPrediction': accPrediction[0], 'is_accident': is_accident,
                               'first_name': request.user.first_name, 'last_name': request.user.last_name})
            else:
                # Pass the image to the models for prediction
                conPrediction = conPredict(image_path)
                number_of_vehicles = len(conPrediction[0].boxes.xyxy)
                traffic_density = density(number_of_vehicles)
                # Save the form data to create a new Incident instance
                
                incident_form = IncidentForm({**request.POST, **incident_data})

                # if incident_form.is_valid():
                #     # Save the incident form
                #     incident_form.save()
                return render(request, 'traffic_light/prediction_result.html',
                              {'image_path': image_path, 'selected_choice': selected_choice,
                               'conPrediction': conPrediction[0], 'number_of_vehicles': number_of_vehicles,
                               'traffic_density': traffic_density, 'first_name': request.user.first_name,
                               'last_name': request.user.last_name})
        print(incident_form.errors)
    
    else:
        form = ImageForm()
    return render(request, 'traffic_light/predict.html', {'form': form, 'first_name': request.user.first_name,
                                                          'last_name': request.user.last_name})


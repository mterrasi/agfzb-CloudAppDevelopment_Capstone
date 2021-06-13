from requests.api import post
#path not working
#from server.djangoapp.models import CarModel
from .models import CarModel
#from server.djangoapp.restapis import get_dealer_reviews_from_cf, get_dealers_from_cf
from .restapis import get_dealer_reviews_from_cf, get_dealers_from_cf
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)

def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = 'Invalid username or password'
            return render(request, 'djangoapp/registration.html', context)
    else:
        return render(request, 'djangoapp/registration.html', context)

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.object.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = 'User already exists'
            return render(request, 'djangoapp/registration.html', context)

# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
#def contact(request):

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = 'https://5df47d1d.us-south.apigw.appdomain.cloud/dealership/dealer-get'
        dealerships = get_dealers_from_cf(url)
        context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == 'GET':
        url = 'https://5df47d1d.us-south.apigw.appdomain.cloud/review/review-get'
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context['reviews'] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
#@csrf_exempt
def add_review(request, dealer_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            review = {}
            form = request.POST
            review["name"] = request.user.username
            review["dealership"] = dealer_id
            review["review"] = form.get('content', '')
            if form.get('purchasecheck', 'off') == 'on':
                review["purchase"] = True
            else:
                review["purchase"] = False
            review["purchase_date"] = form.get('purchasedate', '01/01/1970')
            car = CarModel.objects.get(id=form.get('car', '1'))
            review["car_make"] = car.make.name
            review["car_model"] = car.model
            review["car_year"] = car.year.strftime("%Y")
            json_payload = {}
            json_payload["review"] = review
            url = ''
            response = post_request(url, json_payload, dealer_id=dealer_id)
            return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
        else:
            response = HttpResponse('You must authenticate')
            response.status_code = 401
            return response
    elif request.method == 'GET':
        context = {}
        url = ''
        cars = list(CarModel.objects.filter(dealer_id=dealer_id))
        context["cars"] = cars
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context["reviews"] = reviews
        return render(request, 'djangoapp/add_review.html', context)


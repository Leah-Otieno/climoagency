import json

import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from requests.auth import HTTPBasicAuth
from Agency.credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.contrib import messages
from django.contrib.auth.hashers import check_password



from Agency.models import Contact, Client



# Create your views here.
def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == "POST":
        contacts= Contact(
        name=request.POST["name"],
        email = request.POST["email"],
        subject = request.POST["subject"],
        message = request.POST["message"],
        )
        contacts.save()
        return redirect("contact")
    return render(request, "contact.html")


def agents(request):
    return render(request, "agents.html")

def properties(request):
    return render(request, "properties.html")

def property_single(request):
    return render(request, "property-single.html")

def services(request):
    return render(request, "services.html")

def service_details(request):
    return render(request, "service-details.html")

def starter(request):
    return render(request, "starter-page.html")

def register(request):
    if request.method == "POST":
        myclients=Client(
            name = request.POST["name"],
            email = request.POST["email"],
            password = request.POST["password"],
        )
        myclients.save()
        return redirect("login")
    return render(request, "register.html")

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password  # Use for verifying hashed passwords
from .models import Client  # Import the Client model

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Find the client using the email
        client = Client.objects.filter(email=email).first()

        if client:
            # Directly compare plaintext passwords
            if password == client.password:
                # Store email in the session
                request.session['client_email'] = client.email
                request.session['client_name'] = client.name  # Optional, for display purposes
                messages.success(request, f"Welcome, {client.name}!")
                return redirect('home')  # Replace 'home' with your dashboard URL
            else:
                messages.error(request, "Invalid password!", extra_tags="danger")
        else:
            messages.error(request, "Client with this email does not exist!", extra_tags="danger")

        return redirect('login')  # Redirect back to the login page on failure

    return render(request, 'login.html')

def pay(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullName')
        phone_number = request.POST.get('phone')
        amount = request.POST.get('amount')

        # Validate inputs
        if not full_name or not phone_number or not amount:
            messages.error(request, "All fields are required!")
            return redirect('pay')

        if not (phone_number.startswith('07') or phone_number.startswith('01')) or len(phone_number) != 10:
            messages.error(request, "Invalid phone number! Use format 07XXXXXXXX or 01XXXXXXXX")
            return redirect('pay')

        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, "Amount must be greater than 0!")
                return redirect('pay')
        except ValueError:
            messages.error(request, "Invalid amount! Please enter a valid number.")
            return redirect('pay')

        # Simulate payment processing or forward to Daraja API integration
        # Replace this block with actual Daraja API logic if needed
        messages.success(request, f"Payment request sent successfully for KES {amount} to {phone_number}.")
        return redirect('payment_success')  # Redirect to a success page

    return render(request, 'pay.html')  # Render the payment form template

def token(request):
    consumer_key = 'gRAX8gAaDTgyIsfe32wDpyDpw2FUJFXAMRVOJhVjWFhf2rVh'
    consumer_secret = 'ufGGHJl2X0hjKA1LaPd2sqWlGqDJyd2asKyEUCBvkgn7HgkF0AQRGJcaQXRzwGLu'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

# def pay(request):
#    return render(request, 'pay.html')



def stk(request):
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "eMobilis",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")
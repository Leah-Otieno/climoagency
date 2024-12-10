from django.contrib import admin
from Agency.models import Contact, Client, MPESAPayment

# Register your models here.
admin.site.register(Contact)
admin.site.register(Client)
admin.site.register(MPESAPayment)
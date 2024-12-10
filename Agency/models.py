from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(default="unknown@example.com")
    password = models.CharField(max_length=128)  # Use hashed passwords in practice

    def __str__(self):
        return self.name

from django.db import models

class MPESAPayment(models.Model):
    full_name = models.CharField(max_length=100)  # Name of the payer
    phone_number = models.CharField(max_length=10)  # Format: 07XXXXXXXX
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid
    transaction_code = models.CharField(max_length=20, blank=True, null=True)  # MPESA Transaction code
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')],
        default='Pending'
    )  # Payment status
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the payment was initiated
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the payment was updated

    def __str__(self):
        return f"{self.full_name} - {self.phone_number} - KES {self.amount}"







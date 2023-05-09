from django.db import models
from django.contrib.auth.models import User


class Loan(models.Model):
    id = models.AutoField(primary_key=True)
    nominal_value = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=4, decimal_places=2)
    ip_address = models.GenericIPAddressField()
    request_date = models.DateField(auto_now_add=True)
    bank = models.CharField(max_length=50)
    client = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        app_label = 'loans'

    def __str__(self):
        return f"{self.bank} - {self.id} - {self.client}"

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        app_label = 'loans'
        
    def __str__(self):
        return f"{self.loan} - {self.payment_date} - {self.value}"
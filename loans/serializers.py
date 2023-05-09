import datetime
from pyexpat import model
from rest_framework import serializers
from loans.models import Loan, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'loan', 'payment_date', 'value']

class LoanSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['id', 'nominal_value', 'interest_rate', 'ip_address', 'request_date', 'bank', 'client', 'payments', 'balance']

    def get_balance(self, obj):
        paid_value = obj.payments.aggregate(model.Sum('value'))['value__sum'] or 0
        interest_value = (obj.nominal_value * ((1 + obj.interest_rate/100) ** self._get_days(obj.request_date))) - obj.nominal_value
        return round(obj.nominal_value + interest_value - paid_value, 2)

    def _get_days(self, request_date):
        return (self.context['request'].data.get('payment_date', datetime.today()) - request_date).days

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from decimal import Decimal

from .models import Emprestimo, Pagamento
from django.contrib.auth.models import User
from datetime import datetime


class TestEmprestimo(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_criar_emprestimo(self):
        url = reverse('emprestimo-list')
        data = {
            'valor_nominal': Decimal('1000.00'),
            'taxa_juros': Decimal('0.01'),
            'endereco_ip': '192.168.0.1',
            'data_solicitacao': datetime.now(),
            'banco': 'Banco do Brasil',
            'cliente': 'Fulano'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        emprestimo = Emprestimo.objects.get(id=response.data['id'])
        self.assertEqual(emprestimo.valor_nominal, Decimal('1000.00'))

    def test_listar_emprestimos(self):
        emprestimo = Emprestimo.objects.create(
            valor_nominal=Decimal('1000.00'),
            taxa_juros=Decimal('0.01'),
            endereco_ip='192.168.0.1',
            data_solicitacao=datetime.now(),
            banco='Banco do Brasil',
            cliente='Fulano'
        )
        url = reverse('emprestimo-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], emprestimo.id)

    def test_atualizar_emprestimo(self):
        emprestimo = Emprestimo.objects.create(
            valor_nominal=Decimal('1000.00'),
            taxa_juros=Decimal('0.01'),
            endereco_ip='192.168.0.1',
            data_solicitacao=datetime.now(),
            banco='Banco do Brasil',
            cliente='Fulano'
        )
        url = reverse('emprestimo-detail', args=[emprestimo.id])
        data = {
            'valor_nominal': Decimal('1500.00')
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        emprestimo.refresh_from_db()
        self.assertEqual(emprestimo.valor_nominal, Decimal('1500.00'))

    def test_deletar_emprestimo(self):
        emprestimo = Emprestimo.objects.create(
            valor_nominal=Decimal('1000.00'),
            taxa_juros=Decimal('0.01'),
            endereco_ip='192.168.0.1',
            data_solicitacao=datetime.now(),
            banco='Banco do Brasil',
            cliente='Fulano'
        )
        url = reverse('emprestimo-detail', args=[emprestimo.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Emprestimo.objects.filter(id=emprestimo.id).count(), 0)

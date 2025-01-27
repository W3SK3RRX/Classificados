from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from contratos.models import Contrato

User = get_user_model()

class ContratoAPITestCase(APITestCase):
    def setUp(self):
        # Criação de usuários e contrato de teste
        self.cliente = User.objects.create_user(email="cliente@example.com", password="password123")
        self.profissional = User.objects.create_user(email="pro@example.com", password="password123")
        self.contract_url = "/contratos/"
        self.client.login(email="cliente@example.com", password="password123")

    def test_create_contrato(self):
        # Testa a criação de um contrato
        data = {
            "profissional": self.profissional.id,
            "descricao": "Contrato para desenvolvimento de website",
            "valor": 5000.0,
            "prazo_entrega": "2025-02-15",
            "tipo_modelo": "pre_definido",
        }
        response = self.client.post(self.contract_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["descricao"], "Contrato para desenvolvimento de website")

    def test_listar_contratos(self):
        # Testa a listagem de contratos do cliente
        Contrato.objects.create(
            cliente=self.cliente,
            profissional=self.profissional,
            descricao="Contrato para design gráfico",
            valor=2000.0,
            prazo_entrega="2025-02-10",
            tipo_modelo="pre_definido",
        )
        response = self.client.get(self.contract_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

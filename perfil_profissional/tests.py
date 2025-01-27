from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from perfil_profissional.models import PerfilProfissional, Endereco
from contratos.models import Contrato
from datetime import date

User = get_user_model()

class ContratoAPITestCase(TestCase):
    def setUp(self):
        # Criar usuários
        self.cliente = User.objects.create_user(
            email="cliente@example.com",
            password="cliente123",
            name="Cliente",
            lastname="Teste",
            user_type=User.INDIVIDUAL
        )

        self.profissional = User.objects.create_user(
            email="profissional@example.com",
            password="profissional123",
            name="Profissional",
            lastname="Teste",
            user_type=User.PROFESSIONAL
        )

        # Criar endereço e perfil profissional
        self.endereco = Endereco.objects.create(
            rua="Rua A",
            numero="123",
            bairro="Bairro B",
            cidade="Cidade C",
            estado="SP",
            cep="12345-678"
        )

        self.perfil_profissional = PerfilProfissional.objects.create(
            user=self.profissional,
            endereco=self.endereco,
            profile_name="Profissional Teste",
            telefone="(11) 98765-4321",
            area_atuacao="Consultoria",
            cpf="123.456.789-09",
        )

        # Configurar cliente da API
        self.client = APIClient()

    def test_create_contrato(self):
        # Logar cliente
        self.client.force_authenticate(user=self.cliente)

        data = {
            "contratante": str(self.cliente.id),
            "contratado": self.perfil_profissional.id,
            "descricao": "Serviço de consultoria.",
            "valor": "500.00",
            "prazo_execucao": date.today().strftime("%Y-%m-%d"),
        }

        response = self.client.post("/api/contratos/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contrato.objects.count(), 1)

    def test_list_contratos(self):
        # Criar contrato
        Contrato.objects.create(
            contratante=self.cliente,
            contratado=self.perfil_profissional,
            descricao="Serviço de exemplo.",
            valor="300.00",
            prazo_execucao=date.today()
        )

        # Logar cliente
        self.client.force_authenticate(user=self.cliente)

        response = self.client.get("/api/contratos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_contrato(self):
        contrato = Contrato.objects.create(
            contratante=self.cliente,
            contratado=self.perfil_profissional,
            descricao="Serviço de exemplo.",
            valor="300.00",
            prazo_execucao=date.today()
        )

        # Logar cliente
        self.client.force_authenticate(user=self.cliente)

        response = self.client.get(f"/api/contratos/{contrato.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["descricao"], "Serviço de exemplo.")

    def test_update_contrato(self):
        contrato = Contrato.objects.create(
            contratante=self.cliente,
            contratado=self.perfil_profissional,
            descricao="Serviço de exemplo.",
            valor="300.00",
            prazo_execucao=date.today()
        )

        # Logar cliente
        self.client.force_authenticate(user=self.cliente)

        data = {
            "descricao": "Serviço atualizado.",
            "valor": "400.00",
        }

        response = self.client.patch(f"/api/contratos/{contrato.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contrato.refresh_from_db()
        self.assertEqual(contrato.descricao, "Serviço atualizado.")
        self.assertEqual(str(contrato.valor), "400.00")

    def test_delete_contrato(self):
        contrato = Contrato.objects.create(
            contratante=self.cliente,
            contratado=self.perfil_profissional,
            descricao="Serviço de exemplo.",
            valor="300.00",
            prazo_execucao=date.today()
        )

        # Logar cliente
        self.client.force_authenticate(user=self.cliente)

        response = self.client.delete(f"/api/contratos/{contrato.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contrato.objects.count(), 0)

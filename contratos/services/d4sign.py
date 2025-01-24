import requests
from django.conf import settings

class D4SignService:
    BASE_URL = settings.D4SIGN_API_URL
    API_KEY = settings.D4SIGN_API_KEY
    CRYPTO_KEY = settings.D4SIGN_CRYPTO_KEY

    @staticmethod
    def create_document(file_path, document_name, safe_key):
        """
        Envia o arquivo para o D4Sign e cria um documento no cofre especificado.
        """
        url = f"{D4SignService.BASE_URL}/documents/{safe_key}?apikey={D4SignService.API_KEY}"
        files = {'file': (document_name, open(file_path, 'rb'))}
        data = {'name': document_name}

        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def add_signers(document_key, signers):
        """
        Adiciona signatários ao documento.
        """
        url = f"{D4SignService.BASE_URL}/documents/{document_key}/remote?apikey={D4SignService.API_KEY}&cryptKey={D4SignService.CRYPTO_KEY}"
        response = requests.post(url, json=signers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def generate_sign_url(document_key, signer_key):
        """
        Gera um link para o signatário assinar o documento.
        """
        url = f"{D4SignService.BASE_URL}/documents/{document_key}/url?apikey={D4SignService.API_KEY}&cryptKey={D4SignService.CRYPTO_KEY}"
        response = requests.post(url, json={'key_signer': signer_key})
        response.raise_for_status()
        return response.json()

import os
import re
import logging
from base64 import b64encode
from os.path import basename
from requests import post
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Whats77:
    COUNTRY_CODE = "55"
    EXPECTED_LENGTH_NUMBER = 11
    STATE_NUMBER = '9'
    WHATSAPP_NUMBER_PATTERN = r'^55\d{11}$|^\d{12}$'

    SEND_TEXT = "/send-text"
    SEND_AUDIO = "/send-audio"
    SEND_DOCUMENT = "/send-document"

    def __init__(self, instance_id=None, token=None, security_token=None):
        """
        Inicializa as credenciais e a URL base da API do WhatsApp.
        As credenciais podem ser fornecidas diretamente ou carregadas do .env.

        Args:
            instance_id (str): ID da instância da API.
            token (str): Token de autenticação.
            security_token (str): Token de segurança opcional.
        """
        load_dotenv()
        self.instance_id = instance_id or os.getenv("INSTANCE_ID")
        self.token = token or os.getenv("TOKEN")
        self.security_token = security_token or os.getenv("SECURITY_TOKEN")
        self.base_url_api = None
        self._validate_credentials()
        self._set_base_url_api()

    def _validate_credentials(self):
        """Valida as credenciais obrigatórias."""
        if not self.instance_id:
            raise ValueError("O 'instance_id' não foi configurado.")
        if not self.token:
            raise ValueError("O 'token' não foi configurado.")

    def _set_base_url_api(self):
        """Configura a URL base da API do WhatsApp."""
        self.base_url_api = f"https://api.z-api.io/instances/{self.instance_id}/token/{self.token}"
        logger.info(f"Base URL configurada: {self.base_url_api}")

    @staticmethod
    def normalize_phone_number(number: str) -> str:
        """Normaliza o número de telefone para o formato padrão."""
        clean_number = re.sub(r'\D', '', number)

        if len(clean_number) == 10:
            clean_number = Whats77.STATE_NUMBER + clean_number
        elif len(clean_number) == Whats77.EXPECTED_LENGTH_NUMBER and not clean_number.startswith(Whats77.COUNTRY_CODE):
            clean_number = Whats77.COUNTRY_CODE + clean_number

        return clean_number

    @staticmethod
    def is_valid_whatsapp_number(number: str) -> bool:
        """Verifica se o número é válido para WhatsApp."""
        return re.match(Whats77.WHATSAPP_NUMBER_PATTERN, number) is not None

    def send_text(self, phone_number: str, message: str) -> None:
        """Envia uma mensagem de texto."""
        url = f"{self.base_url_api}{self.SEND_TEXT}"
        payload = {"phone": phone_number, "message": message}
        self._send_request(url, payload)

    def send_audio(self, phone_number: str, base64_audio: str) -> None:
        """Envia um áudio codificado em Base64."""
        url = f"{self.base_url_api}{self.SEND_AUDIO}"
        payload = {"phone": phone_number, "audio": base64_audio}
        self._send_request(url, payload)

    @staticmethod
    def parse_to_base64(file_path: str) -> str:
        """Converte um arquivo para Base64."""
        with open(file_path, 'rb') as file:
            return b64encode(file.read()).decode()

    def send_document(self, phone_number: str, file_path: str, document_type: str = 'pdf', caption: str = None) -> None:
        """Envia um documento."""
        file_name = basename(file_path)
        base64_file = self.parse_to_base64(file_path)
        payload = {
            'phone': phone_number,
            'document': f"data:application/{document_type};base64,{base64_file}",
            'fileName': file_name,
            'caption': caption
        }

        url = f"{self.base_url_api}{self.SEND_DOCUMENT}/{document_type}"
        self._send_request(url, payload)

    def _send_request(self, url: str, payload: dict) -> None:
        """Envia uma requisição HTTP para a API do WhatsApp."""
        headers = {'Client-Token': self.security_token}
        try:
            response = post(url, json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"Envio para {payload.get('phone')} bem-sucedido: {response.json()}")
        except Exception as e:
            logger.error(f"Erro ao enviar para {payload.get('phone')}: {e}")

# Exemplo de uso
def main():
    try:
        # Configurar autenticação dinamicamente ou via .env
        whatsapp = Whats77()

        # Exemplo de envio de texto
        whatsapp.send_text("+5511999999999", "Olá, isso é um teste!")

        # Exemplo de envio de documento
        whatsapp.send_document(
            phone_number="+5511999999999",
            file_path="/caminho/para/arquivo.pdf",
            document_type="pdf",
            caption="Segue o relatório em anexo."
        )

    except Exception as e:
        logger.error(f"Erro no envio: {e}")

if __name__ == "__main__":
    main()

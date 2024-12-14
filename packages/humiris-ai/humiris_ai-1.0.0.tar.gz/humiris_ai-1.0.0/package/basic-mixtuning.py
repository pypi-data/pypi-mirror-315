import requests

class MessageType:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

class UseMixtuningPayload:
    def __init__(self, mix_tuning_id: str, messages: list, temperature: float, max_tokens: int):
        self.mix_tuning_id = mix_tuning_id
        self.messages = messages
        self.temperature = temperature
        self.max_tokens = max_tokens

class MoAi:
    def __init__(self, api_key: str):
        self.api_url = 'https://moai-service-app.humiris.ai/api/api-key-operators/use-basic-mixtuning'
        self.api_key = api_key

    def use_basic_mixtuning(self, payload: UseMixtuningPayload):
        headers = {
            'moai-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(self.api_url, json=vars(payload), headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            raise Exception(f"Failed to send request: {error}")


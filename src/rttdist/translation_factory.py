"""Bridge the legacy typed translation interface to the common provider API."""
from pathlib import Path
import uuid
from rttdist.providers import create_provider
from rttdist.lmstudio_client import LMStudioTranslationClient

def provider_config(config):
    common=dict(config.llm or {})
    generation=dict(common.get('generation',{'temperature':config.lmstudio.temperature}))
    if config.lmstudio.max_tokens is not None:generation.setdefault('max_tokens',config.lmstudio.max_tokens)
    return {'provider':config.provider,'endpoint':common.get('endpoint',config.lmstudio.host),
            'model':common.get('model',config.lmstudio.model),'generation':generation,
            'api_key_env':common.get('api_key_env'),'request_timeout':common.get('request_timeout',300),
            'retries':common.get('retries',0)}

class ProviderChatTransport:
    def __init__(self, config):
        self.settings=provider_config(config)
        self.provider=create_provider(self.settings)
        self.output_root=Path(config.output_root)/'provider_requests'

    def create_chat_completion(self,payload):
        wire={'model':payload['model'],'messages':payload['messages'],'stream':False,
              **self.settings['generation']}
        # Every logical legacy call has a separate ledger. The outer runner owns
        # step replay; identical text on a later step still represents a new call.
        return self.provider.complete(wire,self.output_root/uuid.uuid4().hex)['body']

def create_translation_client(config):
    return LMStudioTranslationClient(model=config.lmstudio.model,
            temperature=config.lmstudio.temperature,host=config.lmstudio.host,
            prompt_template_version=config.prompt_template_version,
            transport=ProviderChatTransport(config),provider_name=config.provider)

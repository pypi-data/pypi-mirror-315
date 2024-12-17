import os
from typing import Optional

import toml
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI as LangChainChatOpenAI, OpenAIEmbeddings as LangChainOpenAIEmbeddings, AzureOpenAIEmbeddings as LangChainAzureEmbeddings,AzureChatOpenAI as LangChainAzureChatOpenAI
from langchain_community.embeddings import DashScopeEmbeddings as LangChainDashScopeEmbeddings
from pydantic import BaseModel
from importlib import resources


class CustomAttract(BaseModel):
    doc_url: Optional[str] = ''
    provider: Optional[str] = ''


class ChatOpenAI(LangChainChatOpenAI, CustomAttract):
    pass


class OpenAIEmbeddings(LangChainOpenAIEmbeddings, CustomAttract):
    pass


class DashScopeEmbeddings(LangChainDashScopeEmbeddings, CustomAttract):
    pass

class AzureOpenAIEmbeddings(LangChainAzureEmbeddings, CustomAttract):
    pass

class AzureChatOpenAI(LangChainAzureChatOpenAI, CustomAttract):
    pass

class BaseLLM:
    @classmethod
    def load_config(cls, config_dir: str = None, env_file: str = '.env'):
        # Use provided directory or current working directory
        working_dir = config_dir or os.getcwd()
        local_path = os.path.join(working_dir, 'model_providers.toml')
        env_path = os.path.join(working_dir, env_file)
        
        # Try to load from specified/current directory
        if os.path.exists(local_path):
            if os.path.exists(env_path):
                load_dotenv(env_path,override=True)
            else:
                # Create env file from template if it doesn't exist
                try:
                    with resources.files('init_llm').joinpath('.env.template').open('rb') as f:
                        env_template = f.read()
                    
                    os.makedirs(working_dir, exist_ok=True)
                    with open(env_path, 'wb') as f:
                        f.write(env_template)
                    
                    print(f"Created {env_file} in {working_dir}")
                    load_dotenv(env_path,override=True)
                except Exception as e:
                    print(f"Warning: Could not create {env_file}. Error: {str(e)}")
                    load_dotenv()
            return toml.load(local_path)
        
        # If not found, create from package resources
        try:
            with resources.files('init_llm').joinpath('model_providers.toml').open('rb') as f:
                config_content = f.read()
                
            # Create model_providers.toml in the working directory
            os.makedirs(working_dir, exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(config_content)
                
            print(f"Created model_providers.toml in {working_dir}")
            
            # Create env file if it doesn't exist
            if not os.path.exists(env_path):
                try:
                    with resources.files('init_llm').joinpath('.env.template').open('rb') as f:
                        env_template = f.read()
                    
                    with open(env_path, 'wb') as f:
                        f.write(env_template)
                    
                    print(f"Created {env_file} in {working_dir}")
                except Exception as e:
                    print(f"Warning: Could not create {env_file}. Error: {str(e)}")
            
            load_dotenv(env_path,override=True)
            return toml.loads(config_content.decode('utf-8'))
            
        except Exception as e:
            raise FileNotFoundError(
                "Failed to load or create model_providers.toml. "
                f"Error: {str(e)}"
            ) from e

    @classmethod
    def get_provider_details(cls, config, model_name, config_type):
        for provider in config['providers']['names']:
            provider_config = config.get(provider)
            models = provider_config.get(config_type, [])
            if model_name == provider or model_name in models:
                model_name = models[0] if model_name == provider else model_name
                base_url = provider_config.get('base_url')
                api_key = os.getenv(provider.upper() + '_API_KEY')
                if not api_key:
                    raise ValueError(f"API key for {provider} not found in environment variables")
                return provider, model_name, base_url, api_key, provider_config.get('doc_url', '')

        raise ValueError(f"Unsupported model_name: {model_name}")



class ChatLLM(BaseLLM):
    def __new__(cls, model_name, temperature=0.1, **kwargs):
        config_dir = kwargs.pop('config_dir', None)
        env_file = kwargs.pop('env_file', '.env')
        config = cls.load_config(config_dir=config_dir, env_file=env_file)
        provider, model_name, base_url, api_key, doc_url = cls.get_provider_details(config, model_name, 'models')

        if provider=='azure':
            instance = AzureChatOpenAI(
                azure_deployment=model_name,
                azure_endpoint=base_url,
                api_version='2024-02-15-preview',
                openai_api_key=api_key,
                temperature=temperature,
                **kwargs
            )
            instance.model_name = model_name
        else:
            instance = ChatOpenAI(
                model=model_name,
                openai_api_base=base_url,
                openai_api_key=api_key,
                temperature=temperature,
                **kwargs
            )
        instance.provider = provider
        instance.doc_url = doc_url
        return instance



class EmbeddingLLM(BaseLLM):
    def __new__(cls, model_name, temperature=0.1, **kwargs):
        config_dir = kwargs.pop('config_dir', None)
        env_file = kwargs.pop('env_file', '.env')
        config = cls.load_config(config_dir=config_dir, env_file=env_file)
        provider, model_name, base_url, api_key, doc_url = cls.get_provider_details(config, model_name, 'embeddings')

        if provider in ['openai', 'zhipu']:
            instance = OpenAIEmbeddings(
                model=model_name,
                openai_api_base=base_url,
                openai_api_key=api_key,
            )
        elif provider == 'qwen':
            instance = DashScopeEmbeddings(
                model=model_name,
                dashscope_api_key=api_key,
                **kwargs
            )
        elif provider == 'azure':
            instance = AzureOpenAIEmbeddings(
                model=model_name,
                azure_endpoint=base_url,
                api_version='2024-02-01',
                openai_api_key=api_key,
            )
        else:
            instance = OpenAIEmbeddings(
                model=model_name,
                openai_api_base=base_url,
                openai_api_key=api_key,
            )

        instance.provider = provider
        instance.doc_url = doc_url
        return instance

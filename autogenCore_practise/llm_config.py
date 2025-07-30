from autogen_ext.models.openai import AzureOpenAIChatCompletionClient,OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()
class LLMConfig:
    model_client = AzureOpenAIChatCompletionClient(
        model=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
        model_info={
        "family": "gpt-4",
        "vision": True,
        "function_calling": True,
        "json_output": True,
        "structured_output": True
    },
        default_params={
        "temperature": 0,
        "seed": 42
    },
    # ✅ Add retry configuration
        max_retries=3,
        timeout=30.0
        ) 
    

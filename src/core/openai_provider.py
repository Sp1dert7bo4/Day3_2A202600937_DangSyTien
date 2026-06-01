import os
import time
from typing import Dict, Any, Optional, Generator
from openai import OpenAI
from dotenv import load_dotenv
from src.core.llm_provider import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self, model_name: str = "gpt-4o", api_key: Optional[str] = None, base_url: Optional[str] = None):
        load_dotenv()
        provider = os.getenv("DEFAULT_PROVIDER", "openai").lower()
        
        # Determine the appropriate API key and base URL
        if api_key is None:
            if provider == "mimo":
                api_key = os.getenv("MIMO_API_KEY")
            elif provider == "deepseek":
                api_key = os.getenv("DEEPSEEK_API_KEY")
            else:
                api_key = os.getenv("OPENAI_API_KEY")
        
        if base_url is None:
            if provider == "mimo":
                base_url = os.getenv("MIMO_BASE_URL")
            elif provider == "deepseek":
                base_url = os.getenv("DEEPSEEK_BASE_URL")
            else:
                base_url = os.getenv("OPENAI_BASE_URL")

        super().__init__(model_name, api_key)
        
        if base_url:
            self.client = OpenAI(api_key=self.api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        start_time = time.time()
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            timeout=120.0,
            max_tokens=1200,
        )

        end_time = time.time()
        latency_ms = int((end_time - start_time) * 1000)

        # Extraction from OpenAI response
        content = response.choices[0].message.content
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }

        return {
            "content": content,
            "usage": usage,
            "latency_ms": latency_ms,
            "provider": "openai"
        }

    def stream(self, prompt: str, system_prompt: Optional[str] = None) -> Generator[str, None, None]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            if chunk.choices and len(chunk.choices) > 0:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

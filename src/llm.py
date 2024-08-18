import json
import time
from dataclasses import dataclass
from ollama import Client


@dataclass
class ModelConfig:
    """A simple dataclass for holding model configuration."""
    name: str
    model_name: str
    system_prompt: str


class LLM:
    def __init__(self, url: str | None, config_name: str):
        self.client = Client(host=url) if url else None
        self.context = None
        self.model_config: ModelConfig = self.load_config(config_name)

    @staticmethod
    def load_config(name: str) -> ModelConfig:
        """Load the JSON configuration file into memory."""
        with open('llm_config.json', 'r') as f:
            config_data = json.load(f)
            model_configs = {model["name"]: ModelConfig(**model) for model in config_data}
            return model_configs.get(name)

    def send_to_llm(self, chunk: str) -> str:
        if self.client is None:
            return chunk
        if not chunk or chunk.isspace():
            return chunk
        response = self.client.generate(model=self.model_config.model_name, prompt=chunk,
                                        system=self.model_config.system_prompt, context=self.context, keep_alive=0,
                                        options={'num_predict': -1})
        time.sleep(1)
        if response["done_reason"] != "stop":
            print("Error in processing by LLM. Stop Reason: "+response["done_reason"])
            print("Chunk:")
            print(chunk)
            print("Response:")
            print(response)
            raise Exception("Error in processing by LLM")
        self.context = response["context"] if "context" in response else None
        return response['response']

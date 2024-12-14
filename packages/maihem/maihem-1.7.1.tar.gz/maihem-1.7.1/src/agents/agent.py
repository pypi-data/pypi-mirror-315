import os
from openai import AzureOpenAI, AsyncAzureOpenAI, AsyncOpenAI


class Agent:

    def __init__(self, instruction_prompt: str, temperature: float = 0.6):
        self.instruction_prompt = instruction_prompt
        self.temperature = temperature
        self.messages = [{"role": "system", "content": instruction_prompt}]

    def chat(self, message: str) -> str:

        if message:
            self.messages.append({"role": "user", "content": message})
            response = self.__llm_call_azure()
        else:
            response = "Hi, how can I help you?"
        self.messages.append({"role": "assistant", "content": response})
        return response

    async def achat(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})
        response = await self.__async_llm_call_azure()
        self.messages.append({"role": "assistant", "content": response})
        return response

    def __llm_call_azure(self):
        """
        Call the Azure OpenAI API asynchronously with a single prompt.
        Returns a completion for the prompt.
        """
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-05-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )

        response = client.chat.completions.create(
            model="maihem-gpt4o",  # deployment_name
            messages=self.messages,
            temperature=self.temperature,
        )

        response_msg = response.choices[0].message.content

        return response_msg

    async def __async_llm_call_azure(self):
        """
        Call the Azure OpenAI API asynchronously with a single prompt.
        Returns a completion for the prompt.
        """
        client = AsyncAzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-05-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )

        response = await client.chat.completions.create(
            model="maihem-gpt4o",  # deployment_name
            messages=self.messages,
            temperature=self.temperature,
        )

        response_msg = response.choices[0].message.content

        return response_msg

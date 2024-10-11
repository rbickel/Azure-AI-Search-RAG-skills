
from openai import AzureOpenAI

class OpenAIClient:
    def __init__(self, openai_key, openai_endpoint, openai_gpt4_deployment):
        self.openai_key = openai_key
        self.openai_endpoint = openai_endpoint
        self.openai_gpt4_deployment = openai_gpt4_deployment

        # Create the AzureOpenAI client
        self.client = AzureOpenAI(
            api_key=self.openai_key,
            api_version="2023-12-01-preview",
            azure_endpoint=self.openai_endpoint
        )

    def call_openai(self, sytem_prompt, user_input):
        response = self.client.chat.completions.create(
            model=self.openai_gpt4_deployment,
            messages=[
                {"role": "system", "content": [{"type": "text", "text": sytem_prompt}]},
                {"role": "user", "content": [{"type": "text", "text": user_input}]},
            ],
            max_tokens=4096,
            temperature=0,
            top_p=0
        )
        return response.choices[0].message.content

    def create_vectors(self, openai_embedding_deployment, text):
        response = self.client.embeddings.create(
            input=text,
            model=openai_embedding_deployment
        )
        return response.data[0].embedding

    def describe_image(self, sytem_prompt, base64image):
        response = self.client.chat.completions.create(
            model=self.openai_gpt4_deployment,
            messages=[
                {"role": "system", "content": [{"type": "text", "text": sytem_prompt}]},
                {
                    "role": "user", "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url":  f"data:image/jpeg;base64,{base64image}"
                            }
                        }
                    ]
                },
            ],
            max_tokens=4096,
            temperature=0,
            top_p=0
        )
        return response.choices[0].message.content
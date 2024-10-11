import azure.functions as func
import logging
from openai_client import OpenAIClient
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="image_ai_description")
def image_ai_description(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    image = req_body['values'][0]['data']['image']['data']
    image_url = req_body['values'][0]['data']['image']['url']
    record_id = req_body['values'][0]['recordId']
    logging.info(f"Processing image: {image_url}")
    
    azure_openai_endpoint_url = os.environ['AZURE_OPENAI_ENDPOINT_URL']
    azure_openai_key = os.environ['AZURE_OPENAI_KEY']
    azure_openai_model_id = os.environ['AZURE_OPENAI_MODEL_ID']
    prompt = os.environ['AZURE_OPENAI_PROMPT']
    
    logging.info(f"Calling OpenAI")
    openai_client = OpenAIClient(
        openai_key=azure_openai_key,
        openai_endpoint=azure_openai_endpoint_url,
        openai_gpt4_deployment=azure_openai_model_id
    )
    
    desc = openai_client.describe_image(prompt, image)
    logging.info(f"Image description: {desc}")
    response = "{\"values\":[{ \"recordId\": \"%s\", \"data\":{\"description\":\"%s\"} }]}" % (record_id, desc.replace('"', '\\"'))
    logging.info(response)
    return func.HttpResponse(response, status_code=200, mimetype='application/json')

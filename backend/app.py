from fastapi import FastAPI, Response, Request, Query
import requests
import uvicorn
import redis
import logging
import os
from pydantic import BaseModel, Field
from typing import Optional, List

LLM_NAME = os.environ.get("LLM_NAME", "llama3.2:1b")
LLM_HOST_NAME = os.environ.get("LLM_HOST_NAME", "localhost")
LLM_PORT = os.environ.get("LLM_PORT", 11434)
REDIS_HOST_NAME = os.environ.get("REDIS_HOST_NAME", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)

redis_client = redis.Redis(host=REDIS_HOST_NAME, port=REDIS_PORT) # Initialize Redis client for caching
app = FastAPI() # Initialize FastAPI instance

# Logging
logging_dir = os.path.join("data", "logs")
os.makedirs(logging_dir, exist_ok=True)
log_file_name = 'Backend_API.log'
logging.basicConfig(
    level=logging.INFO,
    filename=os.path.join(logging_dir, log_file_name),
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Define a simple data model
class Item(BaseModel):
    name: str = Field(default='LLM model')
    description: str = Field(default='Welcome to the LLM model...!!!')

# Define a route that uses the model for validation
@app.get('/', description="Landing page.")
async def landing():
    # Access validated data in item
    response = Item()
    logging.info(f"API has been successfully started.")
    return response.json()

@app.post('/ask', description="Ask a question to the LLM model.")
async def ask_question(prompt: str):
    key = f"prompt:{prompt}"
    
    try:
        # Check if the response is already cached in Redis
        cached_response = redis_client.get(key)
        
        if cached_response:
            st = cached_response.decode('utf-8')
            return {"response": st}
        
        # Make a POST request to the LLM API
        res = requests.post(f'http://{LLM_HOST_NAME}:{LLM_PORT}/api/generate', json={
            "prompt": prompt,
            "stream": False,
            "model": LLM_NAME
        })

        # Log the request details
        logging.info(f"Request to {res.url} with status code {res.status_code}")
        
        if res.status_code == 200:
            result = res.json()

            # Log the request details for model name, tokens and duration
            logging.info(f"Time: {result.get('created_at', 0)}, Model: {result.get('model', 'Unknown')}, Tokens: {result.get('prompt_eval_count', 0)}, Response Tokens: {result.get('eval_count', 0)}, Duration: {result.get('total_duration', 0)} seconds")
            
            """
            dict_keys(['model', 'created_at', 'response', 'done', 'done_reason', 'context', 'total_duration', 
            'load_duration', 'prompt_eval_count', 'prompt_eval_duration', 'eval_count', 'eval_duration'])
            ----------
            total_duration: time spent generating the response
            load_duration: time spent in nanoseconds loading the model
            prompt_eval_count: number of tokens in the prompt
            prompt_eval_duration: time spent in nanoseconds evaluating the prompt
            eval_count: number of tokens in the response
            eval_duration: time in nanoseconds spent generating the response
            context: an encoding of the conversation used in this response, this can be sent in the next request to keep a conversational memory
            response: empty if the response was streamed, if not streamed, this will contain the full response
            """
            
            result = result.get("response", "No response")
            redis_client.set(key, result.encode('utf-8')) # Store the response in Redis
            return {"response": result}
        
        else:
            logging.error(f"Request failed with status code {res.status_code}")
            return {"error": f"Request failed with status code {res.status_code}"}
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app="app:app", host='0.0.0.0', port=8000, reload=True)
    # uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
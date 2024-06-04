import httpx
import json
from fastapi import FastAPI
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from models import BillingRequest

class ServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.Client(base_url=self.base_url)

    def call_service(self, endpoint: str) -> str:
        response = self.client.get(endpoint)
        response.raise_for_status()
        return response.text
    
    def call_service_post(self, endpoint: str, data: dict) -> str:
        response = self.client.post(endpoint, json=data)
        response.raise_for_status()
        return response.text

class OrchestrationService:
    def __init__(self, service_clients: List[ServiceClient]):
        self.service_clients = service_clients

    def orchestrate(self, data:dict) -> dict:
        result1 = self.service_clients[0].call_service_post("/make-billing", data)
        # Process result1 and call next service
        # result2 = self.service_clients[1].call_service("/api/endpoint2")
        # Continue orchestration logic
        # return f"Result1: {result1}, Result2: {result2}"
        return {"result1":json.loads(result1)}

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service clients
service_client1 = ServiceClient(base_url="http://127.0.0.1:8001")
# service_client2 = ServiceClient(base_url="http://example-service2")

# Initialize orchestration service
# orchestration_service = OrchestrationService(service_clients=[service_client1, service_client2])
orchestration_service = OrchestrationService(service_clients=[service_client1])

@app.options("/orchestrate-get-billing")
def options():
    return 200
@app.post("/orchestrate-get-billing")
def start_orchestration(billingReq: dict):
    result = orchestration_service.orchestrate(data=billingReq) 
    return {"message": "Orchestration started", "results": result}

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
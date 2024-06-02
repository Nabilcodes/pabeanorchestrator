import httpx
from fastapi import FastAPI
from typing import List

class ServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.Client(base_url=self.base_url)

    def call_service(self, endpoint: str) -> str:
        response = self.client.get(endpoint)
        response.raise_for_status()
        return response.text

class OrchestrationService:
    def __init__(self, service_clients: List[ServiceClient]):
        self.service_clients = service_clients

    def orchestrate(self) -> str:
        result1 = self.service_clients[0].call_service("/api/endpoint1")
        # Process result1 and call next service
        result2 = self.service_clients[1].call_service("/api/endpoint2")
        # Continue orchestration logic
        return f"Result1: {result1}, Result2: {result2}"

app = FastAPI()

# Initialize service clients
service_client1 = ServiceClient(base_url="http://example-service1")
service_client2 = ServiceClient(base_url="http://example-service2")

# Initialize orchestration service
orchestration_service = OrchestrationService(service_clients=[service_client1, service_client2])

@app.get("/start-orchestration")
def start_orchestration():
    result = orchestration_service.orchestrate()
    return {"message": "Orchestration started", "result": result}

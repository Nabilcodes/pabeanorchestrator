from pydantic import BaseModel

class BillingRequest(BaseModel):
    billed_name : str
    billed_email : str
    value : int
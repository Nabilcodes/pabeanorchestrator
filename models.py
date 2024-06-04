from pydantic import BaseModel

class BillingRequest(BaseModel):
    billed_name : str
    billed_email : str
    nilai_fob : int
    nilai_pabean : int
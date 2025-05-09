from pydantic import BaseModel

class TransactionCreate(BaseModel):
    description: str
    amount: float
    category: str
    date: str
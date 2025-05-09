from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Base, Transaction, engine, SessionLocal
from schemas import TransactionCreate
from utils import analyze_transactions_with_gpt
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS for frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/transactions/")
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/analysis/")
def get_analysis(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")

    analysis = analyze_transactions_with_gpt(transactions)
    return {"transactions": [t.__dict__ for t in transactions], "analysis": analysis}

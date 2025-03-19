from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from typing import Optional

# Database connection using environment variables for security
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_FJhzvylqE48X@ep-blue-snowflake-a55srenu-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Order Model (Database)
class OrderModel(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    product_name = Column(String, index=True)
    price = Column(Float)

# Create tables
Base.metadata.create_all(bind=engine)

# Request/Response Models (Pydantic)
class OrderCreate(BaseModel):
    customer_name: str = Field(..., example="John Doe")
    product_name: str = Field(..., example="Smartphone")
    price: float = Field(..., example=499.99)

class OrderResponse(BaseModel):
    status: str
    order_id: Optional[int] = None
    
    class Config:
        orm_mode = True

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize FastAPI
app = FastAPI(
    title="Orders Service API",
    description="Microservice for order management",
    version="1.0.0"
)

@app.post("/orders/", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order
    
    Returns the order ID and status
    """
    try:
        # Create an order DB model instance
        db_order = OrderModel(
            customer_name=order.customer_name,
            product_name=order.product_name,
            price=order.price
        )
        
        # Add and commit to DB
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        # Return success response
        return {"status": "success", "order_id": db_order.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
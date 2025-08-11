from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import logging
import os
import jwt
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security configuration
SECRET_KEY = os.getenv("JWT_SECRET", "merck-demo-secret-key")
ALGORITHM = "HS256"
security = HTTPBearer()

app = FastAPI(
    title="Merck DevOps Challenge API",
    description="Demo API for DevOps talent showcase with authentication",
    version="1.0.0"
)

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# In-memory storage for demo
items_db = [
    {"id": 1, "name": "Laptop", "description": "High-performance laptop", "price": 999.99},
    {"id": 2, "name": "Mouse", "description": "Wireless mouse", "price": 29.99}
]

# Demo users (in production, use proper user management)
users_db = {
    "demo": "password123",
    "merck": "challenge2024"
}

def create_access_token(data: dict):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/login", response_model=Token)
def login(request: LoginRequest):
    """Login endpoint to get access token"""
    if request.username not in users_db or users_db[request.username] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": request.username})
    logger.info(f"User {request.username} logged in")
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/health")
def health_check():
    """Health check endpoint (public)"""
    logger.info("Health check requested")
    return {"status": "healthy", "environment": os.getenv("ENV", "development")}

@app.get("/items", response_model=List[Item])
def get_items(current_user: str = Depends(verify_token)):
    """Get all items (requires authentication)"""
    logger.info(f"User {current_user} retrieved {len(items_db)} items")
    return items_db

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int, current_user: str = Depends(verify_token)):
    """Get item by ID (requires authentication)"""
    item = next((item for item in items_db if item["id"] == item_id), None)
    if not item:
        logger.warning(f"User {current_user}: Item {item_id} not found")
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=Item)
def create_item(item: ItemCreate, current_user: str = Depends(verify_token)):
    """Create new item (requires authentication)"""
    new_id = max([item["id"] for item in items_db], default=0) + 1
    new_item = {"id": new_id, **item.dict()}
    items_db.append(new_item)
    logger.info(f"User {current_user} created item {new_id}")
    return new_item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

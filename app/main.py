import boto3
import logging
import os
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cognito configuration
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID", "us-east-1_PLACEHOLDER")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID", "PLACEHOLDER")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

cognito_client = boto3.client('cognito-idp', region_name=AWS_REGION)
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
    {
        "id": 1,
        "name": "Laptop",
        "description": "High-performance laptop",
        "price": 999.99,
    },
    {"id": 2, "name": "Mouse", "description": "Wireless mouse", "price": 29.99},
]

# Demo credentials for Cognito
DEMO_CREDENTIALS = {"demo": "password123"}


def verify_cognito_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify Cognito access token"""
    try:
        response = cognito_client.get_user(
            AccessToken=credentials.credentials
        )
        username = response['Username']
        return username
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/login", response_model=Token)
def login(request: LoginRequest):
    """Login endpoint using Cognito authentication"""
    try:
        response = cognito_client.admin_initiate_auth(
            UserPoolId=COGNITO_USER_POOL_ID,
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': request.username,
                'PASSWORD': request.password
            }
        )
        
        access_token = response['AuthenticationResult']['AccessToken']
        logger.info(f"User {request.username} logged in via Cognito")
        return {"access_token": access_token, "token_type": "bearer"}
        
    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Authentication service error")

@app.get("/health")
def health_check():
    """Health check endpoint (public)"""
    logger.info("Health check requested")
    return {"status": "healthy", "environment": os.getenv("ENV", "development")}

@app.get("/items", response_model=List[Item])
def get_items(current_user: str = Depends(verify_cognito_token)):
    """Get all items (requires authentication)"""
    logger.info(f"User {current_user} retrieved {len(items_db)} items")
    return items_db

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int, current_user: str = Depends(verify_cognito_token)):
    """Get item by ID (requires authentication)"""
    item = next((item for item in items_db if item["id"] == item_id), None)
    if not item:
        logger.warning(f"User {current_user}: Item {item_id} not found")
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=Item)
def create_item(item: ItemCreate, current_user: str = Depends(verify_cognito_token)):
    """Create new item (requires authentication)"""
    new_id = max([item["id"] for item in items_db], default=0) + 1
    new_item = {"id": new_id, **item.dict()}
    items_db.append(new_item)
    logger.info(f"User {current_user} created item {new_id}")
    return new_item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

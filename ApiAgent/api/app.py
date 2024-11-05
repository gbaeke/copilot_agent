from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict
from datetime import datetime, timedelta
import random
from fastapi.openapi.utils import get_openapi
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Sales API", description="API for retrieving sales data")

# Security
security = HTTPBearer(scheme_name="BearerAuth")  # Change scheme name to match our spec
VALID_TOKEN = os.getenv("API_KEY")  # Load the API key from the environment variable

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Sales API",
        version="1.0.0",
        description="API for retrieving sales data",
        routes=app.routes,
    )
    
    # Set OpenAPI version
    openapi_schema["openapi"] = "3.0.0"
    
    # Add servers
    openapi_schema["servers"] = [
        {
            "url": "https://fb83-94-143-189-241.ngrok-free.app",  # Replace with your production URL
            "description": "Production server"
        }
    ]
    
    # Add security scheme
    openapi_schema["components"] = {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer"
            }
        }
    }
    
    # Remove endpoint-specific security requirements
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            if "security" in operation:
                del operation["security"]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != VALID_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

def generate_sample_sales_data() -> List[Dict]:
    products = ["Laptop", "Smartphone", "Tablet", "Headphones", "Smartwatch"]
    sales_data = []
    
    # Generate 50 sample sales records
    for _ in range(50):
        sale_date = datetime.now() - timedelta(days=random.randint(0, 365))
        sale = {
            "id": random.randint(1000, 9999),
            "product": random.choice(products),
            "quantity": random.randint(1, 10),
            "price": round(random.uniform(100, 2000), 2),
            "date": sale_date.strftime("%Y-%m-%d"),
            "customer_id": random.randint(1, 1000)
        }
        sale["total"] = round(sale["quantity"] * sale["price"], 2)
        sales_data.append(sale)
    
    return sorted(sales_data, key=lambda x: x["date"], reverse=True)

@app.get("/sales/", dependencies=[Depends(verify_token)])
async def get_sales():
    """
    Retrieve sales data.
    Requires Bearer token authentication.
    """
    return {
        "status": "success",
        "data": generate_sample_sales_data()
    }

@app.get("/")
async def root():
    """
    Root endpoint - provides API information
    """
    return {
        "message": "Welcome to the Sales API",
        "documentation": "/docs",
        "endpoints": ["/sales/"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import List

# -----------------------------
# App Initialization
# -----------------------------

app = FastAPI(
    title="Professional FastAPI Demo",
    description="A robust FastAPI application demonstrating Pydantic v2 validation and full CRUD operations.",
    version="1.0.0"
)

# -----------------------------
# Pydantic Models
# -----------------------------

class User(BaseModel):
    name: str = Field(min_length=3, max_length=20, examples=["Ahmet"])
    email: EmailStr = Field(examples=["ahmet@example.com"])
    age: int = Field(gt=0, le=90, examples=[30])

class UserResponse(User):
    id: int

class Product(BaseModel):
    name: str = Field(examples=["Gofret"])
    price: float = Field(gt=0.0, examples=[85.10])
    description: str | None = Field(default=None, examples=["Amazing gofret"])
    stock: bool = True

class ProductResponse(Product):
    id: int

# -----------------------------
# Mock Databases (In-Memory)
# -----------------------------

fake_users_db: List[dict] = []
fake_products_db: List[dict] = []

# -----------------------------
# User Endpoints
# -----------------------------

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: User):
    """
    Register a new user in the system.
    """
    new_id = len(fake_users_db) + 1
    user_data = {"id": new_id, **user.model_dump()}
    fake_users_db.append(user_data)
    return user_data

@app.get("/users", response_model=List[UserResponse], tags=["Users"])
def get_users(skip: int = 0, limit: int = 10):
    """
    Retrieve a paginated list of all users.
    """
    return fake_users_db[skip : skip + limit]

@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user_by_id(user_id: int):
    """
    Retrieve a specific user by their unique ID.
    """
    user = next((u for u in fake_users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def update_user(user_id: int, user_update: User):
    """
    Update an existing user's information by ID.
    """
    for index, u in enumerate(fake_users_db):
        if u["id"] == user_id:
            updated_data = {"id": user_id, **user_update.model_dump()}
            fake_users_db[index] = updated_data
            return updated_data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(user_id: int):
    """
    Remove a user from the system by ID.
    """
    for index, u in enumerate(fake_users_db):
        if u["id"] == user_id:
            fake_users_db.pop(index)
            return None
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

# -----------------------------
# Product Endpoints
# -----------------------------

@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, tags=["Products"])
def create_product(product: Product):
    """
    Add a new product to the inventory.
    """
    new_id = len(fake_products_db) + 1
    product_data = {"id": new_id, **product.model_dump()}
    fake_products_db.append(product_data)
    return product_data

@app.get("/products", response_model=List[ProductResponse], tags=["Products"])
def get_products(skip: int = 0, limit: int = 10):
    """
    Retrieve a paginated list of all products.
    """
    return fake_products_db[skip : skip + limit]

@app.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def get_product_by_id(product_id: int):
    """
    Retrieve a specific product by its unique ID.
    """
    product = next((p for p in fake_products_db if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def update_product(product_id: int, product_update: Product):
    """
    Update an existing product's details by ID.
    """
    for index, p in enumerate(fake_products_db):
        if p["id"] == product_id:
            updated_data = {"id": product_id, **product_update.model_dump()}
            fake_products_db[index] = updated_data
            return updated_data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Products"])
def delete_product(product_id: int):
    """
    Remove a product from inventory by ID.
    """
    for index, p in enumerate(fake_products_db):
        if p["id"] == product_id:
            fake_products_db.pop(index)
            return None
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

# -----------------------------
# Search/Utility Endpoints
# -----------------------------

@app.get("/search", tags=["Utilities"])
def search_items(q: str, limit: int = 10):
    """
    Searches items based on a query string (mocked implementation).
    """
    # Filter dummy results based on query string from products/users if needed
    return {
        "query": q, 
        "results": [p for p in fake_products_db if q.lower() in p["name"].lower()], 
        "limit": limit
    }

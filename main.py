"""
This file demonstrates the usage of Pydantic models and FastAPI.
It includes:
1. A User model with validation
2. A Product model with optional fields
3. A simple FastAPI application with example endpoints
"""

# -----------------------------
# Imports
# -----------------------------

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from fastapi import FastAPI


# -----------------------------
# User Model (Pydantic)
# -----------------------------

class User(BaseModel):
    """
    User model represents a user entity.

    Fields:
    - name: User name (3–20 characters)
    - mail: Email address (12–50 characters)
    - yas: Age (must be between 1 and 90)
    """

    name: str = Field(min_length=3, max_length=20)
    mail: str = Field(min_length=12, max_length=50)
    yas: int = Field(gt=0, le=90)

    @field_validator("mail")
    @classmethod
    def validate_mail(cls, v):
        """
        Custom validator for email field.
        - Ensures '@' exists in the email
        - Converts email to lowercase
        """
        if "@" not in v:
            raise ValueError("Geçerli bir mail adresi giriniz")
        return v.lower()


# -----------------------------
# User Model Usage Example
# -----------------------------

# Creating a User instance
me = User(
    name="ahmet",
    mail="JDSUDJS   IDJ@gmail.com",
    yas=45
)

# Printing the validated and formatted user object
print(me)


# -----------------------------
# Product Model (Pydantic)
# -----------------------------

class Product(BaseModel):
    """
    Product model represents a product entity.

    Fields:
    - id: Product ID
    - name: Product name
    - price: Product price
    - description: Optional product description
    - stock: Availability status (default: True)
    """

    id: int
    name: str
    price: float
    description: Optional[str]
    stock: bool = True


# -----------------------------
# Product Model Usage Example
# -----------------------------

myModel = Product(
    id=154,
    name="gofret",
    price=85.1,
    description="amazing gofret"
)

print(myModel)


# -----------------------------
# FastAPI Application
# -----------------------------

app = FastAPI()


@app.get("/users")
async def get_users():
    """
    Returns a list of all users.
    """
    return {"users": ["Alice", "Bob", "Charlie"]}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """
    Returns a specific user by user_id.
    """
    return {"user_id": user_id, "name": "Alice"}


@app.get("/search")
async def search_items(q: str, limit: int = 10):
    """
    Searches items based on a query string.
    """
    return {"query": q, "results": [], "limit": limit}

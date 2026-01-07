import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
from datetime import datetime
import random
import string

load_dotenv()

app = FastAPI(title="Flipkart Clone API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase: Client = create_client(
    os.getenv("VITE_SUPABASE_URL"),
    os.getenv("VITE_SUPABASE_ANON_KEY")
)

DEFAULT_USER_ID = "00000000-0000-0000-0000-000000000001"

class CartItemCreate(BaseModel):
    product_id: str
    quantity: int = 1

class CartItemUpdate(BaseModel):
    quantity: int

class AddressCreate(BaseModel):
    full_name: str
    phone: str
    address_line1: str
    address_line2: Optional[str] = ""
    city: str
    state: str
    pincode: str
    is_default: bool = False

class OrderCreate(BaseModel):
    address_id: str
    payment_method: str = "cod"

@app.get("/")
def read_root():
    return {"message": "Flipkart Clone API"}

@app.get("/api/categories")
def get_categories():
    response = supabase.table("categories").select("*").execute()
    return response.data

@app.get("/api/products")
def get_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    query = supabase.table("products").select(
        "*, category:categories(name, slug), images:product_images(*)"
    )

    if category:
        category_response = supabase.table("categories").select("id").eq("slug", category).execute()
        if category_response.data:
            query = query.eq("category_id", category_response.data[0]["id"])

    if search:
        query = query.ilike("name", f"%{search}%")

    query = query.eq("is_available", True).order("created_at", desc=True)
    query = query.range(offset, offset + limit - 1)

    response = query.execute()
    return response.data

@app.get("/api/products/{slug}")
def get_product(slug: str):
    response = supabase.table("products").select(
        "*, category:categories(name, slug), images:product_images(*)"
    ).eq("slug", slug).eq("is_available", True).maybeSingle().execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Product not found")

    return response.data

@app.get("/api/cart")
def get_cart():
    response = supabase.table("cart_items").select(
        "*, product:products(*, images:product_images(*))"
    ).eq("user_id", DEFAULT_USER_ID).execute()

    return response.data

@app.post("/api/cart")
def add_to_cart(item: CartItemCreate):
    existing = supabase.table("cart_items").select("*").eq(
        "user_id", DEFAULT_USER_ID
    ).eq("product_id", item.product_id).maybeSingle().execute()

    if existing.data:
        response = supabase.table("cart_items").update({
            "quantity": existing.data["quantity"] + item.quantity,
            "updated_at": datetime.now().isoformat()
        }).eq("id", existing.data["id"]).execute()
    else:
        response = supabase.table("cart_items").insert({
            "user_id": DEFAULT_USER_ID,
            "product_id": item.product_id,
            "quantity": item.quantity
        }).execute()

    return response.data

@app.patch("/api/cart/{cart_item_id}")
def update_cart_item(cart_item_id: str, item: CartItemUpdate):
    if item.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    response = supabase.table("cart_items").update({
        "quantity": item.quantity,
        "updated_at": datetime.now().isoformat()
    }).eq("id", cart_item_id).eq("user_id", DEFAULT_USER_ID).execute()

    return response.data

@app.delete("/api/cart/{cart_item_id}")
def remove_from_cart(cart_item_id: str):
    response = supabase.table("cart_items").delete().eq(
        "id", cart_item_id
    ).eq("user_id", DEFAULT_USER_ID).execute()

    return {"message": "Item removed from cart"}

@app.delete("/api/cart")
def clear_cart():
    response = supabase.table("cart_items").delete().eq(
        "user_id", DEFAULT_USER_ID
    ).execute()

    return {"message": "Cart cleared"}

@app.get("/api/addresses")
def get_addresses():
    response = supabase.table("addresses").select("*").eq(
        "user_id", DEFAULT_USER_ID
    ).execute()

    return response.data

@app.post("/api/addresses")
def create_address(address: AddressCreate):
    response = supabase.table("addresses").insert({
        "user_id": DEFAULT_USER_ID,
        **address.model_dump()
    }).execute()

    return response.data

@app.post("/api/orders")
def create_order(order: OrderCreate):
    cart_items = supabase.table("cart_items").select(
        "*, product:products(*)"
    ).eq("user_id", DEFAULT_USER_ID).execute()

    if not cart_items.data:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = sum(
        item["quantity"] * float(item["product"]["price"])
        for item in cart_items.data
    )

    order_number = ''.join(random.choices(string.digits, k=10))

    order_response = supabase.table("orders").insert({
        "user_id": DEFAULT_USER_ID,
        "address_id": order.address_id,
        "order_number": order_number,
        "total_amount": total_amount,
        "status": "pending",
        "payment_method": order.payment_method
    }).execute()

    order_id = order_response.data[0]["id"]

    order_items = [
        {
            "order_id": order_id,
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "price": float(item["product"]["price"])
        }
        for item in cart_items.data
    ]

    supabase.table("order_items").insert(order_items).execute()

    supabase.table("cart_items").delete().eq("user_id", DEFAULT_USER_ID).execute()

    return order_response.data[0]

@app.get("/api/orders")
def get_orders():
    response = supabase.table("orders").select(
        "*, address:addresses(*), order_items:order_items(*, product:products(*))"
    ).eq("user_id", DEFAULT_USER_ID).order("created_at", desc=True).execute()

    return response.data

@app.get("/api/orders/{order_id}")
def get_order(order_id: str):
    response = supabase.table("orders").select(
        "*, address:addresses(*), order_items:order_items(*, product:products(*))"
    ).eq("id", order_id).eq("user_id", DEFAULT_USER_ID).maybeSingle().execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Order not found")

    return response.data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

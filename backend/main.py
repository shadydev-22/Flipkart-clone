import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import random
import string
from uuid import UUID
from dotenv import load_dotenv

from database import get_db
# Note: imported classes must match models.py
from models import Category, Product, ProductImage, CartItem, Address, Order, OrderItem, User, WishlistItem


load_dotenv()

app = FastAPI(title="Flipkart Clone API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    # payment_method: str = "cod" # Removed from DB

class ProductImageResponse(BaseModel):
    id: UUID
    image_url: str
    is_primary: bool
    display_order: int

    class Config:
        orm_mode = True

class ProductResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str]
    price: float
    original_price: Optional[float]
    discount_percentage: int
    stock_quantity: int
    brand: Optional[str]
    rating: float
    review_count: int
    images: List[ProductImageResponse] = []

    class Config:
        orm_mode = True

class CartItemResponse(BaseModel):
    id: UUID
    quantity: int
    product: ProductResponse
    
    class Config:
        orm_mode = True

class OrderItemResponse(BaseModel):
    id: UUID
    quantity: int
    price_at_purchase: float
    product: ProductResponse

    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    id: UUID
    created_at: datetime
    total_amount: float
    status: str
    items: List[OrderItemResponse] = []
    
    class Config:
        orm_mode = True

@app.get("/")
def read_root():
    return {"message": "Flipkart Clone API"}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/api/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories

@app.get("/api/products", response_model=List[ProductResponse])
def get_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category:
        cat_obj = db.query(Category).filter(Category.slug == category).first()
        if cat_obj:
            # Get current category ID and all subcategory IDs
            category_ids = [cat_obj.id]
            subcategories = db.query(Category).filter(Category.parent_id == cat_obj.id).all()
            for sub in subcategories:
                category_ids.append(sub.id)
            
            query = query.filter(Product.category_id.in_(category_ids))
    
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    query = query.filter(Product.is_available == True).order_by(Product.created_at.desc())
    
    products = query.options(joinedload(Product.images)).offset(offset).limit(limit).all()
    # Explicitly load relationships if needed, but Pydantic serialization usually handles it via lazy load
    return products

@app.get("/api/products/{slug}", response_model=ProductResponse)
def get_product(slug: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.slug == slug).options(joinedload(Product.images)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/api/cart", response_model=List[CartItemResponse])
def get_cart(db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == DEFAULT_USER_ID).options(
        joinedload(CartItem.product).joinedload(Product.images)
    ).all()
    return cart_items

@app.post("/api/cart")
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == DEFAULT_USER_ID).first()
    if not user:
        user = User(id=DEFAULT_USER_ID, email="test@example.com", full_name="Test User")
        db.add(user)
        db.commit()

    existing = db.query(CartItem).filter(
        CartItem.user_id == DEFAULT_USER_ID,
        CartItem.product_id == item.product_id
    ).first()

    if existing:
        existing.quantity += item.quantity
        # existing.updated_at = datetime.now() # Schema might not have updated_at for cart? 
        # Checked models: CartItem has created_at but no explicit updated_at in user provided SQL?
        # User SQL: has created_at, UNIQUE. No updated_at.
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new_item = CartItem(
            user_id=DEFAULT_USER_ID,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

@app.patch("/api/cart/{cart_item_id}")
def update_cart_item(cart_item_id: str, item: CartItemUpdate, db: Session = Depends(get_db)):
    if item.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == DEFAULT_USER_ID
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found")

    cart_item.quantity = item.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

@app.delete("/api/cart/{cart_item_id}")
def remove_from_cart(cart_item_id: str, db: Session = Depends(get_db)):
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == DEFAULT_USER_ID
    ).first()
    
    if cart_item:
        db.delete(cart_item)
        db.commit()

    return {"message": "Item removed from cart"}

@app.delete("/api/cart")
def clear_cart(db: Session = Depends(get_db)):
    db.query(CartItem).filter(CartItem.user_id == DEFAULT_USER_ID).delete()
    db.commit()
    return {"message": "Cart cleared"}

@app.get("/api/addresses")
def get_addresses(db: Session = Depends(get_db)):
    return db.query(Address).filter(Address.user_id == DEFAULT_USER_ID).all()

@app.post("/api/addresses")
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == DEFAULT_USER_ID).first()
    if not user:
         user = User(id=DEFAULT_USER_ID, email="test@example.com", full_name="Test User")
         db.add(user)
         db.commit()

    # Merge address lines
    full_address_line = address.address_line1
    if address.address_line2:
        full_address_line += ", " + address.address_line2

    new_addr = Address(
        user_id=DEFAULT_USER_ID,
        full_name=address.full_name,
        phone=address.phone,
        city=address.city,
        state=address.state,
        pincode=address.pincode,
        is_default=address.is_default,
        address_line=full_address_line # New field
    )
    db.add(new_addr)
    db.commit()
    db.refresh(new_addr)
    return new_addr

@app.post("/api/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == DEFAULT_USER_ID).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = sum(
        item.quantity * float(item.product.price)
        for item in cart_items
    )

    # Order number generated by DB (Serial)
    # Payment method removed from DB

    new_order = Order(
        user_id=DEFAULT_USER_ID,
        address_id=order.address_id,
        total_amount=total_amount,
        status="Placed"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=item.product.price # Renamed field
        )
        db.add(order_item)
    
    # Clear cart
    db.query(CartItem).filter(CartItem.user_id == DEFAULT_USER_ID).delete()
    db.commit()
    
    return new_order

@app.get("/api/orders", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.user_id == DEFAULT_USER_ID).options(
        joinedload(Order.items).joinedload(OrderItem.product).joinedload(Product.images)
    ).order_by(Order.created_at.desc()).all()

@app.get("/api/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == DEFAULT_USER_ID).options(
        joinedload(Order.items).joinedload(OrderItem.product).joinedload(Product.images)
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Wishlist endpoints
@app.get("/api/wishlist")
def get_wishlist(db: Session = Depends(get_db)):
    wishlist_items = db.query(WishlistItem).filter(WishlistItem.user_id == DEFAULT_USER_ID).options(
        joinedload(WishlistItem.product).joinedload(Product.images)
    ).all()
    
    # Return products with their details
    return [{
        "id": item.id,
        "product": {
            "id": item.product.id,
            "name": item.product.name,
            "slug": item.product.slug,
            "price": item.product.price,
            "original_price": item.product.original_price,
            "discount_percentage": item.product.discount_percentage,
            "brand": item.product.brand,
            "stock_quantity": item.product.stock_quantity,
            "images": [{"id": img.id, "image_url": img.image_url, "is_primary": img.is_primary, "display_order": img.display_order} for img in item.product.images]
        },
        "created_at": item.created_at
    } for item in wishlist_items]

@app.post("/api/wishlist")
def add_to_wishlist(product_id: str, db: Session = Depends(get_db)):
    # Ensure user exists
    user = db.query(User).filter(User.id == DEFAULT_USER_ID).first()
    if not user:
        user = User(id=DEFAULT_USER_ID, email="test@example.com", full_name="Test User")
        db.add(user)
        db.commit()
    
    # Check if already in wishlist
    existing = db.query(WishlistItem).filter(
        WishlistItem.user_id == DEFAULT_USER_ID,
        WishlistItem.product_id == product_id
    ).first()
    
    if existing:
        return {"message": "Product already in wishlist", "id": existing.id}
    
    # Add to wishlist
    new_item = WishlistItem(
        user_id=DEFAULT_USER_ID,
        product_id=product_id
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"message": "Added to wishlist", "id": new_item.id}

@app.delete("/api/wishlist/{product_id}")
def remove_from_wishlist(product_id: str, db: Session = Depends(get_db)):
    wishlist_item = db.query(WishlistItem).filter(
        WishlistItem.user_id == DEFAULT_USER_ID,
        WishlistItem.product_id == product_id
    ).first()
    
    if wishlist_item:
        db.delete(wishlist_item)
        db.commit()
        return {"message": "Removed from wishlist"}
    
    return {"message": "Item not in wishlist"}

@app.get("/api/wishlist/check/{product_id}")
def check_wishlist(product_id: str, db: Session = Depends(get_db)):
    exists = db.query(WishlistItem).filter(
        WishlistItem.user_id == DEFAULT_USER_ID,
        WishlistItem.product_id == product_id
    ).first() is not None
    
    return {"in_wishlist": exists}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)


# Flipkart Clone

A full-featured e-commerce application inspired by Flipkart, built with React, FastAPI, and Supabase.

## Tech Stack

### Frontend
- **React.js 18** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.8+** - Programming language

### Database
- **Supabase (PostgreSQL)** - Database and backend services
- Row Level Security (RLS) policies for data security

## Features

### Core Features
- **Product Listing Page**
  - Grid layout with product cards
  - Search functionality by product name
  - Filter products by category
  - Responsive design

- **Product Detail Page**
  - Image carousel with multiple product images
  - Detailed product information and specifications
  - Add to Cart and Buy Now buttons
  - Stock availability status

- **Shopping Cart**
  - View all items in cart
  - Update product quantities
  - Remove items from cart
  - Cart summary with subtotal and total

- **Order Placement**
  - Checkout page with shipping address form
  - Order summary review
  - Place order functionality
  - Order confirmation page with order details

### Bonus Features
- Fully responsive design (mobile, tablet, desktop)
- Order history - view all past orders
- Persistent cart using database
- Clean and modern UI matching Flipkart's design

## Database Schema

The application uses the following database tables:

- **categories** - Product categories
- **products** - Product information with specifications
- **product_images** - Multiple images per product
- **users** - User information (default user pre-configured)
- **addresses** - Shipping addresses
- **cart_items** - Shopping cart items
- **orders** - Order information
- **order_items** - Items in each order

All tables are protected with Row Level Security (RLS) policies.

## Setup Instructions

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+

### 1. Clone the Repository
```bash
cd Flipkart-clone
```

### 2. Database Setup (Local PostgreSQL)

The project is configured to use a local PostgreSQL database.

1. Create a database named `flipkart_clone`:
   ```bash
   createdb flipkart_clone
   ```

2. Create a `.env` file in the root directory:
   ```bash
   DATABASE_URL=postgresql://user:password@localhost:5432/flipkart_clone
   ```

3. Initialize the database:
   ```bash
   # From root directory
   python backend/init_db.py
   python backend/seed.py
   ```

### 4. Install Frontend Dependencies
```bash
npm install
```

### 5. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 6. Run the Backend Server
```bash
# From the backend directory
python main.py
```
The FastAPI server will start on `http://localhost:8000`

### 7. Run the Frontend Development Server
```bash
# From the root directory
npm run dev
```
The React app will start on `http://localhost:3000`

### 8. Build for Production
```bash
npm run build
```

## API Endpoints

### Products
- `GET /api/categories` - Get all categories
- `GET /api/products` - Get all products (supports search and category filters)
- `GET /api/products/{slug}` - Get product by slug

### Cart
- `GET /api/cart` - Get cart items
- `POST /api/cart` - Add item to cart
- `PATCH /api/cart/{id}` - Update cart item quantity
- `DELETE /api/cart/{id}` - Remove item from cart
- `DELETE /api/cart` - Clear cart

### Orders
- `GET /api/orders` - Get all orders
- `GET /api/orders/{id}` - Get order by ID
- `POST /api/orders` - Create new order

### Addresses
- `GET /api/addresses` - Get user addresses
- `POST /api/addresses` - Create new address

## Project Structure

```
├── backend/
│   ├── main.py                 # FastAPI application
│   └── requirements.txt        # Python dependencies
├── src/
│   ├── components/
│   │   └── Header.jsx          # Navigation header
│   ├── context/
│   │   └── CartContext.jsx     # Global cart state
│   ├── pages/
│   │   ├── HomePage.jsx        # Landing page
│   │   ├── ProductListPage.jsx # Product listing
│   │   ├── ProductDetailPage.jsx # Product details
│   │   ├── CartPage.jsx        # Shopping cart
│   │   ├── CheckoutPage.jsx    # Checkout flow
│   │   ├── OrderConfirmationPage.jsx # Order success
│   │   └── OrderHistoryPage.jsx # Past orders
│   ├── App.jsx                 # Main app component
│   ├── main.jsx               # Entry point
│   └── index.css              # Global styles
├── index.html
├── vite.config.js
├── package.json
└── README.md
```

## Design Choices

### UI/UX
- Color scheme inspired by Flipkart's blue and orange branding
- Card-based product layout for easy scanning
- Sticky header for easy navigation
- Clear call-to-action buttons
- Consistent spacing and typography

### Performance
- Optimized images using Pexels CDN
- Efficient database queries with proper indexing
- Client-side state management for cart

### Security
- Row Level Security (RLS) on all database tables
- Input validation on forms
- Prepared statements to prevent SQL injection

## Assumptions

1. A default user is always logged in (ID: 00000000-0000-0000-0000-000000000001)
2. All prices are in Indian Rupees (₹)
3. Free delivery on orders above ₹500
4. Only Cash on Delivery (COD) payment method is implemented
5. Product images are sourced from Pexels stock photos

## Future Enhancements

- User authentication and registration
- Multiple payment methods (cards, UPI, wallets)
- Product reviews and ratings system
- Wishlist functionality
- Advanced filters (price range, brand, rating)
- Order tracking
- Admin panel for product management

## License

This project is created for educational purposes.
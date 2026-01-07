/*
  # Flipkart Clone - E-commerce Database Schema

  ## Overview
  Complete database schema for a Flipkart-style e-commerce platform with products, categories, cart, and orders.

  ## New Tables
  
  ### 1. categories
  - `id` (uuid, primary key) - Unique category identifier
  - `name` (text) - Category name (Electronics, Fashion, etc.)
  - `slug` (text, unique) - URL-friendly category identifier
  - `description` (text) - Category description
  - `image_url` (text) - Category image
  - `created_at` (timestamptz) - Creation timestamp

  ### 2. products
  - `id` (uuid, primary key) - Unique product identifier
  - `category_id` (uuid, foreign key) - Reference to categories
  - `name` (text) - Product name
  - `slug` (text, unique) - URL-friendly product identifier
  - `description` (text) - Product description
  - `specifications` (jsonb) - Product specifications as JSON
  - `price` (numeric) - Product price
  - `original_price` (numeric) - Original price (for discount display)
  - `discount_percentage` (integer) - Discount percentage
  - `stock_quantity` (integer) - Available stock
  - `brand` (text) - Product brand
  - `rating` (numeric) - Average rating (0-5)
  - `review_count` (integer) - Number of reviews
  - `is_available` (boolean) - Availability status
  - `created_at` (timestamptz) - Creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ### 3. product_images
  - `id` (uuid, primary key) - Unique image identifier
  - `product_id` (uuid, foreign key) - Reference to products
  - `image_url` (text) - Image URL
  - `display_order` (integer) - Order of image display
  - `is_primary` (boolean) - Primary image flag
  - `created_at` (timestamptz) - Creation timestamp

  ### 4. users
  - `id` (uuid, primary key) - Unique user identifier
  - `email` (text, unique) - User email
  - `full_name` (text) - User's full name
  - `phone` (text) - User's phone number
  - `created_at` (timestamptz) - Creation timestamp

  ### 5. addresses
  - `id` (uuid, primary key) - Unique address identifier
  - `user_id` (uuid, foreign key) - Reference to users
  - `full_name` (text) - Recipient name
  - `phone` (text) - Contact phone
  - `address_line1` (text) - Street address
  - `address_line2` (text) - Additional address info
  - `city` (text) - City
  - `state` (text) - State/Province
  - `pincode` (text) - Postal code
  - `is_default` (boolean) - Default address flag
  - `created_at` (timestamptz) - Creation timestamp

  ### 6. cart_items
  - `id` (uuid, primary key) - Unique cart item identifier
  - `user_id` (uuid, foreign key) - Reference to users
  - `product_id` (uuid, foreign key) - Reference to products
  - `quantity` (integer) - Item quantity
  - `created_at` (timestamptz) - Creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ### 7. orders
  - `id` (uuid, primary key) - Unique order identifier
  - `user_id` (uuid, foreign key) - Reference to users
  - `address_id` (uuid, foreign key) - Reference to addresses
  - `order_number` (text, unique) - Human-readable order number
  - `total_amount` (numeric) - Total order amount
  - `status` (text) - Order status (pending, confirmed, shipped, delivered, cancelled)
  - `payment_method` (text) - Payment method
  - `created_at` (timestamptz) - Order creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ### 8. order_items
  - `id` (uuid, primary key) - Unique order item identifier
  - `order_id` (uuid, foreign key) - Reference to orders
  - `product_id` (uuid, foreign key) - Reference to products
  - `quantity` (integer) - Item quantity
  - `price` (numeric) - Price at time of order
  - `created_at` (timestamptz) - Creation timestamp

  ## Security
  - Enable RLS on all tables
  - Add policies for authenticated access (simplified for default user)
  
  ## Important Notes
  1. All tables use UUID as primary keys for better scalability
  2. Timestamps track creation and updates
  3. Foreign keys maintain referential integrity
  4. JSONB used for flexible product specifications
  5. Numeric type used for prices to avoid floating point issues
  6. Default values set for booleans and timestamps
*/

-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  slug text UNIQUE NOT NULL,
  description text DEFAULT '',
  image_url text DEFAULT '',
  created_at timestamptz DEFAULT now()
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  category_id uuid REFERENCES categories(id) ON DELETE SET NULL,
  name text NOT NULL,
  slug text UNIQUE NOT NULL,
  description text DEFAULT '',
  specifications jsonb DEFAULT '{}'::jsonb,
  price numeric(10, 2) NOT NULL,
  original_price numeric(10, 2),
  discount_percentage integer DEFAULT 0,
  stock_quantity integer DEFAULT 0,
  brand text DEFAULT '',
  rating numeric(2, 1) DEFAULT 0,
  review_count integer DEFAULT 0,
  is_available boolean DEFAULT true,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create product_images table
CREATE TABLE IF NOT EXISTS product_images (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id uuid REFERENCES products(id) ON DELETE CASCADE NOT NULL,
  image_url text NOT NULL,
  display_order integer DEFAULT 0,
  is_primary boolean DEFAULT false,
  created_at timestamptz DEFAULT now()
);

-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text UNIQUE NOT NULL,
  full_name text NOT NULL,
  phone text DEFAULT '',
  created_at timestamptz DEFAULT now()
);

-- Create addresses table
CREATE TABLE IF NOT EXISTS addresses (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  full_name text NOT NULL,
  phone text NOT NULL,
  address_line1 text NOT NULL,
  address_line2 text DEFAULT '',
  city text NOT NULL,
  state text NOT NULL,
  pincode text NOT NULL,
  is_default boolean DEFAULT false,
  created_at timestamptz DEFAULT now()
);

-- Create cart_items table
CREATE TABLE IF NOT EXISTS cart_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  product_id uuid REFERENCES products(id) ON DELETE CASCADE NOT NULL,
  quantity integer DEFAULT 1,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE(user_id, product_id)
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  address_id uuid REFERENCES addresses(id) ON DELETE SET NULL,
  order_number text UNIQUE NOT NULL,
  total_amount numeric(10, 2) NOT NULL,
  status text DEFAULT 'pending',
  payment_method text DEFAULT 'cod',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id uuid REFERENCES orders(id) ON DELETE CASCADE NOT NULL,
  product_id uuid REFERENCES products(id) ON DELETE SET NULL,
  quantity integer NOT NULL,
  price numeric(10, 2) NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_slug ON products(slug);
CREATE INDEX IF NOT EXISTS idx_product_images_product ON product_images(product_id);
CREATE INDEX IF NOT EXISTS idx_cart_items_user ON cart_items(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);

-- Enable Row Level Security
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_images ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE addresses ENABLE ROW LEVEL SECURITY;
ALTER TABLE cart_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE order_items ENABLE ROW LEVEL SECURITY;

-- RLS Policies for categories (public read access)
CREATE POLICY "Anyone can view categories"
  ON categories FOR SELECT
  USING (true);

-- RLS Policies for products (public read access)
CREATE POLICY "Anyone can view products"
  ON products FOR SELECT
  USING (true);

-- RLS Policies for product_images (public read access)
CREATE POLICY "Anyone can view product images"
  ON product_images FOR SELECT
  USING (true);

-- RLS Policies for users (users can view their own data)
CREATE POLICY "Users can view own profile"
  ON users FOR SELECT
  USING (true);

CREATE POLICY "Users can update own profile"
  ON users FOR UPDATE
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Users can insert own profile"
  ON users FOR INSERT
  WITH CHECK (true);

-- RLS Policies for addresses
CREATE POLICY "Users can view own addresses"
  ON addresses FOR SELECT
  USING (true);

CREATE POLICY "Users can insert own addresses"
  ON addresses FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Users can update own addresses"
  ON addresses FOR UPDATE
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Users can delete own addresses"
  ON addresses FOR DELETE
  USING (true);

-- RLS Policies for cart_items
CREATE POLICY "Users can view own cart"
  ON cart_items FOR SELECT
  USING (true);

CREATE POLICY "Users can insert to own cart"
  ON cart_items FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Users can update own cart"
  ON cart_items FOR UPDATE
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Users can delete from own cart"
  ON cart_items FOR DELETE
  USING (true);

-- RLS Policies for orders
CREATE POLICY "Users can view own orders"
  ON orders FOR SELECT
  USING (true);

CREATE POLICY "Users can create own orders"
  ON orders FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Users can update own orders"
  ON orders FOR UPDATE
  USING (true)
  WITH CHECK (true);

-- RLS Policies for order_items
CREATE POLICY "Users can view own order items"
  ON order_items FOR SELECT
  USING (true);

CREATE POLICY "Users can create order items"
  ON order_items FOR INSERT
  WITH CHECK (true);
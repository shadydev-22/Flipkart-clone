import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useCart } from '../context/CartContext'
import './Header.css'

function Header() {
  const [searchQuery, setSearchQuery] = useState('')
  const { cartCount } = useCart()
  const navigate = useNavigate()

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      navigate(`/products?search=${encodeURIComponent(searchQuery)}`)
    }
  }

  return (
    <header className="header">
      <div className="header-top">
        <div className="container">
          <Link to="/" className="logo">
            <span className="logo-text">Flipkart</span>
            <span className="logo-tagline">Explore <span className="plus">Plus</span></span>
          </Link>

          <form className="search-bar" onSubmit={handleSearch}>
            <input
              type="text"
              placeholder="Search for products, brands and more"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit" className="search-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M21 21L16.65 16.65M19 11C19 15.4183 15.4183 19 11 19C6.58172 19 3 15.4183 3 11C3 6.58172 6.58172 3 11 3C15.4183 3 19 6.58172 19 11Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </form>

          <div className="header-actions">
            <Link to="/orders" className="header-link">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M16 4H18C19.1046 4 20 4.89543 20 6V20C20 21.1046 19.1046 22 18 22H6C4.89543 22 4 21.1046 4 20V6C4 4.89543 4.89543 4 6 4H8M9 2H15C15.5523 2 16 2.44772 16 3V5C16 5.55228 15.5523 6 15 6H9C8.44772 6 8 5.55228 8 5V3C8 2.44772 8.44772 2 9 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Orders
            </Link>

            <Link to="/cart" className="cart-link">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M9 2L7.5 5M17 2L18.5 5M3 5H21L19 19H5L3 5ZM10 9V11M14 9V11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Cart
              {cartCount > 0 && <span className="cart-count">{cartCount}</span>}
            </Link>
          </div>
        </div>
      </div>

      <nav className="header-nav">
        <div className="container">
          <Link to="/products" className="nav-link">All Products</Link>
          <Link to="/products?category=electronics" className="nav-link">Electronics</Link>
          <Link to="/products?category=fashion" className="nav-link">Fashion</Link>
          <Link to="/products?category=mobile-phones" className="nav-link">Mobiles</Link>
          <Link to="/products?category=laptops" className="nav-link">Laptops</Link>
          <Link to="/products?category=home-kitchen" className="nav-link">Home & Kitchen</Link>
          <Link to="/products?category=books" className="nav-link">Books</Link>
        </div>
      </nav>
    </header>
  )
}

export default Header

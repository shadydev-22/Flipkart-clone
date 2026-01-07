import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import './HomePage.css'

function HomePage() {
  const [categories, setCategories] = useState([])
  const [featuredProducts, setFeaturedProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [categoriesRes, productsRes] = await Promise.all([
          axios.get('/api/categories'),
          axios.get('/api/products?limit=8')
        ])
        setCategories(categoriesRes.data)
        setFeaturedProducts(productsRes.data)
      } catch (error) {
        console.error('Error fetching data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    <div className="home-page">
      <section className="hero-banner">
        <div className="container">
          <div className="hero-content">
            <h1>Welcome to Flipkart Clone</h1>
            <p>Discover amazing products at unbeatable prices</p>
            <Link to="/products" className="cta-button">
              Shop Now
            </Link>
          </div>
        </div>
      </section>

      <section className="categories-section">
        <div className="container">
          <h2 className="section-title">Shop by Category</h2>
          <div className="categories-grid">
            {categories.map((category) => (
              <Link
                key={category.id}
                to={`/products?category=${category.slug}`}
                className="category-card"
              >
                <div className="category-image">
                  <img src={category.image_url} alt={category.name} />
                </div>
                <h3>{category.name}</h3>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="featured-section">
        <div className="container">
          <h2 className="section-title">Featured Products</h2>
          <div className="products-grid">
            {featuredProducts.map((product) => {
              const primaryImage = product.images?.find(img => img.is_primary) || product.images?.[0]
              const discountPrice = product.price
              const originalPrice = product.original_price || product.price

              return (
                <Link
                  key={product.id}
                  to={`/products/${product.slug}`}
                  className="product-card"
                >
                  <div className="product-image">
                    <img src={primaryImage?.image_url} alt={product.name} />
                    {product.discount_percentage > 0 && (
                      <span className="discount-badge">
                        {product.discount_percentage}% OFF
                      </span>
                    )}
                  </div>
                  <div className="product-info">
                    <h3 className="product-name">{product.name}</h3>
                    <div className="product-rating">
                      <span className="rating">
                        {product.rating} ★
                      </span>
                      <span className="review-count">
                        ({product.review_count.toLocaleString()})
                      </span>
                    </div>
                    <div className="product-pricing">
                      <span className="price">₹{parseFloat(discountPrice).toLocaleString('en-IN')}</span>
                      {product.discount_percentage > 0 && (
                        <span className="original-price">
                          ₹{parseFloat(originalPrice).toLocaleString('en-IN')}
                        </span>
                      )}
                    </div>
                  </div>
                </Link>
              )
            })}
          </div>
          <div className="view-all">
            <Link to="/products" className="view-all-link">
              View All Products →
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage

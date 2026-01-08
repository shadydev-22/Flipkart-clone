import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import './HomePage.css'

// Single Banner Image
const BANNER_IMAGE = "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?q=80&w=2600&auto=format&fit=crop"

// Specific order for top nav if possible
const CATEGORY_ORDER = ["Mobiles", "Fashion", "Electronics", "Home & Furniture", "Appliances", "Beauty, Toys & More"]

function HomePage() {
  const [categories, setCategories] = useState([])
  const [featuredProducts, setFeaturedProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [categoriesRes, productsRes] = await Promise.all([
          axios.get('/api/categories'),
          // Fetch more products to fill the grid
          axios.get('/api/products?limit=12')
        ])

        setCategories(Array.isArray(categoriesRes.data) ? categoriesRes.data : [])
        setFeaturedProducts(Array.isArray(productsRes.data) ? productsRes.data : [])

      } catch (error) {
        console.error('Error fetching data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  // Sort/Filter Categories for Top Nav
  const topCategories = categories.filter(c => !c.parent_id).sort((a, b) => {
    const indexA = CATEGORY_ORDER.indexOf(a.name)
    const indexB = CATEGORY_ORDER.indexOf(b.name)
    // If both are in the order list, sort by index
    if (indexA !== -1 && indexB !== -1) return indexA - indexB
    // If only A is in list, it comes first
    if (indexA !== -1) return -1
    // If only B is in list, it comes first
    if (indexB !== -1) return 1
    // Otherwise alphabetical or default
    return a.name.localeCompare(b.name)
  })

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    <div className="home-page">
      {/* Categories Bar (Flipkart Style) */}
      <section className="category-nav-section">
        <div className="category-nav">
          <Link to="/products" className="category-nav-item">
            <div className="category-icon-container">
              <img src="https://rukminim1.flixcart.com/flap/128/128/image/f15c02bfeb02d15d.png?q=100" alt="Top Offers" />
            </div>
            <span className="category-label">Top Offers</span>
          </Link>
          {topCategories.map((category) => (
            <Link key={category.id} to={`/products?category=${category.slug}`} className="category-nav-item">
              <div className="category-icon-container">
                {category.image_url ? (
                  <img src={category.image_url} alt={category.name} />
                ) : (
                  <img src="https://via.placeholder.com/64" alt={category.name} />
                )}
              </div>
              <span className="category-label">{category.name}</span>
            </Link>
          ))}
        </div>
      </section>

      {/* Hero Banner - Single Image */}
      <section className="container">
        <div className="hero-banner">
          <img
            src={BANNER_IMAGE}
            alt="Banner"
            className="banner-img"
          />
        </div>
      </section>

      {/* Structured Deals Section */}
      <section className="deals-section">
        <div className="container">
          <div className="deals-container">
            {/* Promo Side */}
            <div className="deals-promo">
              <div className="deals-promo-content">
                <h2>Best of<br />Electronics</h2>
                <Link to="/products?category=electronics" className="view-all-btn">VIEW ALL</Link>
              </div>
            </div>

            {/* Grid Side - 4 columns */}
            <div className="deals-grid-container">
              <div className="deals-grid">
                {featuredProducts.slice(0, 12).map((product) => {
                  const images = Array.isArray(product.images) ? product.images : [];
                  const primaryImage = images.find(img => img.is_primary) || images[0];

                  return (
                    <Link key={product.id} to={`/products/${product.slug}`} className="deal-card">
                      <div className="deal-image">
                        {primaryImage ? (
                          <img src={primaryImage.image_url} alt={product.name} />
                        ) : (
                          <div className="no-image">No Image</div>
                        )}
                      </div>
                      <div className="deal-info">
                        <h3 className="deal-title">{product.name}</h3>
                        <p className="deal-price">From ₹{parseFloat(product.price).toLocaleString('en-IN')}</p>
                        <p className="deal-tag">{product.brand || "Top Brand"}</p>
                      </div>
                    </Link>
                  )
                })}
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage
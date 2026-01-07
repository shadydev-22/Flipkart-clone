import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import axios from 'axios'
import './ProductListPage.css'

function ProductListPage() {
  const [searchParams] = useSearchParams()
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)

  const category = searchParams.get('category')
  const search = searchParams.get('search')

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get('/api/categories')
        setCategories(response.data)
      } catch (error) {
        console.error('Error fetching categories:', error)
      }
    }
    fetchCategories()
  }, [])

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true)
      try {
        const params = new URLSearchParams()
        if (category) params.append('category', category)
        if (search) params.append('search', search)
        params.append('limit', '50')

        const response = await axios.get(`/api/products?${params}`)
        setProducts(response.data)
      } catch (error) {
        console.error('Error fetching products:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchProducts()
  }, [category, search])

  const currentCategory = categories.find(cat => cat.slug === category)

  return (
    <div className="product-list-page">
      <div className="container">
        <div className="page-header">
          <div className="breadcrumb">
            <Link to="/">Home</Link>
            <span className="separator">›</span>
            {currentCategory && (
              <>
                <span>{currentCategory.name}</span>
              </>
            )}
            {search && (
              <>
                <span>Search Results for "{search}"</span>
              </>
            )}
            {!currentCategory && !search && (
              <>
                <span>All Products</span>
              </>
            )}
          </div>
          <h1 className="page-title">
            {search && `Search Results for "${search}"`}
            {currentCategory && currentCategory.name}
            {!currentCategory && !search && 'All Products'}
          </h1>
          <p className="result-count">{products.length} products found</p>
        </div>

        <div className="page-content">
          <aside className="filters-sidebar">
            <div className="filter-section">
              <h3 className="filter-title">Categories</h3>
              <div className="filter-options">
                <Link
                  to="/products"
                  className={`filter-option ${!category ? 'active' : ''}`}
                >
                  All Products
                </Link>
                {categories.map((cat) => (
                  <Link
                    key={cat.id}
                    to={`/products?category=${cat.slug}`}
                    className={`filter-option ${category === cat.slug ? 'active' : ''}`}
                  >
                    {cat.name}
                  </Link>
                ))}
              </div>
            </div>
          </aside>

          <main className="products-content">
            {loading ? (
              <div className="loading">Loading products...</div>
            ) : products.length === 0 ? (
              <div className="no-results">
                <h2>No products found</h2>
                <p>Try adjusting your filters or search query</p>
              </div>
            ) : (
              <div className="products-grid">
                {products.map((product) => {
                  const primaryImage = product.images?.find(img => img.is_primary) || product.images?.[0]

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
                          <span className="rating">{product.rating} ★</span>
                          <span className="review-count">
                            ({product.review_count.toLocaleString()})
                          </span>
                        </div>
                        <div className="product-pricing">
                          <span className="price">
                            ₹{parseFloat(product.price).toLocaleString('en-IN')}
                          </span>
                          {product.discount_percentage > 0 && (
                            <span className="original-price">
                              ₹{parseFloat(product.original_price).toLocaleString('en-IN')}
                            </span>
                          )}
                        </div>
                        <p className="product-brand">{product.brand}</p>
                      </div>
                    </Link>
                  )
                })}
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  )
}

export default ProductListPage

import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import axios from 'axios'
import { useWishlist } from '../context/WishlistContext'
import './ProductListPage.css'


function ProductListPage() {
  const [searchParams] = useSearchParams()
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [showFilters, setShowFilters] = useState(false)
  const { isInWishlist, toggleWishlist } = useWishlist()

  const category = searchParams.get('category')
  const search = searchParams.get('search')

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get('/api/categories')
        if (Array.isArray(response.data)) {
          setCategories(response.data)
        } else {
          console.error("Categories API returned non-array:", response.data)
          setCategories([])
        }
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
        if (Array.isArray(response.data)) {
          setProducts(response.data)
        } else {
          console.error("Products API returned non-array:", response.data)
          setProducts([])
        }
      } catch (error) {
        console.error('Error fetching products:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchProducts()
  }, [category, search])

  // Defensive check for categories array
  const currentCategory = Array.isArray(categories) ? categories.find(cat => cat.slug === category) : null;

  const toggleFilters = () => {
    setShowFilters(!showFilters)
  }

  const handleWishlistClick = (e, productId) => {
    e.preventDefault() // Prevent navigation to product detail
    e.stopPropagation()
    toggleWishlist(productId)
  }

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
          <div className="page-header-content">
            <h1 className="page-title">
              {search && `Search Results for "${search}"`}
              {currentCategory && currentCategory.name}
              {!currentCategory && !search && 'All Products'}
            </h1>
            <button className="filter-toggle-btn" onClick={toggleFilters}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M3 4H21M3 12H15M3 20H9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              Filters
            </button>
          </div>
          <p className="result-count">
            <span className="result-number">{products ? products.length : 0}</span> {products.length === 1 ? 'product' : 'products'} found
          </p>
        </div>

        <div className="page-content">
          <aside className={`filters-sidebar ${showFilters ? 'show-mobile' : ''}`}>
            <div className="filters-header">
              <h3 className="filters-title">Filters</h3>
              <button className="close-filters" onClick={toggleFilters}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </button>
            </div>

            <div className="filter-section">
              <h3 className="filter-title">CATEGORIES</h3>
              <div className="filter-options">
                <Link
                  to="/products"
                  className={`filter-option ${!category ? 'active' : ''}`}
                  onClick={() => setShowFilters(false)}
                >
                  <span>All Products</span>
                  {!category && (
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M20 6L9 17L4 12" stroke="#2874f0" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  )}
                </Link>
                {/* Render hierarchical categories */}
                {(() => {
                  if (!Array.isArray(categories)) return null;

                  // Group by parent_id
                  const roots = categories.filter(c => !c.parent_id);
                  const getChildren = (parentId) => categories.filter(c => c.parent_id === parentId);

                  return roots.map(root => {
                    const children = getChildren(root.id);
                    const isRootActive = category === root.slug;
                    const isChildActive = children.some(c => c.slug === category);
                    const shouldExpand = isRootActive || isChildActive;

                    return (
                      <div key={root.id} className="category-group">
                        <Link
                          to={`/products?category=${root.slug}`}
                          className={`filter-option ${isRootActive ? 'active' : ''} ${shouldExpand ? 'expanded' : ''}`}
                          onClick={() => setShowFilters(false)}
                        >
                          {isRootActive && (
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" className="category-arrow">
                              <path d="M15 19l-7-7 7-7" stroke="#878787" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            </svg>
                          )}
                          <span>{root.name}</span>
                        </Link>

                        {shouldExpand && children.length > 0 && (
                          <div className="subcategory-list">
                            {children.map(child => (
                              <Link
                                key={child.id}
                                to={`/products?category=${child.slug}`}
                                className={`filter-option sub-option ${category === child.slug ? 'active' : ''}`}
                                onClick={() => setShowFilters(false)}
                              >
                                <span>{child.name}</span>
                                {category === child.slug && (
                                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                                    <path d="M20 6L9 17L4 12" stroke="#2874f0" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                  </svg>
                                )}
                              </Link>
                            ))}
                          </div>
                        )}
                      </div>
                    );
                  });
                })()}
              </div>
            </div>

            {category && (
              <div className="filter-section">
                <h3 className="filter-title">PRICE</h3>
                <div className="filter-options">
                  <label className="filter-checkbox">
                    <input type="checkbox" />
                    <span>Under ₹1,000</span>
                  </label>
                  <label className="filter-checkbox">
                    <input type="checkbox" />
                    <span>₹1,000 - ₹5,000</span>
                  </label>
                  <label className="filter-checkbox">
                    <input type="checkbox" />
                    <span>₹5,000 - ₹10,000</span>
                  </label>
                  <label className="filter-checkbox">
                    <input type="checkbox" />
                    <span>₹10,000 - ₹25,000</span>
                  </label>
                  <label className="filter-checkbox">
                    <input type="checkbox" />
                    <span>Above ₹25,000</span>
                  </label>
                </div>
              </div>
            )}
          </aside>

          <main className="products-content">
            {loading ? (
              <div className="loading">
                <div className="loading-spinner"></div>
                <p>Loading products...</p>
              </div>
            ) : products && products.length === 0 ? (
              <div className="no-results">
                <svg width="80" height="80" viewBox="0 0 24 24" fill="none">
                  <circle cx="11" cy="11" r="8" stroke="#878787" strokeWidth="2" />
                  <path d="M21 21L16.65 16.65" stroke="#878787" strokeWidth="2" strokeLinecap="round" />
                  <path d="M8 11H14M11 8V14" stroke="#878787" strokeWidth="2" strokeLinecap="round" />
                </svg>
                <h2>No products found</h2>
                <p>Try adjusting your filters or search query</p>
                <Link to="/products" className="clear-filters-btn">
                  View All Products
                </Link>
              </div>
            ) : (
              <>
                <div className="products-grid">
                  {Array.isArray(products) && products.map((product) => {
                    // Safe access to images array
                    const images = Array.isArray(product.images) ? product.images : [];
                    const primaryImage = images.find(img => img.is_primary) || images[0];

                    // Safe parsing for numeric values
                    const price = typeof product.price === 'number' ? product.price : parseFloat(product.price || 0);
                    const originalPrice = typeof product.original_price === 'number' ? product.original_price : parseFloat(product.original_price || 0);

                    return (
                      <Link
                        key={product.id}
                        to={`/products/${product.slug}`}
                        className="product-card"
                      >
                        <div className="product-image">
                          {primaryImage ? (
                            <img src={primaryImage.image_url} alt={product.name} loading="lazy" />
                          ) : (
                            <div className="no-image-placeholder">No Image</div>
                          )}
                          {product.discount_percentage > 0 && (
                            <span className="discount-badge">
                              {product.discount_percentage}% OFF
                            </span>
                          )}
                          <button
                            className={`wishlist-btn ${isInWishlist(product.id) ? 'active' : ''}`}
                            onClick={(e) => handleWishlistClick(e, product.id)}
                            title={isInWishlist(product.id) ? "Remove from wishlist" : "Add to wishlist"}
                          >
                            <svg width="20" height="20" viewBox="0 0 24 24" fill={isInWishlist(product.id) ? "#ff6161" : "none"}>
                              <path d="M20.84 4.61C20.3292 4.099 19.7228 3.69364 19.0554 3.41708C18.3879 3.14052 17.6725 2.99817 16.95 2.99817C16.2275 2.99817 15.5121 3.14052 14.8446 3.41708C14.1772 3.69364 13.5708 4.099 13.06 4.61L12 5.67L10.94 4.61C9.9083 3.57831 8.50903 2.99871 7.05 2.99871C5.59096 2.99871 4.19169 3.57831 3.16 4.61C2.1283 5.64169 1.54871 7.04097 1.54871 8.5C1.54871 9.95903 2.1283 11.3583 3.16 12.39L4.22 13.45L12 21.23L19.78 13.45L20.84 12.39C21.351 11.8792 21.7563 11.2728 22.0329 10.6053C22.3095 9.93789 22.4518 9.22248 22.4518 8.5C22.4518 7.77752 22.3095 7.06211 22.0329 6.39464C21.7563 5.72718 21.351 5.12075 20.84 4.61Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            </svg>
                          </button>
                        </div>
                        <div className="product-info">
                          <div className="product-brand">{product.brand}</div>
                          <h3 className="product-name">{product.name}</h3>
                          <div className="product-rating">
                            <span className="rating">{product.rating} ★</span>
                            <span className="review-count">
                              ({(product.review_count || 0).toLocaleString()})
                            </span>
                          </div>
                          <div className="product-pricing">
                            <span className="price">
                              ₹{price.toLocaleString('en-IN')}
                            </span>
                            {product.discount_percentage > 0 && originalPrice > 0 && (
                              <>
                                <span className="original-price">
                                  ₹{originalPrice.toLocaleString('en-IN')}
                                </span>
                              </>
                            )}
                          </div>
                          {product.stock_quantity > 0 && product.stock_quantity < 10 && (
                            <div className="stock-warning">Only {product.stock_quantity} left</div>
                          )}
                        </div>
                      </Link>
                    )
                  })}
                </div>
              </>
            )}
          </main>
        </div>
      </div>
    </div>
  )
}

export default ProductListPage
import { useEffect, useState } from 'react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'
import { useCart } from '../context/CartContext'
import './ProductDetailPage.css'

function ProductDetailPage() {
  const { slug } = useParams()
  const navigate = useNavigate()
  const { addToCart } = useCart()
  const [product, setProduct] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedImage, setSelectedImage] = useState(0)
  const [addingToCart, setAddingToCart] = useState(false)

  useEffect(() => {
    const fetchProduct = async () => {
      setLoading(true)
      try {
        const response = await axios.get(`/api/products/${slug}`)
        setProduct(response.data)
      } catch (error) {
        console.error('Error fetching product:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchProduct()
  }, [slug])

  const handleAddToCart = async () => {
    setAddingToCart(true)
    const success = await addToCart(product.id)
    setAddingToCart(false)
    if (success) {
      alert('Product added to cart!')
    }
  }

  const handleBuyNow = async () => {
    setAddingToCart(true)
    const success = await addToCart(product.id)
    setAddingToCart(false)
    if (success) {
      navigate('/cart')
    }
  }

  if (loading) {
    return <div className="loading">Loading product...</div>
  }

  if (!product) {
    return (
      <div className="not-found">
        <h2>Product not found</h2>
        <Link to="/products">Back to Products</Link>
      </div>
    )
  }

  const images = product.images || []
  const sortedImages = [...images].sort((a, b) => a.display_order - b.display_order)
  const specifications = product.specifications || {}

  return (
    <div className="product-detail-page">
      <div className="container">
        <div className="breadcrumb">
          <Link to="/">Home</Link>
          <span className="separator">›</span>
          <Link to="/products">Products</Link>
          <span className="separator">›</span>
          {product.category && (
            <>
              <Link to={`/products?category=${product.category.slug}`}>
                {product.category.name}
              </Link>
              <span className="separator">›</span>
            </>
          )}
          <span>{product.name}</span>
        </div>

        <div className="product-detail-content">
          <div className="product-images-section">
            <div className="image-thumbnails">
              {sortedImages.map((image, index) => (
                <button
                  key={image.id}
                  className={`thumbnail ${selectedImage === index ? 'active' : ''}`}
                  onClick={() => setSelectedImage(index)}
                >
                  <img src={image.image_url} alt={`${product.name} ${index + 1}`} />
                </button>
              ))}
            </div>
            <div className="main-image">
              <img
                src={sortedImages[selectedImage]?.image_url}
                alt={product.name}
              />
            </div>
          </div>

          <div className="product-details-section">
            <h1 className="product-title">{product.name}</h1>
            <div className="product-brand">{product.brand}</div>

            <div className="product-rating-section">
              <span className="rating-badge">{product.rating} ★</span>
              <span className="rating-text">
                {product.review_count.toLocaleString()} Ratings & Reviews
              </span>
            </div>

            <div className="price-section">
              <div className="price-row">
                <span className="current-price">
                  ₹{parseFloat(product.price).toLocaleString('en-IN')}
                </span>
                {product.discount_percentage > 0 && (
                  <>
                    <span className="original-price">
                      ₹{parseFloat(product.original_price).toLocaleString('en-IN')}
                    </span>
                    <span className="discount-percent">
                      {product.discount_percentage}% off
                    </span>
                  </>
                )}
              </div>
            </div>

            <div className="stock-status">
              {product.stock_quantity > 0 ? (
                <span className="in-stock">In Stock ({product.stock_quantity} available)</span>
              ) : (
                <span className="out-of-stock">Out of Stock</span>
              )}
            </div>

            <div className="action-buttons">
              <button
                className="btn btn-cart"
                onClick={handleAddToCart}
                disabled={addingToCart || product.stock_quantity === 0}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M9 2L7.5 5M17 2L18.5 5M3 5H21L19 19H5L3 5ZM10 9V11M14 9V11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                {addingToCart ? 'Adding...' : 'Add to Cart'}
              </button>
              <button
                className="btn btn-buy"
                onClick={handleBuyNow}
                disabled={addingToCart || product.stock_quantity === 0}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M13 7L11 12M17 7L15 12M21 5L19 19H5L3 5H21Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                {addingToCart ? 'Processing...' : 'Buy Now'}
              </button>
            </div>

            <div className="product-description">
              <h2>Product Description</h2>
              <p>{product.description}</p>
            </div>

            {Object.keys(specifications).length > 0 && (
              <div className="product-specifications">
                <h2>Specifications</h2>
                <div className="spec-table">
                  {Object.entries(specifications).map(([key, value]) => (
                    <div key={key} className="spec-row">
                      <div className="spec-label">{key}</div>
                      <div className="spec-value">{value}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProductDetailPage

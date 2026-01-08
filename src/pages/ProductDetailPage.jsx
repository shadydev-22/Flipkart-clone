import { useEffect, useState, useRef } from 'react'
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

  // Touch/Swipe state
  const [touchStart, setTouchStart] = useState(0)
  const [touchEnd, setTouchEnd] = useState(0)
  const carouselRef = useRef(null)

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

  // Reset selected image when product changes
  useEffect(() => {
    setSelectedImage(0)
  }, [product])

  const handleTouchStart = (e) => setTouchStart(e.targetTouches[0].clientX)
  const handleTouchMove = (e) => setTouchEnd(e.targetTouches[0].clientX)
  const handleTouchEnd = () => {
    if (!product || !product.images) return
    const minSwipeDistance = 50
    const distance = touchStart - touchEnd
    if (distance > minSwipeDistance && selectedImage < product.images.length - 1) {
      setSelectedImage(selectedImage + 1)
    }
    if (distance < -minSwipeDistance && selectedImage > 0) {
      setSelectedImage(selectedImage - 1)
    }
  }

  const handleAddToCart = async () => {
    setAddingToCart(true)
    const success = await addToCart(product.id)
    setAddingToCart(false)
    if (success) {
      alert('Product added to cart!') // Simple alert for now, can be toast
    }
  }

  const handleBuyNow = async () => {
    setAddingToCart(true)
    const success = await addToCart(product.id)
    setAddingToCart(false)
    if (success) navigate('/cart')
  }

  if (loading) return <div className="loading">Loading product...</div>
  if (!product) return <div className="not-found">Product not found</div>

  const images = product.images || []
  // Ensure we have at least one valid image object or a placeholder
  const displayImages = images.length > 0 ? images : [{ image_url: '', id: 'placeholder' }];

  return (
    <div className="product-detail-page">
      <div className="container" style={{ maxWidth: '1200px', margin: '0 auto', padding: '16px' }}>

        <div className="product-layout-grid">
          {/* Left Column: Gallery */}
          <div className="product-gallery-section">
            <div className="gallery-thumbnails">
              {displayImages.map((img, idx) => (
                <div
                  key={img.id || idx}
                  className={`thumbnail-item ${selectedImage === idx ? 'active' : ''}`}
                  onMouseEnter={() => setSelectedImage(idx)}
                  onClick={() => setSelectedImage(idx)}
                >
                  {img.image_url ? (
                    <img
                      src={img.image_url}
                      alt=""
                      onError={(e) => { e.target.style.display = 'none' }}
                      referrerPolicy="no-referrer"
                    />
                  ) : (
                    <div className="thumbnail-placeholder" />
                  )}
                </div>
              ))}
            </div>

            <div
              className="gallery-main-image"
              onTouchStart={handleTouchStart}
              onTouchMove={handleTouchMove}
              onTouchEnd={handleTouchEnd}
            >
              <div className="main-image-wrapper">
                {displayImages[selectedImage]?.image_url ? (
                  <img
                    src={displayImages[selectedImage].image_url}
                    alt={product.name}
                    referrerPolicy="no-referrer"
                  />
                ) : (
                  <div className="no-image-placeholder">No Image Available</div>
                )}
              </div>

              <div className="gallery-actions">
                <button className="btn-action btn-add-cart" onClick={handleAddToCart} disabled={addingToCart}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="white"><path d="M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49c.08-.14.12-.31.12-.48 0-.55-.45-1-1-1H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z" /></svg>
                  ADD TO CART
                </button>
                <button className="btn-action btn-buy-now" onClick={handleBuyNow} disabled={addingToCart}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="white"><path d="M15 12h-2v4h2v-4zm-4 0H9v4h2v-4zm8 0h-2v4h2v-4zm-4-10H9v2h2V2zm-4 4H5v2h2V6zm8 0h-2v2h2V6zM9 16H7v2h2v-2zm-2-8H5v6h2V8zm12 0h-2v6h2V8zm-2 10h2v2h-2v-2z" /></svg>
                  BUY NOW
                </button>
              </div>
            </div>
          </div>

          {/* Right Column: Details */}
          <div className="product-info-section">
            <div className="breadcrumb-small">
              <Link to="/">Home</Link> › <Link to="/products">Products</Link> › {product.name}
            </div>

            <h1 className="product-title-large">{product.name}</h1>

            <div className="rating-box">
              <span className="rating-star">{product.rating} ★</span>
              <span className="rating-count">{product.review_count} Ratings & Reviews</span>
            </div>

            <div className="price-area">
              <h1 className="final-price">₹{product.price.toLocaleString('en-IN')}</h1>
              {product.original_price > product.price && (
                <>
                  <span className="original-price-strike">₹{product.original_price.toLocaleString('en-IN')}</span>
                  <span className="discount-off">{product.discount_percentage}% off</span>
                </>
              )}
            </div>

            <div className="available-offers">
              <h3>Available offers</h3>
              <div className="offer-line">
                <img src="https://rukminim1.flixcart.com/www/36/36/promos/06/09/2016/c22c9fc4-0555-4460-8401-bf5c28d7ba29.png?q=90" width="18" height="18" alt="" />
                <span><b>Bank Offer</b> 5% Unlimited Cashback on Flipkart Axis Bank Credit Card</span>
              </div>
              <div className="offer-line">
                <img src="https://rukminim1.flixcart.com/www/36/36/promos/06/09/2016/c22c9fc4-0555-4460-8401-bf5c28d7ba29.png?q=90" width="18" height="18" alt="" />
                <span><b>Bank Offer</b> 10% Off on Bank of Baroda Mastercard debit cards first time transaction, Terms and Condition apply</span>
              </div>
            </div>

            <div className="specifications-box">
              <h3>Specifications</h3>
              <div className="spec-grid">
                <div className="spec-row">
                  <div className="spec-key">In The Box</div>
                  <div className="spec-val">Handset, USB-C Charge Cable (1m)</div>
                </div>
                <div className="spec-row">
                  <div className="spec-key">Model Number</div>
                  <div className="spec-val">{product.slug}</div> # Just a placeholder
                </div>
                {/* Dynamic specs if available */}
                {product.specifications && Object.entries(product.specifications).map(([k, v]) => (
                  <div className="spec-row" key={k}>
                    <div className="spec-key">{k}</div>
                    <div className="spec-val">{v}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="description-box">
              <h3>Description</h3>
              <p>{product.description}</p>
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}

export default ProductDetailPage
import { Link, useNavigate } from 'react-router-dom'
import { useCart } from '../context/CartContext'
import './CartPage.css'

function CartPage() {
  const { cartItems, updateCartItem, removeFromCart, getCartTotal } = useCart()
  const navigate = useNavigate()

  const handleQuantityChange = (cartItemId, newQuantity) => {
    if (newQuantity > 0) {
      updateCartItem(cartItemId, newQuantity)
    }
  }

  const handleRemove = (cartItemId) => {
    removeFromCart(cartItemId)
  }

  const handleCheckout = () => {
    navigate('/checkout')
  }

  const cartTotal = getCartTotal()
  const deliveryCharge = cartTotal > 500 ? 0 : 40

  if (cartItems.length === 0) {
    return (
      <div className="cart-page">
        <div className="container">
          <div className="empty-cart">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none">
              <path d="M9 2L7.5 5M17 2L18.5 5M3 5H21L19 19H5L3 5ZM10 9V11M14 9V11" stroke="#878787" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <h2>Your cart is empty!</h2>
            <p>Add items to it now.</p>
            <Link to="/products" className="shop-now-btn">
              Shop Now
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="cart-page">
      <div className="container">
        <h1 className="page-title">Shopping Cart ({cartItems.length} items)</h1>

        <div className="cart-content">
          <div className="cart-items-section">
            {cartItems.map((item) => {
              const primaryImage = item.product.images?.find(img => img.is_primary) || item.product.images?.[0]
              const itemTotal = item.quantity * parseFloat(item.product.price)

              return (
                <div key={item.id} className="cart-item">
                  <Link to={`/products/${item.product.slug}`} className="item-image">
                    <img src={primaryImage?.image_url} alt={item.product.name} />
                  </Link>

                  <div className="item-details">
                    <Link to={`/products/${item.product.slug}`} className="item-name">
                      {item.product.name}
                    </Link>
                    <div className="item-brand">{item.product.brand}</div>
                    <div className="item-price">
                      <span className="price">₹{parseFloat(item.product.price).toLocaleString('en-IN')}</span>
                      {item.product.discount_percentage > 0 && (
                        <>
                          <span className="original-price">
                            ₹{parseFloat(item.product.original_price).toLocaleString('en-IN')}
                          </span>
                          <span className="discount">
                            {item.product.discount_percentage}% Off
                          </span>
                        </>
                      )}
                    </div>
                  </div>

                  <div className="item-actions">
                    <div className="quantity-controls">
                      <button
                        className="qty-btn"
                        onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                        disabled={item.quantity <= 1}
                      >
                        -
                      </button>
                      <span className="quantity">{item.quantity}</span>
                      <button
                        className="qty-btn"
                        onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                        disabled={item.quantity >= item.product.stock_quantity}
                      >
                        +
                      </button>
                    </div>

                    <div className="item-subtotal">
                      ₹{itemTotal.toLocaleString('en-IN')}
                    </div>

                    <button
                      className="remove-btn"
                      onClick={() => handleRemove(item.id)}
                    >
                      Remove
                    </button>
                  </div>
                </div>
              )
            })}
          </div>

          <div className="cart-summary-section">
            <div className="summary-card">
              <h2 className="summary-title">Price Details</h2>

              <div className="summary-row">
                <span>Price ({cartItems.length} items)</span>
                <span>₹{cartTotal.toLocaleString('en-IN')}</span>
              </div>

              <div className="summary-row">
                <span>Delivery Charges</span>
                <span className={deliveryCharge === 0 ? 'free' : ''}>
                  {deliveryCharge === 0 ? 'FREE' : `₹${deliveryCharge}`}
                </span>
              </div>

              <div className="summary-divider"></div>

              <div className="summary-row total">
                <span>Total Amount</span>
                <span>₹{(cartTotal + deliveryCharge).toLocaleString('en-IN')}</span>
              </div>

              {cartTotal > 500 && (
                <div className="savings-message">
                  You will save ₹{deliveryCharge} on this order
                </div>
              )}

              <button className="checkout-btn" onClick={handleCheckout}>
                Place Order
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CartPage

import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import axios from 'axios'
import './OrderConfirmationPage.css'

function OrderConfirmationPage() {
  const { orderId } = useParams()
  const [order, setOrder] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchOrder = async () => {
      try {
        const response = await axios.get(`/api/orders/${orderId}`)
        setOrder(response.data)
      } catch (error) {
        console.error('Error fetching order:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchOrder()
  }, [orderId])

  if (loading) {
    return <div className="loading">Loading order details...</div>
  }

  if (!order) {
    return (
      <div className="not-found">
        <h2>Order not found</h2>
        <Link to="/orders">View All Orders</Link>
      </div>
    )
  }

  return (
    <div className="order-confirmation-page">
      <div className="container">
        <div className="confirmation-card">
          <div className="success-icon">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="#388e3c" strokeWidth="2" />
              <path d="M8 12L11 15L16 9" stroke="#388e3c" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>

          <h1 className="confirmation-title">Order Placed Successfully!</h1>
          <p className="confirmation-message">
            Thank you for your order. Your order has been placed successfully.
          </p>

          <div className="order-details-card">
            <div className="order-detail-row">
              <span className="label">Order Number:</span>
              <span className="value">{order.order_number}</span>
            </div>
            <div className="order-detail-row">
              <span className="label">Total Amount:</span>
              <span className="value">₹{parseFloat(order.total_amount).toLocaleString('en-IN')}</span>
            </div>
            <div className="order-detail-row">
              <span className="label">Payment Method:</span>
              <span className="value">
                {order.payment_method === 'cod' ? 'Cash on Delivery' : order.payment_method}
              </span>
            </div>
            <div className="order-detail-row">
              <span className="label">Status:</span>
              <span className="value status">{order.status}</span>
            </div>
          </div>

          <div className="delivery-address-card">
            <h3>Delivery Address</h3>
            {order.address && (
              <div className="address-details">
                <p className="address-name">{order.address.full_name}</p>
                <p>{order.address.address_line1}</p>
                {order.address.address_line2 && <p>{order.address.address_line2}</p>}
                <p>{order.address.city}, {order.address.state} - {order.address.pincode}</p>
                <p>Phone: {order.address.phone}</p>
              </div>
            )}
          </div>

          <div className="order-items-card">
            <h3>Order Items</h3>
            <div className="order-items-list">
              {order.items.map((item) => {
                const primaryImage = item.product?.images?.find(img => img.is_primary) || item.product?.images?.[0]

                return (
                  <div key={item.id} className="order-item">
                    {item.product && (
                      <>
                        <img src={primaryImage?.image_url} alt={item.product.name} />
                        <div className="item-info">
                          <div className="item-name">{item.product.name}</div>
                          <div className="item-qty">Quantity: {item.quantity}</div>
                        </div>
                        <div className="item-price">
                          ₹{(item.quantity * parseFloat(item.price_at_purchase)).toLocaleString('en-IN')}
                        </div>
                      </>
                    )}
                  </div>
                )
              })}
            </div>
          </div>

          <div className="action-buttons">
            <Link to="/orders" className="btn btn-secondary">
              View All Orders
            </Link>
            <Link to="/products" className="btn btn-primary">
              Continue Shopping
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default OrderConfirmationPage

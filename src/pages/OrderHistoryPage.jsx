import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import './OrderHistoryPage.css'

function OrderHistoryPage() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await axios.get('/api/orders')
        setOrders(response.data)
      } catch (error) {
        console.error('Error fetching orders:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchOrders()
  }, [])

  if (loading) {
    return <div className="loading">Loading orders...</div>
  }

  if (orders.length === 0) {
    return (
      <div className="order-history-page">
        <div className="container">
          <div className="empty-orders">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none">
              <path d="M16 4H18C19.1046 4 20 4.89543 20 6V20C20 21.1046 19.1046 22 18 22H6C4.89543 22 4 21.1046 4 20V6C4 4.89543 4.89543 4 6 4H8M9 2H15C15.5523 2 16 2.44772 16 3V5C16 5.55228 15.5523 6 15 6H9C8.44772 6 8 5.55228 8 5V3C8 2.44772 8.44772 2 9 2Z" stroke="#878787" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <h2>No orders yet</h2>
            <p>You haven't placed any orders.</p>
            <Link to="/products" className="shop-now-btn">
              Start Shopping
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="order-history-page">
      <div className="container">
        <h1 className="page-title">My Orders</h1>

        <div className="orders-list">
          {orders.map((order) => {
            const orderDate = new Date(order.created_at).toLocaleDateString('en-IN', {
              day: 'numeric',
              month: 'short',
              year: 'numeric'
            })

            return (
              <div key={order.id} className="order-card">
                <div className="order-header">
                  <div className="order-info">
                    <div className="order-number">Order #{order.order_number}</div>
                    <div className="order-date">Placed on {orderDate}</div>
                  </div>
                  <div className="order-status-badge">
                    <span className={`status ${order.status}`}>{order.status}</span>
                  </div>
                </div>

                <div className="order-items">
                  {order.items.map((item) => {
                    const primaryImage = item.product?.images?.find(img => img.is_primary) || item.product?.images?.[0]

                    return (
                      <div key={item.id} className="order-item">
                        {item.product && (
                          <>
                            <img src={primaryImage?.image_url} alt={item.product.name} />
                            <div className="item-details">
                              <Link
                                to={`/products/${item.product.slug}`}
                                className="item-name"
                              >
                                {item.product.name}
                              </Link>
                              <div className="item-qty">Quantity: {item.quantity}</div>
                              <div className="item-price">
                                ₹{(item.quantity * parseFloat(item.price_at_purchase)).toLocaleString('en-IN')}
                              </div>
                            </div>
                          </>
                        )}
                      </div>
                    )
                  })}
                </div>

                <div className="order-footer">
                  <div className="order-total">
                    <span>Total Amount:</span>
                    <span className="amount">
                      ₹{parseFloat(order.total_amount).toLocaleString('en-IN')}
                    </span>
                  </div>
                  <Link
                    to={`/order-confirmation/${order.id}`}
                    className="view-details-btn"
                  >
                    View Details
                  </Link>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default OrderHistoryPage

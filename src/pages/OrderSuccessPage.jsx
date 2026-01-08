import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import './ProductListPage.css'; // Reusing some styles
import './ProductDetailPage.css';

const OrderSuccessPage = () => {
    const { orderId } = useParams();
    const [order, setOrder] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchOrder = async () => {
            try {
                const response = await axios.get(`/api/orders/${orderId}`);
                setOrder(response.data);
            } catch (err) {
                setError('Failed to load order details');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        if (orderId) {
            fetchOrder();
        }
    }, [orderId]);

    if (loading) return <div className="loading">Loading order details...</div>;
    if (error) return <div className="error-message">{error}</div>;
    if (!order) return <div className="error-message">Order not found</div>;

    return (
        <div className="page-container">
            <div className="order-success-container" style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
                <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    <div style={{ color: '#2874f0', fontSize: '4rem', marginBottom: '1rem' }}>✓</div>
                    <h1>Order Placed Successfully!</h1>
                    <p>Thank you for your purchase. Your order ID is <strong>{order.id}</strong></p>
                </div>

                <div className="order-details-card" style={{ background: 'white', padding: '1.5rem', borderRadius: '4px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
                    <h2>Order Summary</h2>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem', borderBottom: '1px solid #f0f0f0', paddingBottom: '1rem' }}>
                        <span>Status:</span>
                        <span style={{ color: 'green', fontWeight: 'bold' }}>{order.status}</span>
                    </div>

                    <h3>Items</h3>
                    <div className="order-items-list">
                        {order.items.map((item) => (
                            <div key={item.id} style={{ display: 'flex', gap: '1rem', marginBottom: '1rem', borderBottom: '1px solid #f0f0f0', paddingBottom: '1rem' }}>
                                <img
                                    src={item.product.images?.[0]?.image_url}
                                    alt={item.product.name}
                                    style={{ width: '80px', height: '80px', objectFit: 'contain' }}
                                />
                                <div style={{ flex: 1 }}>
                                    <Link to={`/products/${item.product.slug}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                                        <h4>{item.product.name}</h4>
                                    </Link>
                                    <p>Quantity: {item.quantity}</p>
                                    <p>Price: ₹{item.price_at_purchase.toLocaleString()}</p>
                                </div>
                                <div style={{ fontWeight: 'bold' }}>
                                    ₹{(item.quantity * item.price_at_purchase).toLocaleString()}
                                </div>
                            </div>
                        ))}
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '1rem', fontSize: '1.2rem', fontWeight: 'bold' }}>
                        <span>Total Amount:</span>
                        <span>₹{order.total_amount.toLocaleString()}</span>
                    </div>
                </div>

                <div style={{ textAlign: 'center', marginTop: '2rem' }}>
                    <Link to="/" className="add-to-cart-btn" style={{ textDecoration: 'none', display: 'inline-block' }}>
                        Continue Shopping
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default OrderSuccessPage;

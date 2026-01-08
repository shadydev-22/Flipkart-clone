import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './ProfilePage.css';

const ProfilePage = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const response = await axios.get('/api/orders');
                setOrders(response.data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchOrders();
    }, []);

    if (loading) return <div className="loading" style={{ height: '60vh' }}>Loading...</div>;

    const user = {
        name: "Test User",
        email: "test@example.com",
        profileImage: "https://static-assets-web.flixcart.com/fk-p-linchpin-web/fk-cp-zion/img/profile-pic-male_4811a1.svg"
    };

    return (
        <div className="profile-container">
            {/* Sidebar */}
            <aside className="profile-sidebar">
                <div className="profile-user-card">
                    <div className="profile-avatar">
                        <img src={user.profileImage} alt="Profile" />
                    </div>
                    <div>
                        <div className="profile-name-small">Hello,</div>
                        <div className="profile-name-large">{user.name}</div>
                    </div>
                </div>
                <div className="sidebar-menu">
                    <Link to="/profile" className="sidebar-item active">MY ORDERS</Link>
                    <div className="sidebar-item">ACCOUNT SETTINGS</div>
                    <div className="sidebar-item">PAYMENTS</div>
                    <div className="sidebar-item">MY CHATS</div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="profile-main">
                <h1 className="profile-header">My Orders</h1>

                {orders.length === 0 ? (
                    <div className="empty-state">
                        <img src="https://rukminim1.flixcart.com/www/800/800/promos/16/05/2019/d438a32e-765a-4d8b-b4a6-520b560971e8.png?q=90" alt="Empty" />
                        <h3>You have no orders</h3>
                        <Link to="/" className="view-all-btn">Start Shopping</Link>
                    </div>
                ) : (
                    orders.map(order => (
                        <Link to={`/order-confirmation/${order.id}`} key={order.id} className="order-card" style={{ textDecoration: 'none', color: 'inherit', cursor: 'pointer' }}>
                            <div className="order-details">
                                <div className="order-image-container">
                                    {order.items[0]?.product?.images?.[0]?.image_url ? (
                                        <img src={order.items[0].product.images[0].image_url} alt="Product" />
                                    ) : (
                                        <div style={{ width: '100%', height: '100%', background: '#f0f0f0' }}></div>
                                    )}
                                </div>
                                <div className="order-info">
                                    <div className="order-product-name">
                                        {order.items[0]?.product?.name || "Product Name"}
                                    </div>
                                    <div className="order-meta">
                                        {order.items.length > 1 ? `& ${order.items.length - 1} more items` : `Qty: ${order.items[0]?.quantity}`}
                                    </div>
                                    <div className="order-price">₹{order.total_amount.toLocaleString()}</div>
                                </div>
                            </div>

                            <div className="order-status">
                                <div className="status-badge">
                                    <div className="status-dot"></div>
                                    {order.status}
                                </div>
                                <div className="order-meta">
                                    Order ID: {order.id.slice(0, 8).toUpperCase()}
                                </div>
                            </div>
                        </Link>
                    ))
                )}
            </main>
        </div>
    );
};

export default ProfilePage;

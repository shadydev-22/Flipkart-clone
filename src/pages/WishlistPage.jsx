import { Link } from 'react-router-dom'
import { useWishlist } from '../context/WishlistContext'
import { useCart } from '../context/CartContext'
import './WishlistPage.css'

function WishlistPage() {
    const { wishlistItems, removeFromWishlist, loading } = useWishlist()
    const { addToCart } = useCart()

    const handleAddToCart = async (productId) => {
        const success = await addToCart(productId, 1)
        if (success) {
            // Optionally remove from wishlist after adding to cart
            // await removeFromWishlist(productId)
        }
    }

    const handleRemove = (productId) => {
        removeFromWishlist(productId)
    }

    if (loading && wishlistItems.length === 0) {
        return <div className="loading">Loading wishlist...</div>
    }

    if (wishlistItems.length === 0) {
        return (
            <div className="wishlist-page">
                <div className="container">
                    <div className="empty-wishlist">
                        <svg width="80" height="80" viewBox="0 0 24 24" fill="none">
                            <path d="M20.84 4.61C20.3292 4.099 19.7228 3.69364 19.0554 3.41708C18.3879 3.14052 17.6725 2.99817 16.95 2.99817C16.2275 2.99817 15.5121 3.14052 14.8446 3.41708C14.1772 3.69364 13.5708 4.099 13.06 4.61L12 5.67L10.94 4.61C9.9083 3.57831 8.50903 2.99871 7.05 2.99871C5.59096 2.99871 4.19169 3.57831 3.16 4.61C2.1283 5.64169 1.54871 7.04097 1.54871 8.5C1.54871 9.95903 2.1283 11.3583 3.16 12.39L4.22 13.45L12 21.23L19.78 13.45L20.84 12.39C21.351 11.8792 21.7563 11.2728 22.0329 10.6053C22.3095 9.93789 22.4518 9.22248 22.4518 8.5C22.4518 7.77752 22.3095 7.06211 22.0329 6.39464C21.7563 5.72718 21.351 5.12075 20.84 4.61Z" stroke="#878787" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                        <h2>Your wishlist is empty!</h2>
                        <p>Add items you like to your wishlist. Review them anytime and easily move them to cart.</p>
                        <Link to="/products" className="shop-now-btn">
                            Shop Now
                        </Link>
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="wishlist-page">
            <div className="container">
                <h1 className="page-title">My Wishlist ({wishlistItems.length} items)</h1>

                <div className="wishlist-grid">
                    {wishlistItems.map((item) => {
                        const primaryImage = item.product.images?.find(img => img.is_primary) || item.product.images?.[0]
                        const price = parseFloat(item.product.price)
                        const originalPrice = parseFloat(item.product.original_price || 0)

                        return (
                            <div key={item.id} className="wishlist-card">
                                <button
                                    className="remove-wishlist-btn"
                                    onClick={() => handleRemove(item.product.id)}
                                    title="Remove from wishlist"
                                >
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                                        <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                    </svg>
                                </button>

                                <Link to={`/products/${item.product.slug}`} className="wishlist-product-link">
                                    <div className="wishlist-image">
                                        {primaryImage ? (
                                            <img src={primaryImage.image_url} alt={item.product.name} />
                                        ) : (
                                            <div className="no-image-placeholder">No Image</div>
                                        )}
                                        {item.product.discount_percentage > 0 && (
                                            <span className="discount-badge">
                                                {item.product.discount_percentage}% OFF
                                            </span>
                                        )}
                                    </div>

                                    <div className="wishlist-info">
                                        <div className="wishlist-brand">{item.product.brand}</div>
                                        <h3 className="wishlist-name">{item.product.name}</h3>
                                        <div className="wishlist-pricing">
                                            <span className="price">₹{price.toLocaleString('en-IN')}</span>
                                            {item.product.discount_percentage > 0 && originalPrice > 0 && (
                                                <>
                                                    <span className="original-price">
                                                        ₹{originalPrice.toLocaleString('en-IN')}
                                                    </span>
                                                    <span className="discount-text">
                                                        {item.product.discount_percentage}% off
                                                    </span>
                                                </>
                                            )}
                                        </div>
                                    </div>
                                </Link>

                                <button
                                    className="add-to-cart-btn"
                                    onClick={() => handleAddToCart(item.product.id)}
                                    disabled={item.product.stock_quantity === 0}
                                >
                                    {item.product.stock_quantity === 0 ? 'Out of Stock' : 'Add to Cart'}
                                </button>
                            </div>
                        )
                    })}
                </div>
            </div>
        </div>
    )
}

export default WishlistPage

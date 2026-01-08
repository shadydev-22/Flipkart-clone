import { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

const WishlistContext = createContext()

export const useWishlist = () => {
    const context = useContext(WishlistContext)
    if (!context) {
        throw new Error('useWishlist must be used within a WishlistProvider')
    }
    return context
}

export const WishlistProvider = ({ children }) => {
    const [wishlistItems, setWishlistItems] = useState([])
    const [wishlistCount, setWishlistCount] = useState(0)
    const [loading, setLoading] = useState(false)

    const fetchWishlist = async () => {
        try {
            const response = await axios.get('/api/wishlist')
            setWishlistItems(response.data)
            setWishlistCount(response.data.length)
        } catch (error) {
            console.error('Error fetching wishlist:', error)
        }
    }

    useEffect(() => {
        fetchWishlist()
    }, [])

    const addToWishlist = async (productId) => {
        setLoading(true)
        try {
            await axios.post('/api/wishlist', null, { params: { product_id: productId } })
            await fetchWishlist()
            return true
        } catch (error) {
            console.error('Error adding to wishlist:', error)
            return false
        } finally {
            setLoading(false)
        }
    }

    const removeFromWishlist = async (productId) => {
        setLoading(true)
        try {
            await axios.delete(`/api/wishlist/${productId}`)
            await fetchWishlist()
        } catch (error) {
            console.error('Error removing from wishlist:', error)
        } finally {
            setLoading(false)
        }
    }

    const isInWishlist = (productId) => {
        return wishlistItems.some(item => item.product.id === productId)
    }

    const toggleWishlist = async (productId) => {
        if (isInWishlist(productId)) {
            await removeFromWishlist(productId)
        } else {
            await addToWishlist(productId)
        }
    }

    return (
        <WishlistContext.Provider
            value={{
                wishlistItems,
                wishlistCount,
                loading,
                addToWishlist,
                removeFromWishlist,
                isInWishlist,
                toggleWishlist,
                fetchWishlist
            }}
        >
            {children}
        </WishlistContext.Provider>
    )
}

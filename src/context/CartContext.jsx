import { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

const CartContext = createContext()

export const useCart = () => {
  const context = useContext(CartContext)
  if (!context) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([])
  const [cartCount, setCartCount] = useState(0)
  const [loading, setLoading] = useState(false)

  const fetchCart = async () => {
    try {
      const response = await axios.get('/api/cart')
      setCartItems(response.data)
      setCartCount(response.data.reduce((sum, item) => sum + item.quantity, 0))
    } catch (error) {
      console.error('Error fetching cart:', error)
    }
  }

  useEffect(() => {
    fetchCart()
  }, [])

  const addToCart = async (productId, quantity = 1) => {
    setLoading(true)
    try {
      await axios.post('/api/cart', { product_id: productId, quantity })
      await fetchCart()
      return true
    } catch (error) {
      console.error('Error adding to cart:', error)
      return false
    } finally {
      setLoading(false)
    }
  }

  const updateCartItem = async (cartItemId, quantity) => {
    setLoading(true)
    try {
      await axios.patch(`/api/cart/${cartItemId}`, { quantity })
      await fetchCart()
    } catch (error) {
      console.error('Error updating cart:', error)
    } finally {
      setLoading(false)
    }
  }

  const removeFromCart = async (cartItemId) => {
    setLoading(true)
    try {
      await axios.delete(`/api/cart/${cartItemId}`)
      await fetchCart()
    } catch (error) {
      console.error('Error removing from cart:', error)
    } finally {
      setLoading(false)
    }
  }

  const clearCart = async () => {
    setLoading(true)
    try {
      await axios.delete('/api/cart')
      setCartItems([])
      setCartCount(0)
    } catch (error) {
      console.error('Error clearing cart:', error)
    } finally {
      setLoading(false)
    }
  }

  const getCartTotal = () => {
    return cartItems.reduce(
      (sum, item) => {
        if (!item.product || !item.product.price) return sum
        return sum + (item.quantity * parseFloat(item.product.price))
      },
      0
    )
  }

  return (
    <CartContext.Provider
      value={{
        cartItems,
        cartCount,
        loading,
        addToCart,
        updateCartItem,
        removeFromCart,
        clearCart,
        fetchCart,
        getCartTotal
      }}
    >
      {children}
    </CartContext.Provider>
  )
}

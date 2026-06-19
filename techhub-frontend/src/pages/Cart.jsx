import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';

const Cart = () => {
  const { cart, removeFromCart, clearCart, cartTotal } = useCart();
  const navigate = useNavigate();

  const handleCheckout = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    const orderData = {
      items: cart.map((item) => ({
        product_id: item.id,
        quantity: item.quantity,
      })),
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/api/order/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify(orderData),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Checkout failed');
      }

      const data = await response.json();
      alert(`Order placed successfully! Order ID: ${data.order_id}`);
      clearCart();
      navigate('/');
    } catch (err) {
      console.error('Checkout failed:', err);
      alert(err.message || 'There was an error processing your order.');
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4">Your Shopping Cart</h2>
      <div className="row">
        <div className="col-md-8">
          <ul className="list-group shadow-sm">
            {cart.map((item) => (
              <li key={item.id} className="list-group-item d-flex justify-content-between align-items-center p-3">
                <div>
                  <h6 className="my-0">{item.name}</h6>
                  <small className="text-muted">Quantity: {item.quantity} x ${item.price}</small>
                </div>
                <div>
                  <span className="text-primary fw-bold me-3">${(item.price * item.quantity).toFixed(2)}</span>
                  <button 
                    className="btn btn-sm btn-outline-danger" 
                    onClick={() => removeFromCart(item.id)}
                  >
                    Remove
                  </button>
                </div>
              </li>
            ))}
            {cart.length === 0 && <li className="list-group-item text-center p-5">Your cart is empty.</li>}
          </ul>
        </div>

        {/* Checkout Summary Block */}
        <div className="col-md-4">
          <div className="card shadow-sm border-primary">
            <div className="card-body">
              <h5 className="card-title">Order Summary</h5>
              <hr />
              <div className="d-flex justify-content-between mb-3">
                <span>Total:</span>
                <span className="h4 text-primary">${cartTotal.toFixed(2)}</span>
              </div>
              <button 
                className="btn btn-primary w-100 btn-lg" 
                disabled={cart.length === 0}
                onClick={handleCheckout}
              >
                Proceed to Checkout
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;
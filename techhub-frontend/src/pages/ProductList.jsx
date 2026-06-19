import React, { useEffect, useState } from 'react';
import { useCart } from '../context/CartContext';
import { useNavigate } from 'react-router-dom';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { addToCart } = useCart();
  const navigate = useNavigate();

  useEffect(() => {
    const loadProducts = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/products/');
        if (!response.ok) {
          throw new Error('Failed to load products');
        }

        const data = await response.json();
        setProducts(data);
      } catch (err) {
        console.error(err);
        setError('Unable to load products from Django backend.');
      } finally {
        setLoading(false);
      }
    };

    loadProducts();
  }, []);

  const handleAddToCart = (product) => {
    addToCart({
      id: product.id,
      name: product.name,
      price: Number(product.price),
    });
  };

  if (loading) {
    return <div className="container mt-5">Loading products...</div>;
  }

  if (error) {
    return <div className="container mt-5 text-danger">{error}</div>;
  }

  return (
    <div className="container mt-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 className="mb-1">TechHub Store</h1>
          <p className="text-muted">Data powered by the Django backend.</p>
        </div>
        <button className="btn btn-outline-primary" onClick={() => navigate('/cart')}>
          View Cart
        </button>
      </div>

      <div className="row gy-4">
        {products.map((product) => (
          <div key={product.id} className="col-md-4">
            <div className="card h-100 shadow-sm">
              <div className="card-body">
                <h5 className="card-title">{product.name}</h5>
                <p className="card-text text-truncate" style={{ minHeight: '3rem' }}>
                  {product.description || 'No description available.'}
                </p>
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <span className="fw-bold">${Number(product.price).toFixed(2)}</span>
                  <span className="badge bg-secondary">{product.stock} in stock</span>
                </div>
                <button
                  className="btn btn-primary w-100"
                  disabled={product.stock <= 0}
                  onClick={() => handleAddToCart(product)}
                >
                  Add to Cart
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductList;

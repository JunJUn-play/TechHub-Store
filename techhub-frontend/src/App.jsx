import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ProtectedRoute from './src/components/ProtectedRoute';
import Dashboard from './src/components/Dashboard';
import ProductList from './pages/ProductList';
import Login from './pages/Login';
import Register from './pages/Register';
import Cart from './pages/Cart';
import Unauthorized from './pages/Unauthorized';

function App() {
  const [user, setUser] = useState(() => ({
    loggedIn: Boolean(localStorage.getItem('token')),
    role: localStorage.getItem('role') || 'customer',
    username: localStorage.getItem('username') || '',
    token: localStorage.getItem('token') || '',
  }));

  const handleLogout = async () => {
    const token = localStorage.getItem('token');

    if (token) {
      try {
        await fetch('http://127.0.0.1:8000/api/auth/logout/', {
          method: 'POST',
          headers: {
            Authorization: `Token ${token}`,
          },
        });
      } catch (err) {
        console.warn('Logout request failed:', err);
      }
    }

    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('username');
    setUser({ loggedIn: false, role: 'customer', username: '', token: '' });
  };

  return (
    <Router>
      <header className="bg-dark text-white py-3">
        <div className="container d-flex justify-content-between align-items-center">
          <div>
            <Link to="/" className="text-white text-decoration-none fs-4">
              TechHub
            </Link>
            <span className="text-muted ms-3">JSX + Django Store</span>
          </div>
          <div className="d-flex gap-2 align-items-center">
            <Link to="/cart" className="btn btn-outline-light btn-sm">
              Cart
            </Link>
            {user.loggedIn ? (
              <>
                <span className="text-light small">{user.username}</span>
                <button onClick={handleLogout} className="btn btn-outline-light btn-sm">
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="btn btn-outline-light btn-sm">
                  Login
                </Link>
                <Link to="/register" className="btn btn-light btn-sm text-dark">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </header>
      <Routes>
        {/* PUBLIC ROUTES */}
        <Route path="/" element={<ProductList />} />
        <Route path="/login" element={<Login setUser={setUser} />} />
        <Route path="/register" element={<Register />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/unauthorized" element={<h1>Access Denied: You do not have permission.</h1>} />

        {/* STAFF & ADMIN ONLY ROUTES */}
        <Route element={<ProtectedRoute user={user} allowedRoles={['staff', 'admin']} />}>
          <Route path="/dashboard" element={<Dashboard user={user} />} />
          <Route path="/inventory" element={<h1>Manage Stock</h1>} />
        </Route>

        {/* ADMIN ONLY ROUTES */}
        <Route element={<ProtectedRoute user={user} allowedRoles={['admin']} />}>
          <Route path="/admin-settings" element={<h1>System Configuration</h1>} />
          <Route path="/unauthorized" element={<Unauthorized />} />
        </Route>

      </Routes>
    </Router>
  );
}

export default App;

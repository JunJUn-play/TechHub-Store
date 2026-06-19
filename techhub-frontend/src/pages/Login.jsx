import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Login = ({ setUser }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        const data = await response.json();
        setError(data.detail || 'Invalid credentials');
        return;
      }

      const data = await response.json();
      localStorage.setItem('token', data.token);
      localStorage.setItem('role', data.role);
      localStorage.setItem('username', data.username);

      setUser({
        loggedIn: true,
        role: data.role,
        username: data.username,
        token: data.token,
      });
      navigate('/');
    } catch (err) {
      console.error(err);
      setError('Login failed. Please try again.');
    }
  };

  return (
    <div className="container vh-100 d-flex align-items-center justify-content-center">
      <div className="card shadow-sm p-4" style={{ maxWidth: '480px', width: '100%' }}>
        <h2 className="mb-4">TechHub Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="username" className="form-label">Username</label>
            <input
              id="username"
              className="form-control"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              required
            />
          </div>

          <div className="mb-3">
            <label htmlFor="password" className="form-label">Password</label>
            <input
              id="password"
              type="password"
              className="form-control"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
          </div>

          {error && <div className="alert alert-danger">{error}</div>}

          <button type="submit" className="btn btn-primary w-100">
            Sign In
          </button>
        </form>

        <div className="mt-4 text-center">
          <span className="text-muted">Need an account?</span>{' '}
          <Link to="/register">Register here</Link>
        </div>
      </div>
    </div>
  );
};

export default Login;

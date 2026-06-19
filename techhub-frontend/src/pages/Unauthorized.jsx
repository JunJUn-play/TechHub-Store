import React from 'react';
import { useNavigate } from 'react-router-dom';

const Unauthorized = () => {
  const navigate = useNavigate();

  return (
    <div className="container vh-100 d-flex align-items-center justify-content-center">
      <div className="text-center p-5 shadow-lg rounded-4 bg-white border-top border-5 border-danger" style={{ maxWidth: '500px' }}>
        {/* Bootstrap Icon or Emoji */}
        <div className="display-1 text-danger mb-4">
          <i className="bi bi-shield-lock-fill"></i> 🔒
        </div>
        
        <h1 className="fw-bold text-dark">Access Denied</h1>
        <p className="text-muted mb-4">
          Oops! It looks like you don't have the required permissions to view the 
          <strong> TechHub Management Portal</strong>.
        </p>

        <div className="d-grid gap-2">
          <button 
            onClick={() => navigate('/')} 
            className="btn btn-primary btn-lg shadow-sm"
          >
            Back to Store
          </button>
          
          <button 
            onClick={() => navigate('/login')} 
            className="btn btn-outline-secondary"
          >
            Login with Different Account
          </button>
        </div>

        <p className="mt-4 small text-secondary">
          Error Code: 403 Forbidden | TechHub Security Layer
        </p>
      </div>
    </div>
  );
};

export default Unauthorized;
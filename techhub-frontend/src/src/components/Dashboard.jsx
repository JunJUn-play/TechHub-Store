// src/components/Dashboard.jsx
import React from 'react';

const Dashboard = ({ user }) => {
  // Styles mirroring the "TechHub" dark theme from your diagram
  const cardHeaderStyle = {
    backgroundColor: '#0b1120',
    color: '#007bff',
    fontWeight: 'bold'
  };

  return (
    <div className="container py-5">
      <div className="row mb-4">
        <div className="col">
          <h2 className="border-bottom pb-2">
            System Interface: <span className="text-primary">{user.role.toUpperCase()}</span>
          </h2>
        </div>
      </div>

      {/* --- ADMIN VIEW --- */}
      {user.role === 'admin' && (
        <div className="row g-4">
          <div className="col-md-4">
            <div className="card shadow-sm border-danger">
              <div className="card-body">
                <h5 className="card-title text-danger">User Management</h5>
                <p className="card-text">Authorize Staff and Manage Customer accounts.</p>
                <button className="btn btn-danger">Manage Users</button>
              </div>
            </div>
          </div>
          <div className="col-md-8">
            <div className="card shadow-sm">
              <div className="card-header" style={cardHeaderStyle}>System Health & Reports</div>
              <div className="card-body">
                <p>Full access to database records and transaction logs.</p>
                <div className="alert alert-info">SQLite Database Connection: Active</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* --- STAFF VIEW --- */}
      {user.role === 'staff' && (
        <div className="card shadow-sm">
          <div className="card-header bg-warning text-dark fw-bold">Inventory & Order Processing</div>
          <div className="card-body">
            <table className="table table-striped align-middle">
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Gaming Laptop X1</td>
                  <td><span className="badge bg-success">In Stock</span></td>
                  <td><button className="btn btn-sm btn-outline-dark">Update Stock</button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* --- CUSTOMER VIEW --- */}
      {user.role === 'customer' && (
        <div className="row">
          <div className="col-md-12">
            <div className="p-5 mb-4 bg-light rounded-3 shadow-sm border border-primary">
              <div className="container-fluid py-5">
                <h1 className="display-5 fw-bold text-dark">Welcome to TechHub</h1>
                <p className="col-md-8 fs-4 text-secondary">Browse our high-performance components and track your current orders.</p>
                <button className="btn btn-primary btn-lg" type="button">Shop Now</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
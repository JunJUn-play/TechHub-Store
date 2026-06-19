import React from 'react';

const Navbar = ({ user }) => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark border-bottom border-primary">
      <div className="container-fluid">
        <a className="navbar-brand fw-bold" href="#">TECH<span className="text-primary">HUB</span></a>
        
        <div className="navbar-nav ms-auto">
          {/* Universal Link */}
          <a className="nav-link" href="/">Store</a>

          {/* CUSTOMER: Browse & Orders */}
          {user.role === 'customer' && (
            <>
              <a className="nav-link" href="/my-orders">My Orders</a>
              <a className="nav-link btn btn-primary btn-sm text-white ms-2" href="/cart">Cart 🛒</a>
            </>
          )}

          {/* STAFF: Inventory & Processing */}
          {user.role === 'staff' && (
            <a className="nav-link text-warning" href="/staff/orders">Process Orders</a>
          )}

          {/* ADMIN: Full Management */}
          {user.role === 'admin' && (
            <>
              <a className="nav-link text-info" href="/admin/users">Manage Users</a>
              <a className="nav-link text-danger" href="/admin/reports">Financials</a>
            </>
          )}

          <span className="navbar-text ms-3 text-secondary">| {user.username}</span>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
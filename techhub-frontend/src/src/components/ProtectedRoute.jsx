import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

/**
 * @param {Object} user - The current user object from state/context
 * @param {Array} allowedRoles - List of roles permitted to view this route
 */
const ProtectedRoute = ({ user, allowedRoles }) => {
  
  // 1. Check if user is logged in
  if (!user || !user.loggedIn) {
    return <Navigate to="/login" replace />;
  }

  // 2. Check if user's role is in the allowed list
  if (!allowedRoles.includes(user.role)) {
    // Redirect unauthorized users to a 'Forbidden' or Home page
    return <Navigate to="/unauthorized" replace />;
  }

  // 3. If all checks pass, render the child component (the Dashboard)
  return <Outlet />;
};

export default ProtectedRoute;
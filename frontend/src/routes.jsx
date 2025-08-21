import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Login.jsx";
import Patients from "./components/Patients.jsx";
import CalendarView from "./components/CalendarView.jsx";
import Signup from "./components/Signup.jsx";

// Protected route component
const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem("token");
  if (!token) return <Navigate to="/login" replace />;
  return children;
};

const RoutesComponent = () => {
  return (
    <Routes>
       {/* Public routes */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Signup />} />  {/* <-- add this */}
      <Route
        path="/patients"
        element={
          <ProtectedRoute>
            <Patients />
          </ProtectedRoute>
        }
      />
      <Route
        path="/therapies"
        element={
          <ProtectedRoute>
            <CalendarView />
          </ProtectedRoute>
        }
      />
      {/* Default redirect */}
      <Route path="*" element={<Navigate to="/patients" />} />
    </Routes>
  );
};

export default RoutesComponent;

import React from "react";
import { Link, useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav className="navbar" style={styles.navbar}>
      <div style={styles.logo}>
        <Link to="/" style={styles.link}>Speech Therapy Coach</Link>
      </div>
      <div style={styles.links}>
        {token ? (
          <>
            <Link to="/patients" style={styles.link}>Patients</Link>
            <Link to="/therapies" style={styles.link}>Therapies</Link>
            <button onClick={handleLogout} style={styles.button}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" style={styles.link}>Login</Link>
            <Link to="/register" style={styles.link}>Register</Link>
          </>
        )}
      </div>
    </nav>
  );
};

// Simple inline styles, you can replace with Tailwind or CSS later
const styles = {
  navbar: {
    display: "flex",
    justifyContent: "space-between",
    padding: "10px 20px",
    backgroundColor: "#1976d2",
    color: "#fff",
    alignItems: "center",
  },
  logo: {
    fontWeight: "bold",
    fontSize: "18px",
  },
  links: {
    display: "flex",
    gap: "15px",
    alignItems: "center",
  },
  link: {
    color: "#fff",
    textDecoration: "none",
    fontWeight: "500",
  },
  button: {
    padding: "5px 10px",
    backgroundColor: "#f44336",
    border: "none",
    borderRadius: "4px",
    color: "#fff",
    cursor: "pointer",
  },
};

export default Navbar;

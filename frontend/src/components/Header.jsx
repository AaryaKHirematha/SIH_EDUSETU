import { NavLink, useNavigate } from 'react-router-dom';
import { useState } from 'react';

export default function Header() {
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);
  const authToken = localStorage.getItem('stembridge_auth');
  const isAuthenticated = authToken && authToken.length > 0 && authToken !== 'null' && authToken !== 'undefined';

  const handleLogout = () => {
    localStorage.removeItem('stembridge_auth');
    navigate('/login');
    setMobileOpen(false);
  };

  return (
    <header className="edusetu-header">
      <div className="edusetu-container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <NavLink to="/" className="edusetu-brand" onClick={() => setMobileOpen(false)}>
          Edu<span>Setu</span>
        </NavLink>
        
        {/* Desktop Nav */}
        <nav className="edusetu-nav">
          <NavLink to="/" className={({isActive}) => isActive ? "nav-link active" : "nav-link"} end>Home</NavLink>
          <NavLink to="/translate" className={({isActive}) => isActive ? "nav-link active" : "nav-link"}>Translate</NavLink>
          <NavLink to="/history" className={({isActive}) => isActive ? "nav-link active" : "nav-link"}>History</NavLink>
          <NavLink to="/saved" className={({isActive}) => isActive ? "nav-link active" : "nav-link"}>Saved</NavLink>
          <NavLink to="/help" className={({isActive}) => isActive ? "nav-link active" : "nav-link"}>Help</NavLink>
          <NavLink to="/settings" className={({isActive}) => isActive ? "nav-link active" : "nav-link"}>Settings</NavLink>
          {isAuthenticated ? (
            <button onClick={handleLogout} className="button-secondary" style={{ minHeight: '2.5rem', padding: '0.4rem 1rem' }}>Logout</button>
          ) : (
            <NavLink to="/login" className="button-primary" style={{ minHeight: '2.5rem', padding: '0.4rem 1rem' }}>Sign In</NavLink>
          )}
        </nav>

        {/* Mobile Menu Button */}
        <button className="mobile-menu-btn" onClick={() => setMobileOpen(!mobileOpen)}>
          <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={mobileOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"}></path></svg>
        </button>

        {/* Mobile Nav */}
        {mobileOpen && (
          <nav className="mobile-nav">
            <NavLink to="/" className="nav-link" onClick={() => setMobileOpen(false)} end>Home</NavLink>
            <NavLink to="/translate" className="nav-link" onClick={() => setMobileOpen(false)}>Translate</NavLink>
            <NavLink to="/history" className="nav-link" onClick={() => setMobileOpen(false)}>History</NavLink>
            <NavLink to="/saved" className="nav-link" onClick={() => setMobileOpen(false)}>Saved</NavLink>
            <NavLink to="/help" className="nav-link" onClick={() => setMobileOpen(false)}>Help</NavLink>
            <NavLink to="/settings" className="nav-link" onClick={() => setMobileOpen(false)}>Settings</NavLink>
            {isAuthenticated ? (
              <button onClick={handleLogout} className="button-secondary" style={{ marginTop: '0.5rem' }}>Logout</button>
            ) : (
              <NavLink to="/login" className="button-primary" onClick={() => setMobileOpen(false)} style={{ marginTop: '0.5rem', textAlign: 'center' }}>Sign In</NavLink>
            )}
          </nav>
        )}
      </div>
    </header>
  );
}

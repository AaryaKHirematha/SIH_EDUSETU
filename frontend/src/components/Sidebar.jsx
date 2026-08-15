import { NavLink, useNavigate } from 'react-router-dom';

export default function Sidebar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('stembridge_auth');
    navigate('/login');
  };

  return (
    <div className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-title">STEMBridge</div>
        <div className="brand-subtitle">Translation Intelligence</div>
      </div>
      
      <div className="sidebar-nav">
        <NavLink to="/" className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")}>
          Translate / Dashboard
        </NavLink>
        <NavLink to="/history" className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")}>
          Translation History
        </NavLink>
      </div>
      
      <div className="sidebar-bottom">
        <div className="status-chip">
          <div className="status-dot"></div>
          Pipeline online
        </div>
        <div className="status-chip">
          IndicTrans2 · 200M
        </div>
        <div className="status-chip" style={{color: 'var(--accent-blue)'}}>
          CUDA · FP16 · RTX 3050
        </div>
        <button className="btn-logout" onClick={handleLogout}>
          <svg style={{width: '16px', marginRight: '6px'}} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
          Logout
        </button>
      </div>
    </div>
  );
}
